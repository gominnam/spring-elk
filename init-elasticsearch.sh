##!/bin/bash
#
#echo "Starting init-elasticsearch.sh script..."
#
## Elasticsearch가 실행된 후 인덱스 생성
##until curl -f -X GET "http://elasticsearch:9200/_cluster/health?wait_for_status=yellow&timeout=50s"; do
##  echo "Waiting for Elasticsearch in shell file..."
##  sleep 5
##done
#
## Elasticsearch가 실행된 후 인덱스 생성
#until curl -f -X GET "http://elasticsearch:9200/_cluster/health?wait_for_status=yellow&timeout=50s"; do
#  echo "Waiting for Elasticsearch in shell file..."
#  sleep 5
#done
#
## N-gram 분석기를 포함한 인덱스 생성
##curl -f -X PUT "http://elasticsearch:9200/wiki_movies" -H "Content-Type: application/json" -d'
#response=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "http://elasticsearch:9200/wiki_movies" -H "Content-Type: application/json" -d'
#{
#  "settings": {
#    "analysis": {
#      "tokenizer": {
#        "edge_ngram_tokenizer": {
#          "type": "edge_ngram",
#          "min_gram": 2,
#          "max_gram": 3,
#          "token_chars": ["letter", "digit", "whitespace"]
#        }
#      },
#      "analyzer": {
#        "edge_ngram_analyzer": {
#          "type": "custom",
#          "tokenizer": "edge_ngram_tokenizer",
#          "filter": ["lowercase"]
#        }
#      }
#    }
#  },
#  "mappings": {
#    "properties": {
#      "title": {
#        "type": "text",
#        "analyzer": "edge_ngram_analyzer",
#        "search_analyzer": "standard"
#      },
#      "director": {
#        "type": "text",
#        "analyzer": "edge_ngram_analyzer",
#        "search_analyzer": "standard"
#      },
#      "cast": {
#        "type": "text",
#        "analyzer": "edge_ngram_analyzer",
#        "search_analyzer": "standard"
#      }
#    }
#  }
#}')
#
#if [ "$response" -ne 200 ]; then
#  echo "Failed to create index. HTTP status code: $response"
#  exit 1
#fi
#
#echo "Index created successfully."



#!/bin/bash

echo "Starting init-elasticsearch.sh script..."

# Elasticsearch가 실행된 후 인덱스 생성
until curl -s -o /dev/null -w "%{http_code}" "http://elasticsearch:9200/_cluster/health?wait_for_status=yellow&timeout=50s" | grep "200"; do
  echo "Waiting for Elasticsearch in shell file..."
  sleep 5
done

# N-gram 분석기를 포함한 인덱스 생성
response=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "http://elasticsearch:9200/wiki_movies" -H "Content-Type: application/json" -d'
{
  "settings": {
    "analysis": {
      "analyzer": {
        "autocomplete": {
          "type": "custom",
          "tokenizer": "autocomplete",
          "filter": ["lowercase"]
        },
        "autocomplete_search": {
          "type": "custom",
          "tokenizer": "lowercase"
        }
      },
      "tokenizer": {
        "autocomplete": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 10,
          "token_chars": ["letter"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "autocomplete_search"
      },
      "director": {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "autocomplete_search"
      },
      "cast": {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "autocomplete_search"
      }
    }
  }
}')

if [ "$response" -ne 200 ]; then
  echo "Failed to create index. HTTP status code: $response"
  exit 1
fi

echo "Index created successfully."