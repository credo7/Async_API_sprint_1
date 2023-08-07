from etl.create_postgresql_connection import create_postgresql_connection
from etl.extract_transform.postgres_extractor import PostgresReceiver, TableQuery
from etl.extract_transform.postgres_orchester import PostgresOrchester
from etl.extract_transform.query_builder import (
    TargetQuery,
    RelatedQuery,
    MoviesTransformQuery,
    EarliestUpdateTimeQuery,
)
from etl.extract_transform.query_manager import (
    PostgresTableName,
    IntermediateTable,
    QueryManager,
)
from etl.extract_transform.schemas import FilmWork
from etl.load.elastic_search_loader import ElasticLoader
from etl.env_settings import settings
from etl.load.elastic_config import ElasticIndexName, ELASTIC_CONFIGS
from etl.time_event_decorators.repeat_every import repeat_every_seconds
from etl.extract_transform.boundaries import get_query_boundaries
from state.storage import RedisStorage
from state.state import State
from redis.client import Redis


# ELASTIC_INDEXES = list(ElasticIndex)
ELASTIC_INDEXES = [ElasticIndexName.MOVIE]
TABLE_NAMES = list(PostgresTableName)
# TABLE_NAMES = ['film_work', 'person', 'genre']


# @repeat_every_seconds(settings.repeat_time_seconds)
def synchronise_postgres_elastic(loader: ElasticLoader, extractor: PostgresOrchester, state):
    for index in ELASTIC_INDEXES:
        current_state_key = f'{index.value}_update'
        update_state = state.get_state(current_state_key)
        boundaries = get_query_boundaries(last_update_time=update_state)
        data_to_load = extractor.extract_transformed_data(
            index=index, table_names=TABLE_NAMES, boundaries=boundaries
        )
        loader.load_data_to_es(es_data=data_to_load, es_index=index)
        # state.set_state(current_state_key)


if __name__ == '__main__':
    elastic_search_loader = ElasticLoader(
        es_url=settings.elastic_url, es_indexes=ELASTIC_INDEXES, es_configs=ELASTIC_CONFIGS
    )
    redis_storage = RedisStorage(redis_adapter=Redis.from_url(url=settings.redis_url))
    state = State(storage=redis_storage)

    movie_query_manager = QueryManager(
        base_table=PostgresTableName.FILM_WORK,
        queries={
            TableQuery.TARGET.value: TargetQuery(),
            TableQuery.RELATED.value: RelatedQuery(),
            TableQuery.TRANSFORM.value: MoviesTransformQuery(),
            TableQuery.GET_EARLIEST_UPDATE_TIME.value: EarliestUpdateTimeQuery(),
        },
        relative_tables={
            PostgresTableName.GENRE.value: IntermediateTable(
                table_name='content.genre_film_work',
                main_id_field='film_work_id',
                related_id_field='genre_id',
            ),
            PostgresTableName.PERSON.value: IntermediateTable(
                table_name='content.person_film_work',
                main_id_field='film_work_id',
                related_id_field='person_id',
            ),
        },
    )

    movie_receiver = PostgresReceiver(
        index=ElasticIndexName.MOVIE, query_manager=movie_query_manager, schema=FilmWork
    )
    extractor = PostgresOrchester(extractors=[movie_receiver])
    synchronise_postgres_elastic(
        loader=elastic_search_loader, extractor=extractor, state=state
    )
