import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import sqlalchemy as sa


class Base(DeclarativeBase):
    created_at : Mapped[datetime.datetime] = mapped_column(server_default=sa.func.now())
    updated_at : Mapped[datetime.datetime] = mapped_column(server_default=sa.func.now(), onupdate=sa.func.now())


class User(Base):
    """
    Определяем класс User, который наследует от класса Base. Это означает, что все атрибуты этого класса будут автоматически сопоставлены с колонками в таблице базы данных.
    """
    __tablename__ = "user" # указываем имя таблицы в базе данных, соответствующей этой модели.
    user_id: Mapped[str] = mapped_column(primary_key=True) # это поле является первичным ключом таблицы.
    phone: Mapped[str] = mapped_column(unique=True)
    tg_uid: Mapped[str | None]

    orders: Mapped[list['Order']] = relationship("Order", back_populates="user") # Используется relationship для определения связей между сущностями (например, один пользователь может иметь много заказов).
    cart_items: Mapped[list['CartItem']] = relationship("CartItem", back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    category_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

    products: Mapped[list['Product']] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[float]
    stock_quantity: Mapped[int]
    category_id: Mapped[int] = mapped_column(sa.ForeignKey('categories.category_id'))

    category: Mapped[Category] = relationship("Category", back_populates="products")
    order_items: Mapped[list['OrderItem']] = relationship("OrderItem", back_populates="product")
    cart_items: Mapped[list['CartItem']] = relationship("CartItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(sa.ForeignKey('user.user_id'))
    order_date: Mapped[datetime.datetime] = mapped_column(default=sa.func.now())
    status: Mapped[str]

    user: Mapped[User] = relationship("User", back_populates="orders")
    order_items: Mapped[list['OrderItem']] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id: Mapped[str] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(sa.ForeignKey('orders.order_id'))
    product_id: Mapped[str] = mapped_column(sa.ForeignKey('products.product_id'))
    quantity: Mapped[int]

    order: Mapped[Order] = relationship("Order", back_populates="order_items")
    product: Mapped[Product] = relationship("Product", back_populates="order_items")


class CartItem(Base):
    __tablename__ = "cart_items"
    cart_item_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(sa.ForeignKey('user.user_id'))
    product_id: Mapped[str] = mapped_column(sa.ForeignKey('products.product_id'))
    quantity: Mapped[int]

    user: Mapped[User] = relationship("User", back_populates="cart_items")
    product: Mapped[Product] = relationship("Product", back_populates="cart_items")
