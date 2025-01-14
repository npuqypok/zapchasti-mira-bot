from dataclasses import dataclass
import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass
class OrderItemDTO(RepositoryDTO):
    order_item_id: str
    order_id: str
    product_id: str
    quantity: int


class OrderItemRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> OrderItemDTO | None:
        stmt = sa.select(tables.OrderItem).where(
            tables.OrderItem.order_item_id == item_id
        )

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return OrderItemDTO(
                order_item_id=result.order_item_id,
                order_id=result.order_id,
                product_id=result.product_id,
                quantity=result.quantity,
            )

    def get_all(
        self,
    ) -> tuple[list[OrderItemDTO], int]:  # получение всех элементов заказа
        stmt = sa.select(tables.OrderItem)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            results = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                OrderItemDTO(
                    order_item_id=result.order_item_id,
                    order_id=result.order_id,
                    product_id=result.product_id,
                    quantity=result.quantity,
                )
                for result in results
            ], total

    def create(
        self, order_item_dto: OrderItemDTO
    ) -> None:  # создание нового элемента заказа
        new_order_item = tables.OrderItem(
            order_id=order_item_dto.order_id,
            product_id=order_item_dto.product_id,
            quantity=order_item_dto.quantity,
        )

        with self.sessionmaker.begin() as session:
            session.add(new_order_item)
            return None

    def update(
        self, item_id: str, order_item_dto: OrderItemDTO
    ) -> None:  # обновление существующего элемента заказа
        stmt = sa.select(tables.OrderItem).where(
            tables.OrderItem.order_item_id == item_id
        )

        with self.sessionmaker() as session:
            order_item = session.execute(stmt).scalar_one_or_none()
            if order_item is None:
                return None

            order_item.order_id = order_item_dto.order_id
            order_item.product_id = order_item_dto.product_id
            order_item.quantity = order_item_dto.quantity

    def delete(self, item_id: str) -> None:  # удаление элемента заказа
        stmt = sa.delete(tables.OrderItem).where(
            tables.OrderItem.order_item_id == item_id
        )

        with self.sessionmaker.begin() as session:
            session.execute(stmt)
