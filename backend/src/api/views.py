from typing import List

from fastapi import APIRouter, Depends

from api.v1.films import get_film_details, get_film_list, get_film_search
from api.v1.genres import get_genre_details, get_genre_list
from api.v1.persons import get_person_details, get_person_films, get_person_list, get_person_search
from models.film import Film, FilmList, FilmModified
from models.genre import Genre, GenreList
from models.person import Person, PersonList
from services.list import ListService
from services.retrieve import RetrieveService

router = APIRouter()


@router.get(
    '/films',
    response_model=FilmList,
    response_model_by_alias=False,
    summary='Главная страница',
    description='Популярные фильмы и фильтрация по жанрам',
    response_description='Название и рейтинг фильмов',
    tags=['films'])
async def films(films_list: ListService = Depends(get_film_list)) -> List[FilmModified]:
    return await films_list.get()


@router.get(
    '/films/search',
    response_model=FilmList,
    response_model_by_alias=False,
    summary='Поиск фильмов',
    description='Полнотекстовый поиск по названиям фильмов',
    response_description='Название и рейтинг фильмов',
    tags=['films'])
async def films_search(films_by_search: ListService = Depends(get_film_search)) -> List[FilmModified]:
    return await films_by_search.get()


@router.get(
    '/films/{film_id}',
    response_model=Film,
    response_model_by_alias=False,
    summary='Страница фильма',
    description='Полная информация по фильму',
    response_description='Название, описание, рейтинг, жанры и персонал фильмов',
    tags=['films'])
async def films_pk(film_details: RetrieveService = Depends(get_film_details)) -> Film:
    return await film_details.get()


@router.get(
    '/persons',
    response_model=PersonList,
    response_model_by_alias=False,
    summary='Персоны',
    description='Список персон',
    response_description='Полное имя, основная роль, фильмы c участием персоны',
    tags=['persons'])
async def persons(persons_list: ListService = Depends(get_person_list)) -> List[Person]:
    return await persons_list.get()


@router.get(
    '/persons/search',
    response_model=PersonList,
    response_model_by_alias=False,
    summary='Поиск персон',
    description='Полнотекстовый поиск по именам персон',
    response_description='Полное имя, основная роль, фильмы c участием персоны',
    tags=['persons'])
async def persons_search(persons_by_search: ListService = Depends(get_person_search)) -> List[Person]:
    return await persons_by_search.get()


@router.get(
    '/persons/{person_id}',
    response_model=Person,
    response_model_by_alias=False,
    summary='Страница персоны',
    description='Полная информация по персоне',
    response_description='Полное имя, основная роль, фильмы c участием персоны',
    tags=['persons'])
async def persons_pk(person_details: RetrieveService = Depends(get_person_details)) -> Person:
    return await person_details.get()


@router.get(
    '/persons/{person_id}/film',
    response_model=FilmList,
    response_model_by_alias=False,
    summary='Фильмы по персоне',
    description='Фильмы персоны отсортированные по популярности',
    response_description='Название и рейтинг фильмов персоны',
    tags=['persons'])
async def persons_pk_film(films_by_person: ListService = Depends(get_person_films)) -> List[FilmModified]:
    return await films_by_person.get()


@router.get(
    '/genres',
    response_model=GenreList,
    response_model_by_alias=False,
    summary='Жанры',
    description='Список жанров',
    response_description='Название и описание жанров',
    tags=['genres'])
async def genres(genres_list: ListService = Depends(get_genre_list)) -> List[Genre]:
    return await genres_list.get()


@router.get(
    '/genres/{genre_id}',
    response_model=Genre,
    response_model_by_alias=False,
    summary='Страница жанра',
    description='Полная информация по жанру',
    response_description='Название и описание жанра',
    tags=['genres'])
async def genres_pk(genre_details: RetrieveService = Depends(get_genre_details)) -> Genre:
    return await genre_details.get()
