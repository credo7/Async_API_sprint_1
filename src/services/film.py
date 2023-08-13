import json
from functools import lru_cache
from typing import Optional, List

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis
import orjson

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_many_by_parameters(self, page_number: int, page_size: int, sort: str = None):
        films = await self._film_list_from_cache(page_size=page_size, page_number=page_number, sort=sort)
        if not films:
            films = await self._get_film_list_from_elastic(page_number=page_number, page_size=page_size, sort=sort)
            if not films:
                return None
            await self._put_film_list_to_cache(page_number=page_number, page_size=page_size, sort=sort, films=films)

        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
            return Film.parse_from_elastic(doc)
        except NotFoundError:
            return None

    async def _get_film_list_from_elastic(self, page_number: int, page_size: int, sort: str = None):
        query = {'query': {'match_all': {}}, 'size': page_size, 'from': (page_number - 1) * page_size}

        if sort:
            sort_key, sort_order = (sort[1:], 'desc') if sort.startswith('-') else (sort, 'asc')
            query['sort'] = [{sort_key: sort_order}]

        try:
            doc = await self.elastic.search(index='movies', body=query)
        except NotFoundError:
            return None
        documents = doc['hits']['hits']
        films = [Film.parse_from_elastic(doc) for doc in documents]
        return films

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_from_redis(data)
        return film

    async def _film_list_from_cache(self, page_size: int, page_number: int, sort: str = None):
        cache_key = f"{sort or ''}_{page_size}_{page_number}"

        data = await self.redis.get(cache_key)
        if not data:
            return None

        film_list = orjson.loads(data)
        films = [Film.parse_from_redis(film) for film in film_list]

        return films

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.model_dump_json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_film_list_to_cache(self, sort: str, page_size: int, page_number: int, films: List[Film]):
        cache_key = f"{sort or ''}_{page_size}_{page_number}"

        films_json_list = [film.model_dump_json() for film in films]
        films_json_str = orjson.dumps(films_json_list)

        await self.redis.set(cache_key, films_json_str, FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
