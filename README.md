
# ELK (Elasitcsearch, Logstash, Kibana) Stack

## 목적

- Netflix, Coupang Play 처럼 하나의 검색란에서 영화 제목, 감독, 장르, 배우를 검색하여 결과를 확인할 수 있는 검색 서비스 구현
- ELK 스택을 사용하여 효율적인 검색기능 구현
- 빅데이터를 원하는 데이터로 수정 후 저장(Kaggle wiki movie plots 데이터 사용)


## 실행방법

1. csv 파일 다운
2. docker-compose (elasticsearch, logstash, kibana) 실행
```angular2html
// 처음 실행할 경우 logstash 컨테이너에서 csv 파일을 파싱하고 elasticsearch에 저장
docker-compose up -d
```

## Data
파일 수정 및 파싱

1. 개행 특수 문자 제거
- logstash 에서 csv 파일을 정확하게 파싱할 수있도록 파일 수정

```python
# prompt: 원본 csv 파일에서 개행 특수문자 제거

from tqdm import tqdm
import csv
with open('wiki_movie_plots_deduped.csv', 'r') as infile, open('output.csv', 'w') as outfile:
  reader = csv.reader(infile)
  writer = csv.writer(outfile)
  for row in tqdm(reader):
    new_row = [''.join(c for c in s if c not in ['\n']) for s in row]
    writer.writerow(new_row)
    
```

2. 포스터 이미지 링크 추가
- poster_image_url 데이터 크롤링하여 추가
  - python source code 참조 (src/main/python/insert_poster_image.py)

3. 한국어로 검색할 수 있도록 데이터 추가
- 

## Custom Scoring
- 검색 조건 title, genre, actor


## Trouble Shooting

1. 1. **Endpoint POST /update-poster-images 요청 시 'all shards failed' 오류 발생**

    - **Shard Health 확인**
      ```bash
      curl -X GET "http://localhost:9200/_cat/indices?v" | jq
      ```
        - 결과: yellow, green 상태로 문제 없음을 확인 (red 상태일 경우 문제 발생)

    - **Mapping 확인**
      ```bash
      curl -X GET "http://localhost:9200/wiki_movies/_mapping" | jq
      ```
        - 결과: 새로 생성한 `post-image-url` 확인

    - **해결 방법**
      - elasticsearch 의 default max_result_window 값이 10000으로 설정되어 있어서, 10000개 이상의 데이터를 한번에 가져올 수 없음
      - Paging을 이용하여 데이터를 가져오도록 수정
      - ref : https://discuss.elastic.co/t/es-search-failed-search-phase-execution-exception-all-shards-failed/335428

1. 2. ElasticSearch 대량 데이터 비효율 문제

    - **원인과 해결 방법**
      - Q: NoSQL 기반 검색 엔진으로 문서를 수정하는게 아닌 삭제, 수정하는 방식으로 대량의 업데이트 경우 비용이 큰 문제발생
      - A1: Bulk API 사용(실시간 update 가 필요한 경우 용이)
      - A2: poster_image_url 데이터 크롤링하여 CSV 파일을 수정(이 방법으로 해결)


</br></br>
2. 1. **한글 검색으로도 조회할 수 있도록 데이터 추가 과정 문제**
   - **원인**
     1. papago(api 서비스 중단)나 google 번역기를 사용하려 했지만 영어 Title 과 한글 Title 이 번역과 불일치로 인해 사용 불가
     2. Wikipedia의 영어 Title을 통해 Wikidata ID를 얻어 한글 Title 을 얻는 방식
        - 위 방법으로는 한글 Title이 없는 경우가 있었지만 대중적이지 않은 영화들로 한글 검색을 지원을 안하는 방향으로 결정(해결 방안을 추후 모색하기)


세마포어 thread 5 50 프로 시간 단축(2hour 30minutes)
## References

- [Kaggle Dataset](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots)
- [Elasticsearch Srping](https://spring.io/projects/spring-data-elasticsearch)
- [Elasticsearch Guild](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html)
