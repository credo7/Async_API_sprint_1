from contextlib import contextmanager
import psycopg2
from psycopg2.extras import DictCursor
from etl.time_event_decorators.backoff import backoff
from env_settings import settings


@contextmanager
@backoff()
def create_postgresql_connection():
    pg_connection = psycopg2.connect(
        dbname=settings.database_name,
        user=settings.database_username,
        password=settings.database_password,
        host=settings.database_hostname,
        port=settings.database_port,
        cursor_factory=DictCursor,
    )
    yield pg_connection
    pg_connection.close()
