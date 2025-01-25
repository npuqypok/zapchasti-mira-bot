from dataclasses import asdict, dataclass # используются для создания классов данных (DTO) и преобразования их в словари.
from typing import Any, Generic, TypeVar # используются для создания обобщенных классов и типов.
from abc import ABC, abstractmethod # используются для создания абстрактных базовых классов и определения абстрактных методов.
from sqlalchemy.orm import Session, sessionmaker # используются для работы с сессиями SQLAlchemy.
import uuid

@dataclass
class RepositoryDTO:
    """
    представляет объект передачи данных (DTO). Он содержит метод to_dict(), который преобразует объект в словарь, используя функцию asdict
    """
    def to_dict(self) -> dict[str, Any]:
	    return asdict(self)
    
T = TypeVar("T", bound=RepositoryDTO)


class BaseRepository(Generic[T], ABC):
    def __init__(self, sessionmaker: sessionmaker[Session]):
        self.sessionmaker = sessionmaker

    @abstractmethod
    def get_by_id(self, item_id: str) -> T | None: ...

    @abstractmethod
    def get_all(self, query: str) -> tuple[list[T], int]: ...

    @abstractmethod
    def create(self, item: T) -> None: ...

    @abstractmethod
    def update(self, item_id: str, item: T) -> None: ...

    @abstractmethod
    def delete(self, item_id: str) -> None: ...

    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())
