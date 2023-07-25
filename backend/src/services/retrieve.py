from typing import Optional, Type
from uuid import UUID

from services.base import BaseService, redis_cache
from services.mixins import SingleObjectMixin
from core.config import CONFIG, CinemaObject


class RetrieveService(BaseService, SingleObjectMixin):
    """Сервис для представления объекта кинотеатра по ID."""

    model: Type[CinemaObject]
    id: Optional[UUID]

    @property
    def redis_key(self) -> str:
        """
        Ключ от данных в кэше Redis в виде индекса и ID запрашиваемого документа.

        Returns:
            str: Индекс и ID разделённые двоеточиями
        """
        return '{index}::id::{id}'.format(index=self.index, id=self.id)

    @redis_cache(expire=CONFIG.fastapi.cache_expire_in_seconds)
    async def get(self) -> CinemaObject:
        """
        Основной метод получения одного объекта кинотеатра.

        Returns:
            CinemaObject: Объект кинотеатра
        """
        data = await self.get_elastic_doc(self.index, self.id)
        obj = await self.get_object(data, self.model)
        return obj
