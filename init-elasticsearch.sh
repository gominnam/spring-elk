#!/bin/bash

# Elasticsearch가 실행된 후 인덱스 생성
until curl -X GET "http://elasticsearch:9200/_cluster/health?wait_for_status=yellow&timeout=50s"; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

# N-gram 분석기를 포함한 인덱스 생성
curl -X PUT "http://elasticsearch:9200/wiki_movies" -H "Content-Type: application/json" -d'
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "edge_ngram_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 3,
          "token_chars": ["letter", "digit", "whitespace"]
        }
      },
      "analyzer": {
        "edge_ngram_analyzer": {
          "type": "custom",
          "tokenizer": "edge_ngram_tokenizer",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "edge_ngram_analyzer",
        "search_analyzer": "standard"
      },
      "director": {
        "type": "text",
        "analyzer": "edge_ngram_analyzer",
        "search_analyzer": "standard"
      },
      "cast": {
        "type": "text",
        "analyzer": "edge_ngram_analyzer",
        "search_analyzer": "standard"
      }
    }
  }
}'
