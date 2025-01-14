from dataclasses import dataclass
import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass
class CartItemDTO(RepositoryDTO):
    cart_item_id: str
    user_id: str | None = None
    product_id: str | None = None
    quantity: int


class CartItemRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> CartItemDTO | None:
        stmt = sa.select(tables.CartItem).where(tables.CartItem.cart_item_id == item_id)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return CartItemDTO(
                cart_item_id=result.cart_item_id,
                user_id=result.user_id,
                product_id=result.product_id,
                quantity=result.quantity,
            )

    def get_all(
        self,
    ) -> tuple[list[CartItemDTO], int]:  # получение всех элементов корзины
        stmt = sa.select(tables.CartItem)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            results = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                CartItemDTO(
                    cart_item_id=result.cart_item_id,
                    user_id=result.user_id,
                    product_id=result.product_id,
                    quantity=result.quantity,
                )
                for result in results
            ], total

    def create(
        self, cart_item_dto: CartItemDTO
    ) -> None:  # создание нового элемента корзины
        new_cart_item = tables.CartItem(
            user_id=cart_item_dto.user_id,
            product_id=cart_item_dto.product_id,
            quantity=cart_item_dto.quantity,
        )

        with self.sessionmaker.begin() as session:
            session.add(new_cart_item)
            return None

    def update(
        self, item_id: str, cart_item_dto: CartItemDTO
    ) -> None:  # обновление существующего элемента корзины
        stmt = sa.select(tables.CartItem).where(tables.CartItem.cart_item_id == item_id)

        with self.sessionmaker() as session:
            cart_item = session.execute(stmt).scalar_one_or_none()
            if cart_item is None:
                return None

            cart_item.user_id = cart_item_dto.user_id
            cart_item.product_id = cart_item_dto.product_id
            cart_item.quantity = cart_item_dto.quantity

    def delete(self, item_id: str) -> None:  # удаление элемента корзины
        stmt = sa.delete(tables.CartItem).where(tables.CartItem.cart_item_id == item_id)

        with self.sessionmaker.begin() as session:
            session.execute(stmt)
