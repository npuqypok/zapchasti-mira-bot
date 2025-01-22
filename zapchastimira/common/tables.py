import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import sqlalchemy as sa


class Base(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=sa.func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=sa.func.now(), onupdate=sa.func.now()
    )


class User(Base):
    """
    Определяем класс User, который наследует от класса Base. Это означает, что все атрибуты этого класса будут автоматически сопоставлены с колонками в таблице базы данных.
    """

    __tablename__ = (
        "user"  # указываем имя таблицы в базе данных, соответствующей этой модели.
    )
    user_id: Mapped[str] = mapped_column(
        primary_key=True
    )  # это поле является первичным ключом таблицы.
    phone: Mapped[str] = mapped_column(unique=True)
    tg_uid: Mapped[str | None]


class UserCars(Base):
    __tablename__ = "user_cars"

    car_id: Mapped[str] = mapped_column(
        primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        sa.ForeignKey("user.user_id")
    )
    make: Mapped[str]
    model: Mapped[str]
    year: Mapped[int]
    color: Mapped[str | None] = mapped_column(
        sa.String(50)
    )


class Category(Base):
    __tablename__ = "categories"
    category_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )
    parts: Mapped[list["Part"]] = relationship(
        "Part", back_populates="category"
    )  # Обратное отношение


class ProductCategory(Base):
    __tablename__ = "product_category"
    category_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    base_categoty_id: Mapped[str] = mapped_column(sa.ForeignKey("categories.category_id"))

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )
    

class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[float]
    stock_quantity: Mapped[int]
    page_url: Mapped[str]

    category_id: Mapped[str] = mapped_column(sa.ForeignKey("product_category.category_id"))

    category: Mapped[ProductCategory] = relationship("ProductCategory", back_populates="products")


class PartCategory(Base):
    __tablename__ = "part_category"
    category_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    base_categoty_id: Mapped[str] = mapped_column(sa.ForeignKey("categories.category_id"))

    part: Mapped[list["Part"]] = relationship(
        "Part", back_populates="category"
    )

class Part(Base):
    __tablename__ = "parts"
    part_id: Mapped[str] = mapped_column(primary_key=True)
    part_number: Mapped[str] = mapped_column(unique=True)  # Уникальный код запчасти
    name: Mapped[str]
    description: Mapped[str | None]
    brand: Mapped[str]  # Бренд запчасти
    compatibility: Mapped[str | None]  # Совместимость с моделями
    price: Mapped[float]
    stock_quantity: Mapped[int]
    image_url: Mapped[str | None]  # Ссылка на изображение

    category_id: Mapped[str] = mapped_column(sa.ForeignKey("part_category.category_id"))

    category: Mapped[PartCategory] = relationship(
        "Category", back_populates="part"
    )  # Обратное отношение
