from elasticsearch_dsl import Keyword, Text

from testdata.schemas.base import Mappings, Settings


class Person(Mappings):
    """Класс структуры документа с данными о персоне."""

    full_name = Text(analyzer='ru_en', fields={'raw': Keyword()})

    class Index(Settings):
        name = 'persons'
