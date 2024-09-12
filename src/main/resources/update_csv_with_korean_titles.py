import csv
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
import nest_asyncio

# Jupyter 환경에서 이벤트 루프 중첩 허용
nest_asyncio.apply()

def get_wikidata_id(en_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={en_title}&prop=pageprops&format=json"
    try:
        response = requests.get(url)

        # JSON 응답이 아닌 경우 처리
        try:
            response_json = response.json()
        except ValueError:
            print(f"Warning: Non-JSON response for title {en_title}. Skipping...")
            return None

        pages = response_json['query']['pages']
        for page_id in pages:
            # pageprops가 존재하는지 체크
            if 'pageprops' in pages[page_id] and 'wikibase_item' in pages[page_id]['pageprops']:
                return pages[page_id]['pageprops']['wikibase_item']
            else:
                print(f"Warning: No 'wikibase_item' for title {en_title}. Skipping...")
                return None

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch data for title {en_title}. Exception: {e}")
        return None

    return None

def get_movie_details_from_wikidata(wikidata_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&props=labels|claims&languages=ko|en&format=json"
    try:
        response = requests.get(url).json()
        entity = response['entities'][wikidata_id]

        # 한국어 제목
        ko_title = entity['labels'].get('ko', {}).get('value', None)

        # 장르 (P136)
        genres = []
        if 'P136' in entity['claims']:
            for claim in entity['claims']['P136']:
                try:
                    genre_id = claim['mainsnak']['datavalue']['value']['id']
                    genre_label = get_label_from_wikidata_id(genre_id)
                    if genre_label != 'N/A':
                        genres.append(genre_label)
                except KeyError:
                    continue  # 'datavalue'가 없으면 건너뛰기

        # 감독 (P57)
        directors = []
        if 'P57' in entity['claims']:
            for claim in entity['claims']['P57']:
                try:
                    director_id = claim['mainsnak']['datavalue']['value']['id']
                    director_label = get_label_from_wikidata_id(director_id)
                    if director_label != 'N/A':
                        directors.append(director_label)
                except KeyError:
                    continue  # 'datavalue'가 없으면 건너뛰기

        # 배우 (P161)
        actors = []
        if 'P161' in entity['claims']:
            for claim in entity['claims']['P161']:
                try:
                    actor_id = claim['mainsnak']['datavalue']['value']['id']
                    actor_label = get_label_from_wikidata_id(actor_id)
                    if actor_label != 'N/A':
                        actors.append(actor_label)
                except KeyError:
                    continue  # 'datavalue'가 없으면 건너뛰기

        return ko_title, genres, directors, actors

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch movie details for Wikidata ID {wikidata_id}. Exception: {e}")
        return None, [], [], []

    except KeyError as e:
        print(f"Error: Missing expected key in response for Wikidata ID {wikidata_id}. KeyError: {e}")
        return None, [], [], []



# 위키데이터 ID에서 레이블(이름) 가져오기
def get_label_from_wikidata_id(wikidata_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&props=labels&languages=ko|en&format=json"
    response = requests.get(url).json()
    entity = response['entities'][wikidata_id]
    label = entity['labels'].get('ko', {}).get('value', entity['labels'].get('en', {}).get('value', None))
    return label

def process_movie(row):
    # Maintain existing data while adding new data
    wiki_page = row['Wiki Page'].replace(" ", "_")  # Adjust spaces for URL format
    en_title = wiki_page.split("/")[-1]
    wikidata_id = get_wikidata_id(en_title)

    if wikidata_id:
        ko_title, genres, directors, actors = get_movie_details_from_wikidata(wikidata_id)

        # Function to update column values, removing unwanted values and adding new ones
        def update_column(column_value, new_values):
            unwanted_values = {'unKnown', 'unknown', 'Unknown'}
            if new_values:
                # Filter out unwanted values from the column
                existing_values = set(value.strip() for value in column_value.split(", ")) if column_value else set()
                existing_values = {value for value in existing_values if value.lower() not in unwanted_values}

                # Add new values to the existing set
                new_values_set = {value.strip() for value in new_values if value.strip().lower() not in unwanted_values}

                # Union of existing and new values
                updated_values = existing_values.union(new_values_set)

                return ', '.join(sorted(updated_values))
            return column_value

        # Update columns, removing unwanted values and adding new data
        if ko_title and ko_title.lower() not in ['unKnown', 'unknown', 'Unknown']:
            row['Title'] = update_column(row.get('Title', ''), [ko_title])
        if genres and not all(genre.lower() in ['unKnown', 'unknown', 'Unknown'] for genre in genres):
            row['Genre'] = update_column(row.get('Genre', ''), genres)
        if directors and not all(director.lower() in ['unKnown', 'unknown', 'Unknown'] for director in directors):
            row['Director'] = update_column(row.get('Director', ''), directors)
        if actors and not all(actor.lower() in ['unKnown', 'unknown', 'Unknown'] for actor in actors):
            row['Cast'] = update_column(row.get('Cast', ''), actors)

    return row

# CSV 파일에서 데이터를 읽고, 비동기 처리
async def process_movies(input_file, output_file):
    # CSV 읽기
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = [row for row in reader]

    # ThreadPoolExecutor로 비동기 처리 (10개 스레드로 처리)
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, process_movie, row) for row in rows]
        updated_rows = await asyncio.gather(*tasks)

    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        fieldnames = reader.fieldnames  # 기존 필드 유지
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

# 메인 함수
async def main():
    input_file = 'input.csv'  # 입력 파일명
    output_file = 'output.csv'  # 출력 파일명

    await process_movies(input_file, output_file)

# 실행 (Jupyter에서는 바로 await 사용)
await main()
