##!/bin/bash
echo "Starting init-elasticsearch.sh script..."

# Check index 존재 여부
if curl -s -o /dev/null -w "%{http_code}" "http://elasticsearch:9200/wiki_movies" | grep -q "200"; then
  echo "Index 'wiki_movies' already exists. Skipping index creation."
else
  echo "Creating index 'wiki_movies' with n-gram analyzer..."

  # index 생성 및 n-gram setting 적용
  response=$(curl -s -w "\n%{http_code}" -X PUT "http://elasticsearch:9200/wiki_movies" -H "Content-Type: application/json" -d'
  {
    "settings": {
        "analysis": {
          "tokenizer": {
            "ngram_tokenizer": {
              "type": "ngram",
              "min_gram": 2,
              "max_gram": 3,
              "token_chars": [
                "letter",
                "digit"
              ]
            }
          },
          "analyzer": {
            "ngram_analyzer": {
              "type": "custom",
              "tokenizer": "ngram_tokenizer",
              "filter": [
                "lowercase"
              ]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "analyzer": "ngram_analyzer"
          },
          "director": {
            "type": "text",
            "analyzer": "ngram_analyzer"
          },
          "cast": {
            "type": "text",
            "analyzer": "ngram_analyzer"
          }
        }
      }
    }
  ')

  http_code=$(echo "$response" | tail -n1)
  response_body=$(echo "$response" | sed '$d')

  if [ "$http_code" -ne 200 ]; then
    echo "Failed to create index. HTTP status code: $http_code"
    echo "Response body: $response_body"
    exit 1
  else
    echo "Index created successfully."
  fi
fi

# elasticsearch container 실행 유지
tail -f /dev/null
