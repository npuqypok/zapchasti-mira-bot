from dataclasses import dataclass
import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.common.db_utils import get_sessionmaker
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass(kw_only=True)
class ProductDTO(RepositoryDTO):
    product_id: str | None = None
    name: str
    price: float
    stock_quantity: int
    category_id: str | None = None
    description: str | None = None
    page_url: str


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
                page_url=result.page_url,
            )

    def get_all(self, query: str) -> tuple[list[ProductDTO], int]:
        tsquery = " & ".join(query.split())
        stmt = sa.select(tables.Product).where(
            tables.Product.search_vector.op("@@")(sa.func.to_tsquery("simple", tsquery))
        )

        with self.sessionmaker() as session:
            results = session.execute(stmt).scalars().all()

            return [
                ProductDTO(
                    product_id=result.product_id,
                    name=result.name,
                    description=result.description,
                    price=result.price,
                    stock_quantity=result.stock_quantity,
                    category_id=result.category_id,
                    page_url=result.page_url,
                )
                for result in results
            ], len(results)

    def create(self, product_dto: ProductDTO) -> None:
        new_product = tables.Product(
            name=product_dto.name,
            description=product_dto.description,
            price=product_dto.price,
            stock_quantity=product_dto.stock_quantity,
            category_id=product_dto.category_id,
            page_url=product_dto.page_url,
        )

        with self.sessionmaker.begin() as session:
            session.add(new_product)
            return None

    def update(self, item_id: str, product_dto: ProductDTO) -> None:
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
            product.page_url = product_dto.page_url

    def delete(self, item_id: str) -> None:
        stmt = sa.delete(tables.Product).where(tables.Product.product_id == item_id)

        with self.sessionmaker.begin() as session:
            session.execute(stmt)


product_repository = ProductRepository(sessionmaker=get_sessionmaker())
