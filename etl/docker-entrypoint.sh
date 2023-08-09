#!/bin/bash

# Wait for PostgreSQL
until pg_isready -h postgres_test -U postgres_test; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - proceeding"

# Wait for ElasticSearch to be ready
while ! curl -s http://elasticsearch_test:9200/_cat/health; do
    echo "Elastic is unavailable - sleeping"
    sleep 1
done

python main.py