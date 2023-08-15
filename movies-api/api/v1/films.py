from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from services.film import FilmService, get_film_service
from models.film import Film
from models.sort import MoviesSortOptions

router = APIRouter()


@router.get('/{film_id}', response_model=Film)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service),
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film


@router.get('/', response_model=List[Film])
async def film_details_list(
    sort: MoviesSortOptions = Query(
        None,
        description='Sort order (Use "imdb_rating" for ascending or "-imdb_rating" for descending)',
    ),
    page_size: int = Query(50, ge=1, le=100, description='Number of films per page'),
    page_number: int = Query(1, ge=1, description='Page number'),
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:
    films = await film_service.get_many_by_parameters(
        page_number=page_number, page_size=page_size, sort=sort
    )
    return films
