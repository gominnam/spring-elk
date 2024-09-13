import csv
import aiohttp  # 비동기 HTTP 요청
import asyncio
import random
import time
import nest_asyncio

# Jupyter 환경에서 이벤트 루프 중첩 허용
nest_asyncio.apply()

# 비동기적으로 HTTP 요청 보내기
async def fetch(session, url, retries=10, backoff_factor=10, max_backoff=60):
    try:
        for attempt in range(retries):
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:  # Too Many Requests
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        wait_time = int(retry_after)  # 서버가 응답하는 시간 사용
                    else:
                        wait_time = min(backoff_factor * (2 ** attempt) + random.uniform(0, 1), max_backoff)
                    print(f"Rate limited. Waiting for {wait_time} seconds before retrying...")
                    await asyncio.sleep(wait_time)  # 대기 시간 설정
                else:
                    print(f"Unexpected status {response.status} for URL {url}")
                    return None
        print(f"Failed to fetch data after {retries} attempts.")
    except Exception as e:
        print(f"Error: {e}")
        return None

async def get_wikidata_id(session, en_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={en_title}&prop=pageprops&format=json"
    response_json = await fetch(session, url)
    if response_json:
        pages = response_json.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            if 'pageprops' in page_info and 'wikibase_item' in page_info['pageprops']:
                return page_info['pageprops']['wikibase_item']
    print(f"Warning: No 'wikibase_item' for title {en_title}. Skipping...")
    return None

# 비동기적으로 영화 정보 가져오기
async def get_movie_details_from_wikidata(session, wikidata_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&props=labels|claims&languages=ko|en&format=json"
    try:
        async with session.get(url) as response:
            response_json = await response.json()
            entity = response_json['entities'][wikidata_id]

            # 한국어 제목
            ko_title = entity['labels'].get('ko', {}).get('value', None)

            # 장르 (P136)
            genres = []
            if 'P136' in entity['claims']:
                for claim in entity['claims']['P136']:
                    try:
                        genre_id = claim['mainsnak']['datavalue']['value']['id']
                        genre_label = await get_label_from_wikidata_id(session, genre_id)
                        if genre_label != 'N/A':
                            genres.append(genre_label)
                    except KeyError:
                        continue

            # 감독 (P57)
            directors = []
            if 'P57' in entity['claims']:
                for claim in entity['claims']['P57']:
                    try:
                        director_id = claim['mainsnak']['datavalue']['value']['id']
                        director_label = await get_label_from_wikidata_id(session, director_id)
                        if director_label != 'N/A':
                            directors.append(director_label)
                    except KeyError:
                        continue

            # 배우 (P161)
            actors = []
            if 'P161' in entity['claims']:
                for claim in entity['claims']['P161']:
                    try:
                        actor_id = claim['mainsnak']['datavalue']['value']['id']
                        actor_label = await get_label_from_wikidata_id(session, actor_id)
                        if actor_label != 'N/A':
                            actors.append(actor_label)
                    except KeyError:
                        continue

            return ko_title, genres, directors, actors

    except aiohttp.ClientError as e:
        print(f"Error: Failed to fetch movie details for Wikidata ID {wikidata_id}. Exception: {e}")
        return None, [], [], []

    except KeyError as e:
        print(f"Error: Missing expected key in response for Wikidata ID {wikidata_id}. KeyError: {e}")
        return None, [], [], []

# 비동기적으로 Wikidata ID에서 레이블 가져오기
async def get_label_from_wikidata_id(session, wikidata_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&props=labels&languages=ko|en&format=json"
    async with session.get(url) as response:
        response_json = await response.json()
        entity = response_json['entities'][wikidata_id]
        label = entity['labels'].get('ko', {}).get('value', entity['labels'].get('en', {}).get('value', None))
        return label

# 세마포어를 사용하여 동시 요청 수를 제한
sem = asyncio.Semaphore(5)  # 한 번에 5개의 요청만 허용(약 60프로 시간 단축)// 10개로 테스트 한 결과 429(TOO MANY REQUESTS) 에러 발생

async def process_movie(session, row):
    async with sem:
        wiki_page = row['Wiki Page'].replace(" ", "_")
        en_title = wiki_page.split("/")[-1]
        wikidata_id = await get_wikidata_id(session, en_title)

        if wikidata_id:
            ko_title, genres, directors, actors = await get_movie_details_from_wikidata(session, wikidata_id)

            def update_column(column_value, new_values):
                unwanted_values = {'unKnown', 'unknown', 'Unknown'}
                if new_values:
                    existing_values = set(value.strip() for value in column_value.split(", ")) if column_value else set()
                    existing_values = {value for value in existing_values if value.lower() not in unwanted_values}
                    new_values_set = {value.strip() for value in new_values if value and value.strip().lower() not in unwanted_values}
                    updated_values = existing_values.union(new_values_set)
                    return ', '.join(sorted(updated_values))
                return column_value

            if ko_title:
                row['Title'] = update_column(row.get('Title', ''), [ko_title])
            if genres:
                row['Genre'] = update_column(row.get('Genre', ''), genres)
            if directors:
                row['Director'] = update_column(row.get('Director', ''), directors)
            if actors:
                row['Cast'] = update_column(row.get('Cast', ''), actors)

        return row

# 비동기적으로 CSV 파일 처리
async def process_movies(input_file, output_file):
    async with aiohttp.ClientSession() as session:
        # CSV 읽기
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            rows = [row for row in reader]

        # 비동기적으로 영화 처리
        tasks = [process_movie(session, row) for row in rows]
        updated_rows = await asyncio.gather(*tasks)

        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

# 메인 함수
async def main():
    input_file = 'input.csv'
    output_file = 'output.csv'
    await process_movies(input_file, output_file)

# 실행
await main()
