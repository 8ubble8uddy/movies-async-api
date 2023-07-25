from typing import Iterator, List, Union

from faker import Faker

from testdata.schemas.genre import Genre
from testdata.schemas.person import Person
from testdata.schemas.movie import PersonInMovie, Movie
from conftest import GENRES, MOVIES_PER_GENRE, ACTORS_PER_MOVIE, WRITERS_PER_MOVIE


class ElasticDocsFactory:
    """Класс для генерации документов Elasticsearch."""

    SCHEMAS = Movie, Person, Genre

    def __init__(self) -> None:
        """При инициализации класса создается объект для генерации фейковых данных."""
        self.fake = Faker()

    @property
    def fake_movie_person(self) -> PersonInMovie:
        """
        Документ персоны в фильме.

        Returns:
            PersonInMovie: Документ персоны в фильме
        """
        return PersonInMovie(id=self.fake.uuid4(), name=self.fake.name())

    def get_movies(self, genre: Genre) -> Iterator[Movie]:
        """
        Генерирует фильмы с жанром в виде документов.

        Args:
            genre: Жанр

        Yields:
            Movie: Документ фильма
        """
        for _ in range(MOVIES_PER_GENRE):
            actors = [self.fake_movie_person for _ in range(ACTORS_PER_MOVIE)]
            writers = [self.fake_movie_person for _ in range(WRITERS_PER_MOVIE)]
            yield Movie(
                id=self.fake.uuid4(),
                imdb_rating=self.fake.pyfloat(positive=True, right_digits=1, max_value=10),
                genre=[genre.name],
                title=' '.join(word.capitalize() for word in self.fake.words()),
                description=self.fake.text(),
                director=[self.fake.name()],
                actors_names=[actor.name for actor in actors],
                writers_names=[writer.name for writer in writers],
                actors=actors,
                writers=writers,
            )

    def get_persons(self, movie: Movie) -> Iterator[Person]:
        """
        Генерирует персоны из фильма в виде документов.

        Args:
            movie: Фильм

        Yields:
            Person: Документ персоны
        """
        for person in sum([list(movie.actors), list(movie.writers)], []):
            yield Person(id=person.id, full_name=person.name)
        yield Person(id=self.fake.uuid4(), full_name=movie.director[0])

    def get_genres(self, genres_names: List[str]) -> Iterator[Genre]:
        """
        Генерирует жанры в виде документов.

        Args:
            genres_names: Названия жанров

        Yields:
            Genre: Документ жанра
        """
        for name in genres_names:
            yield Genre(id=self.fake.uuid4(), name=name, description=self.fake.text())

    def gendata(self) -> Iterator[Union[Movie, Person, Genre]]:
        """
        Основной метод генерации документов Elasticsearch.

        Yields:
            Movie | Person | Genre: Фейковые документы кинотеатра
        """
        for genre in self.get_genres(GENRES):
            for movie in self.get_movies(genre):
                yield genre
                yield movie
                yield from self.get_persons(movie)
