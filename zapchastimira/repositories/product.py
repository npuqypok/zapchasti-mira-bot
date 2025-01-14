from dataclasses import dataclass
import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass
class ProductDTO(RepositoryDTO):
    product_id: str | None = None
    name: str
    description: str | None = None
    price: float
    stock_quantity: int
    category_id: str | None = None


class ProductRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> ProductDTO | None:
        stmt = sa.select(tables.Product).where(tables.Product.product_id == item_id)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return ProductDTO(
                product_id=result.product_id,
                name=result.name,
                description=result.description,
                price=result.price,
                stock_quantity=result.stock_quantity,
                category_id=result.category_id,
            )

    def get_all(self) -> tuple[list[ProductDTO], int]:  # получение всех продуктов
        stmt = sa.select(tables.Product)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            results = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                ProductDTO(
                    product_id=result.product_id,
                    name=result.name,
                    description=result.description,
                    price=result.price,
                    stock_quantity=result.stock_quantity,
                    category_id=result.category_id,
                )
                for result in results
            ], total

    def create(self, product_dto: ProductDTO) -> None:  # cоздание нового продукта
        new_product = tables.Product(
            name=product_dto.name,
            description=product_dto.description,
            price=product_dto.price,
            stock_quantity=product_dto.stock_quantity,
            category_id=product_dto.category_id,
        )

        with self.sessionmaker.begin() as session:
            session.add(new_product)
            return None

    def update(
        self, item_id: str, product_dto: ProductDTO
    ) -> None:  # обновление существующего продукта
        stmt = sa.select(tables.Product).where(tables.Product.product_id == item_id)

        with self.sessionmaker() as session:
            product = session.execute(stmt).scalar_one_or_none()
            if product is None:
                return None

            product.name = product_dto.name
            product.description = product_dto.description
            product.price = product_dto.price
            product.stock_quantity = product_dto.stock_quantity
            product.category_id = product_dto.category_id

    def delete(self, item_id: str) -> None:  # удаление продукта
        stmt = sa.delete(tables.Product).where(tables.Product.product_id == item_id)

        with self.sessionmaker.begin() as session:
            session.execute(stmt)
