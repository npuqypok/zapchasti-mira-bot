from dataclasses import dataclass
import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass
class CategoryDTO(RepositoryDTO):
    category_id: str | None = None
    name: str
    description: str | None = None


class CategoryRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> CategoryDTO | None:
        stmt = sa.select(tables.Category).where(tables.Category.category_id == item_id)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return CategoryDTO(
                category_id=result.category_id,
                name=result.name,
                description=result.description,
            )

    def get_all(self) -> tuple[list[CategoryDTO], int]:
        stmt = sa.select(tables.Category)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            results = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                CategoryDTO(
                    category_id=result.category_id,
                    name=result.name,
                    description=result.description,
                )
                for result in results
            ], total

    def create(self, category_dto: CategoryDTO) -> None:
        new_category = tables.Category(
            name=category_dto.name, description=category_dto.description
        )

        with self.sessionmaker.begin() as session:
            session.add(new_category)
            return None

    def update(self, item_id: str, category_dto: CategoryDTO) -> None:
        stmt = sa.select(tables.Category).where(tables.Category.category_id == item_id)

        with self.sessionmaker() as session:
            category = session.execute(stmt).scalar_one_or_none()
            if category is None:
                return None

            category.name = category_dto.name
            category.description = category_dto.description

    def delete(self, item_id: str) -> None:
        stmt = sa.delete(tables.Category).where(tables.Category.category_id == item_id)

        with self.sessionmaker.begin() as session:
            session.execute(stmt)
