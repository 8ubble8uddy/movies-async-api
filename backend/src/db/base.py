from pydantic import BaseModel


class DatabaseModel(BaseModel):
    """Базовый класс для работы с хранилищем."""

    class Config:
        """Настройки валидации."""

        arbitrary_types_allowed = True
