from typing import Dict, List, Optional

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MatchPhrase, Nested, QueryString, Term, Terms


def genres_by_film(film: Dict) -> Dict:
    """
    Функция для получения запроса в Elasticsearch с целью получить жанры переданного фильма.

    Args:
        film: Данные фильма

    Returns:
        Dict: Запрос в Elasticsearch для жанров фильма
    """
    query = Search().filter(Terms(name__raw=film['genre']))
    return query.to_dict()


def directors_by_film(film: Dict) -> Dict:
    """
    Функция для получения запроса в Elasticsearch с целью получить режиссёров переданного фильма.

    Args:
        film: Данные фильма

    Returns:
        Dict: Запрос в Elasticsearch для режиссёров фильма
    """
    query = Search().filter(Terms(full_name__raw=film['director']))
    return query.to_dict()


def films_by_person(person: Dict, fields: Optional[List] = None) -> Dict:
    """
    Функция для получения запроса в Elasticsearch с целью получить фильмы переданной персоны.

    Args:
        person: Данные персоны
        fields: Поля индекса в Elasticsearch с данными фильма

    Returns:
        Dict: Запрос в Elasticsearch для фильмов персоны
    """
    query = Search().source(fields).sort('-imdb_rating').filter(
        Nested(path='actors', query=Term(actors__id=person['id'])) |
        Nested(path='writers', query=Term(writers__id=person['id'])) |
        MatchPhrase(director=person['full_name']),
    )[:1000]
    return query.to_dict()


def films_by_genre(genre: Dict) -> Dict:
    """
    Функция для получения запроса в Elasticsearch с целью получить фильмы переданного жанра.

    Args:
        genre: Данные жанра

    Returns:
        Dict: Запрос в Elasticsearch для фильмов жанра
    """
    query = Search().filter(Term(genre=genre['name']))
    return query.to_dict()


def search_data(query_str: str, fields: Optional[List] = None) -> Dict:
    """
    Функция для получения запроса в Elasticsearch с целью полнотекстового поиска.

    Args:
        query_str: Запрос для полнотекстового поиска
        fields: Поля индекса в Elasticsearch по которым ведётся поиск

    Returns:
        Dict: Запрос в Elasticsearch для полнотекстового поиска
    """
    query = Search().filter(QueryString(query=query_str, fields=fields))
    return query.to_dict()
