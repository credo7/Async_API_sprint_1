#!/bin/bash

# Get the PostgreSQL user role from an environment variable
POSTGRES_USER_ROLE=${POSTGRES_USER:-app}
echo "Postgres user role is: $POSTGRES_USER_ROLE"

# Wait for PostgreSQL
until pg_isready -h postgres_test -U $POSTGRES_USER_ROLE; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - proceeding"

# Load data from SQLite to Postgres
python sqlite_to_postgres/load_data.py
if [ $? -ne 0 ]; then
  echo "Failed to load data - exiting"
  exit 1
fi

# Wait for ElasticSearch to be ready
while ! curl -s http://elasticsearch_test:9200/_cat/health; do
    echo "Elastic is unavailable - sleeping"
    sleep 1
done

python main.py