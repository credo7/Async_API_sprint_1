from enum import Enum


class SortOptions(str, Enum):
    asc = 'imdb_rating'
    desc = '-imdb_rating'
