
# ELK (Elasitcsearch, Logstash, Kibana) Stack

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


## References

- [Kaggle Dataset](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots)
- [Elasticsearch Srping](https://spring.io/projects/spring-data-elasticsearch)
- [Elasticsearch Guild](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html)
