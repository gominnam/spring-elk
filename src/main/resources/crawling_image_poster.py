import csv
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def get_poster_image_url(wiki_page_url):
  try:
    response = requests.get(wiki_page_url)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.content, 'html.parser')
    image_tag = soup.select_one('.infobox-image img')
    poster_image_url = image_tag.get('src')
    return poster_image_url
  except Exception as e:
    print(f"Error fetching poster image URL for {wiki_page_url}: {e}")
    return None

# Input and output file paths
input_file = 'wiki_movie_plots_deduped_noline.csv'
output_file = 'output.csv'

existing_urls = set()

try:
    with open(output_file, 'r', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(outfile)
        for row in reader:
            existing_urls.add(row['Wiki Page'])  # 이미 처리된 Wiki Page URL을 기록
except FileNotFoundError:
    # 만약 output.csv 파일이 없을 경우, 처음부터 새로 작성
    pass

# Read the input CSV file
with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'a', newline='', encoding='utf-8') as outfile:
  reader = csv.DictReader(infile)
  fieldnames = reader.fieldnames + ['Poster Image URL']
  writer = csv.DictWriter(outfile, fieldnames=fieldnames)

  if not existing_urls:
      writer.writeheader()

  def process_row(row):
      wiki_page_url = row['Wiki Page']
      if wiki_page_url in existing_urls:
          return None  # 이미 처리된 경우 건너뜀
      poster_image_url = get_poster_image_url(wiki_page_url)
      row['Poster Image URL'] = poster_image_url
      return row

  # 병렬로 작업 처리
  with ThreadPoolExecutor(max_workers=10) as executor:
      results = list(executor.map(process_row, reader))

  # 결과 저장
  for row in results:
      if row:
          writer.writerow(row)
