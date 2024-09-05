
# ELK (Elasitcsearch, Logstash, Kibana) Stack

## 목적

- Netflix, Coupang Play 처럼 하나의 검색란에서 영화 제목, 감독, 장르, 배우를 검색하여 결과를 확인할 수 있는 검색 서비스 구현
- ELK 스택을 사용하여 데이터를 저장하고 검색(Kaggle wiki movie plots 데이터 사용)


## 고려사항

- 



## 실행방법

1. csv 파일 다운
2. docker-compose (elasticsearch, logstash, kibana) 실행
```angular2html
// 처음 실행할 경우 logstash 컨테이너에서 csv 파일을 파싱하고 elasticsearch에 저장
docker-compose up -d
```

## Data
파일 수정 및 파싱
- logstash 에서 csv 파일을 정확하게 파싱할 수있도록 파일 수정
- python 코드를 사용하여 개행 특수문자 제거

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


2. 2. ElasticSearch 대량 데이터 비효율

    - **원인과 해결 방법**
      - Q: NoSQL 기반 검색 엔진으로 문서를 수정하는게 아닌 삭제, 수정하는 방식으로 대량의 업데이트 경우 비용이 큰 문제발생
      - A: Bulk API 사용(실시간 update 가 필요한 경우 용이)
      

## References

- [Kaggle Dataset](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots)
- [Elasticsearch Srping](https://spring.io/projects/spring-data-elasticsearch)
- [Elasticsearch Guild](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html)
