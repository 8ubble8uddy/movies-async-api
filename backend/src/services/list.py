from typing import List, Type

from services.base import BaseService, redis_cache
from services.mixins import QuerysetMixin, SingleObjectMixin
from core.config import CONFIG, CinemaObject, CinemaObjectList


class ListService(BaseService, SingleObjectMixin, QuerysetMixin):
    """Сервис для представления списка объектов кинотеатра."""

    model: Type[CinemaObjectList]

    @property
    def redis_key(self) -> str:
        """
        Ключ от данных в кэше Redis в виде индекса и параметров запроса в URL-адресе.

        Returns:
            str: Индекс и параметры разделённые двоеточиями
        """
        params = [
            f'{field}::{value}' for field, value in self.__repr_args__()
            if field in {'filter', 'page_number', 'page_size', 'query', 'sort'}
        ]
        return '{index}::{params}'.format(index=self.index, params='::'.join(params))

    @redis_cache(expire=CONFIG.fastapi.cache_expire_in_seconds)
    async def get(self) -> List[CinemaObject]:
        """
        Основной метод получения списка объектов кинотеатра.

        Returns:
            CinemaObjectList: Список объектов кинотеатра
        """
        queryset = await self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        data = await self.search_elastic_docs(self.index, page)
        obj_list = [
            await self.get_object(item, self.model.item) for item in data
        ]
        return obj_list
