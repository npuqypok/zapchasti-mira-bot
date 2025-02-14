import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Session, sessionmaker


@dataclass
class RepositoryDTO:
    """
    Представляет объект передачи данных (DTO).

    Этот класс служит базовым DTO для обмена данными между слоями приложения.
    Он содержит метод `to_dict()`, который преобразует объект в словарь, используя функцию `asdict`.
    """

    def to_dict(self) -> dict[str, Any]:
        """
        Преобразует объект DTO в словарь.

        Returns:
            dict[str, Any]: Словарь, представляющий DTO.
        """
        return asdict(self)


T = TypeVar("T", bound=RepositoryDTO)


class BaseRepository(Generic[T], ABC):
    """
    Абстрактный базовый класс для репозиториев.

    Этот класс определяет интерфейс для всех репозиториев, которые работают с моделями базы данных.
    Он обеспечивает базовые методы для получения, создания, обновления и удаления элементов.

    Attributes:
        sessionmaker (sessionmaker[Session]): Фабрика сессий SQLAlchemy.

    Methods:
        get_by_id(item_id: str) -> T | None: Получает элемент по его ID.
        get_all(query: str) -> tuple[list[T], int]: Получает все элементы по запросу.
        create(item: T) -> None: Создает новый элемент.
        update(item_id: str, item: T) -> None: Обновляет существующий элемент.
        delete(item_id: str) -> None: Удаляет элемент по его ID.
        generate_uuid() -> str: Генерирует новый UUID.
    """

    def __init__(self, sessionmaker: sessionmaker[Session]):
        """
        Инициализирует репозиторий.

        Args:
            sessionmaker (sessionmaker[Session]): Фабрика сессий SQLAlchemy.
        """
        self.sessionmaker = sessionmaker

    @abstractmethod
    def get_by_id(self, item_id: str) -> T | None:
        """
        Получает элемент по его ID.

        Args:
            item_id (str): ID элемента.

        Returns:
            T | None: Элемент, если найден, иначе None.
        """
        ...

    @abstractmethod
    def get_all(self, query: str) -> tuple[list[T], int]:
        """
        Получает все элементы по запросу.

        Args:
             query (str): Запрос для фильтрации элементов.

        Returns:
             tuple[list[T], int]: Список элементов и общее количество элементов, соответствующих запросу.
        """
        ...

    @abstractmethod
    def create(self, item: T) -> None:
        """
        Создает новый элемент.

        Args:
            item (T): Объект DTO для создания.
        """
        ...

    @abstractmethod
    def update(self, item_id: str, item: T) -> None:
        """
        Обновляет существующий элемент.

        Args:
            item_id (str): ID элемента для обновления.
            item (T): Объект DTO с новыми данными.
        """
        ...

    @abstractmethod
    def delete(self, item_id: str) -> None:
        """
        Удаляет элемент по его ID.

        Args:
            item_id (str): ID элемента для удаления.
        """
        ...

    @staticmethod
    def generate_uuid() -> str:
        """
        Генерирует новый UUID.

        Returns:
            str: Строка, представляющая UUID.
        """
        return str(uuid.uuid4())
