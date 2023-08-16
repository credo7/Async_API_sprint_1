from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from models.person import Person
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=List[Person])
async def person_details_list(
    # sort: str = Query(None, description='Sort order (-name to sort descending)'),
    search: str = Query(None, description='Searching text'),
    page_size: int = Query(50, ge=1, le=100, description='Number of persons per page'),
    page_number: int = Query(1, ge=1, description='Page number'),
    person_service: PersonService = Depends(get_person_service),
) -> List[Person]:
    persons = await person_service.filter(
        search=search, page_number=page_number, page_size=page_size
    )

    return persons


@router.get('/{person_id}', response_model=Person)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service),
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return person
