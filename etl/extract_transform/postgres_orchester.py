import logging
from typing import List
from etl.extract_transform.boundaries import get_query_boundaries
from etl.extract_transform.boundaries import DateBoundaries
from etl.load.elastic_config import ElasticIndexName
from etl.extract_transform.postgres_extractor import PostgresReceiver


class PostgresOrchester:
    def __init__(self, extractors: List[PostgresReceiver]):
        self.extractors = extractors

    def extract_transformed_data(
        self, index: ElasticIndexName, table_names: List[str], boundaries: DateBoundaries
    ):
        if boundaries is None:
            from_time = self.extract_min_update_time()
            boundaries = get_query_boundaries(from_time)
        target_extractor = None
        for extractor in self.extractors:
            if extractor.index == index:
                target_extractor = extractor
                break
        if target_extractor is None:
            logging.info('No target extractor for index %s', index.value)
            return
        return target_extractor.get_transformed_ids(table_names, boundaries)

    def extract_min_update_time(self):
        minimal_update_points = [
            extractor.get_minimal_update_time() for extractor in self.extractors
        ]
        return min(minimal_update_points)
