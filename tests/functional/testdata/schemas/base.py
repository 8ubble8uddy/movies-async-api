from elasticsearch_dsl import Document, Keyword, MetaField, analyzer, token_filter


class Mappings(Document):
    """Класс базовой структуры документа для Elasticsearch."""

    id = Keyword()

    class Meta:
        dynamic = MetaField('strict')

    def to_dict(self) -> dict:
        """
        Сериализация документа в словарь для корректной загрузки данных через bulk-запрос.

        Returns:
            dict: Данные документа в удобном формате для загрузки
        """
        doc = super().to_dict(include_meta=True)
        doc['_id'] = self.id
        return doc


class Settings(object):
    """Класс настроек индекса для Elasticsearch."""

    settings = {'refresh_interval': '1s'}
    analyzers = [analyzer('ru_en', tokenizer='standard', filter=[
        'lowercase',
        token_filter('english_stop', 'stop', stopwords='_english_'),
        token_filter('english_stemmer', 'stemmer', language='english'),
        token_filter('english_possessive_stemmer', 'stemmer', language='possessive_english'),
        token_filter('russian_stop', 'stop', stopwords='_russian_'),
        token_filter('russian_stemmer', 'stemmer', language='russian'),
    ])]
