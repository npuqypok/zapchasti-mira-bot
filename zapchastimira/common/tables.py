import datetime
from enum import StrEnum

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=sa.func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=sa.func.now(), onupdate=sa.func.now())


class UserStateEnum(StrEnum):
    START = "start"
    SEARCH = "search"


class User(Base):
    __tablename__ = "user"
    user_id: Mapped[str] = mapped_column(primary_key=True)
    phone: Mapped[str | None]
    tg_uid: Mapped[str | None]
    state: Mapped[UserStateEnum] = mapped_column(sa.String)


class UserCars(Base):
    __tablename__ = "user_cars"

    car_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(sa.ForeignKey("user.user_id"))
    make: Mapped[str]
    model: Mapped[str]
    year: Mapped[int]
    color: Mapped[str | None] = mapped_column(sa.String(50))


class Category(Base):
    __tablename__ = "categories"
    category_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]


class ProductCategory(Base):
    __tablename__ = "product_category"
    category_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    base_categoty_id: Mapped[str] = mapped_column(sa.ForeignKey("categories.category_id"))
    # search_vector: Mapped[TSVECTOR] = mapped_column(TSVECTOR)


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[float]
    stock_quantity: Mapped[int]
    page_url: Mapped[str]
    search_vector: Mapped[TSVECTOR] = mapped_column(TSVECTOR)

    category_id: Mapped[str] = mapped_column(sa.ForeignKey("product_category.category_id"))


class PartCategory(Base):
    __tablename__ = "part_category"
    category_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    base_categoty_id: Mapped[str] = mapped_column(sa.ForeignKey("categories.category_id"))
    # search_vector: Mapped[TSVECTOR] = mapped_column(TSVECTOR)


class Part(Base):
    __tablename__ = "parts"
    part_id: Mapped[str] = mapped_column(primary_key=True)
    part_number: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[str | None]
    brand: Mapped[str]
    compatibility: Mapped[str | None]
    price: Mapped[float]
    stock_quantity: Mapped[int]
    image_url: Mapped[str | None]
    search_vector: Mapped[TSVECTOR] = mapped_column(TSVECTOR)

    category_id: Mapped[str] = mapped_column(sa.ForeignKey("part_category.category_id"))


class Contact(Base):
    __tablename__ = "contacts"
    contact_id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    position: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str | None]
    description: Mapped[str | None]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=sa.func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=sa.func.now(), onupdate=sa.func.now())
