from dataclasses import (
    dataclass,
)  # Используется для упрощения создания классов, которые в основном хранят данные.
import datetime
import sqlalchemy as sa

from zapchastimira.common import tables  # Импортируем таблицы
from zapchastimira.common.db_utils import (
    get_sessionmaker,
)  # Импортируем функцию для получения sessionmaker
from zapchastimira.repositories.base import (
    BaseRepository,
    RepositoryDTO,
)  # Импортируем базовый репозиторий


@dataclass
class PartDTO(RepositoryDTO):
    part_id: str
    part_number: str
    name: str
    description: str | None = None
    brand: str
    compatibility: str | None = None
    price: float
    stock_quantity: int
    image_url: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class PartRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> PartDTO | None:
        stmt = sa.select(tables.Part).where(tables.Part.part_id == item_id)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return PartDTO(
                part_id=result.part_id,
                part_number=result.part_number,
                name=result.name,
                description=result.description,
                brand=result.brand,
                compatibility=result.compatibility,
                price=result.price,
                stock_quantity=result.stock_quantity,
                image_url=result.image_url,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )

    def get_all(self) -> tuple[list[PartDTO], int]:
        stmt = sa.select(tables.Part)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            res = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                PartDTO(
                    part_id=i.part_id,
                    part_number=i.part_number,
                    name=i.name,
                    description=i.description,
                    brand=i.brand,
                    compatibility=i.compatibility,
                    price=i.price,
                    stock_quantity=i.stock_quantity,
                    image_url=i.image_url,
                    created_at=i.created_at,
                    updated_at=i.updated_at,
                )
                for i in res
            ], total

    def create(self, item: PartDTO) -> None:
        tmp = tables.Part(
            part_id=item.part_id or self.generate_uuid(),
            part_number=item.part_number,
            name=item.name,
            description=item.description,
            brand=item.brand,
            compatibility=item.compatibility,
            price=item.price,
            stock_quantity=item.stock_quantity,
            image_url=item.image_url,
        )

        with self.sessionmaker.begin() as session:
            session.add(tmp)

    def update(self, item_id: str, item: PartDTO) -> None:
        stmt = sa.select(tables.Part).where(tables.Part.part_id == item_id)

        with self.sessionmaker.begin() as session:
            part = session.execute(stmt).scalar_one_or_none()
            if part is None:
                return None

            part.part_number = item.part_number
            part.name = item.name
            part.description = item.description
            part.brand = item.brand
            part.compatibility = item.compatibility
            part.price = item.price
            part.stock_quantity = item.stock_quantity
            part.image_url = item.image_url

    def delete(self, item_id: str) -> None:
        stmt = sa.delete(tables.Part).where(tables.Part.part_id == item_id)
        with self.sessionmaker.begin() as session:
            session.execute(stmt)


# Создание экземпляра репозитория для использования в приложении.
part_repository = PartRepository(sessionmaker=get_sessionmaker())
