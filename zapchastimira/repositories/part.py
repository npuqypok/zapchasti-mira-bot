from dataclasses import (
    dataclass,
)
import datetime
import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.common.db_utils import (
    get_sessionmaker,
)
from zapchastimira.repositories.base import (
    BaseRepository,
    RepositoryDTO,
)


@dataclass(kw_only=True)
class PartDTO(RepositoryDTO):
    part_id: str
    part_number: str
    name: str
    description: str | None = None
    brand: str
    compatibility: str | None = None
    price: float
    stock_quantity: int
    page_url: str
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
                created_at=result.created_at,
                updated_at=result.updated_at,
                page_url=result.image_url,
            )

    def get_all(self, query: str) -> tuple[list[PartDTO], int]:
        tsquery = " & ".join(query.split())
        stmt = sa.select(tables.Part).where(
            tables.Part.search_vector.op("@@")(sa.func.to_tsquery("simple", tsquery))
        )
        with self.sessionmaker() as session:
            results = session.execute(stmt).scalars().all()
            return [
                PartDTO(
                    part_id=result.part_id,
                    part_number=result.part_number,
                    name=result.name,
                    description=result.description,
                    brand=result.brand,
                    compatibility=result.compatibility,
                    price=result.price,
                    stock_quantity=result.stock_quantity,
                    created_at=result.created_at,
                    updated_at=result.updated_at,
                    page_url=result.image_url,
                )
                for result in results
            ], len(results)

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
            image_url=item.page_url,
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
            part.image_url = item.page_url

    def delete(self, item_id: str) -> None:
        stmt = sa.delete(tables.Part).where(tables.Part.part_id == item_id)
        with self.sessionmaker.begin() as session:
            session.execute(stmt)


part_repository = PartRepository(sessionmaker=get_sessionmaker())
