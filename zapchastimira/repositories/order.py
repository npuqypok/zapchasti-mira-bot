from dataclasses import dataclass
import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass
class OrderDTO(RepositoryDTO):
    order_id: str
    user_id: str | None = None
    status: str


class OrderRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> OrderDTO | None:
        stmt = sa.select(tables.Order).where(tables.Order.order_id == item_id)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return OrderDTO(
                order_id=result.order_id, user_id=result.user_id, status=result.status
            )

    def get_all(self) -> tuple[list[OrderDTO], int]:  # получение всех заказов
        stmt = sa.select(tables.Order)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            results = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                OrderDTO(
                    order_id=result.order_id,
                    user_id=result.user_id,
                    status=result.status,
                )
                for result in results
            ], total

    def create(self, order_dto: OrderDTO) -> None:  # создание нового заказа
        new_order = tables.Order(user_id=order_dto.user_id, status=order_dto.status)

        with self.sessionmaker.begin() as session:
            session.add(new_order)
            return None

    def update(
        self, item_id: str, order_dto: OrderDTO
    ) -> None:  # обновление существующего заказа
        stmt = sa.select(tables.Order).where(tables.Order.order_id == item_id)

        with self.sessionmaker() as session:
            order = session.execute(stmt).scalar_one_or_none()
            if order is None:
                return None

            order.user_id = order_dto.user_id
            order.status = order_dto.status

    def delete(self, item_id: str) -> None:  # удаление заказа
        stmt = sa.delete(tables.Order).where(tables.Order.order_id == item_id)

        with self.sessionmaker.begin() as session:
            session.execute(stmt)
