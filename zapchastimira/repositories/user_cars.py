from dataclasses import dataclass
import sqlalchemy as sa

from zapchastimira.common import tables  # Импортируем таблицы
from zapchastimira.common.db_utils import get_sessionmaker
from zapchastimira.repositories.base import (
    BaseRepository,
    RepositoryDTO,
)  # Импортируем базовый репозиторий


@dataclass
class UserCarDTO(RepositoryDTO):
    car_id: str | None = None
    user_id: str  # ID пользователя, которому принадлежит автомобиль
    make: str  # Производитель автомобиля
    model: str  # Модель автомобиля
    year: int  # Год выпуска автомобиля
    color: str | None = None  # Цвет автомобиля


class UserCarsRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> UserCarDTO | None:
        stmt = sa.select(tables.UserCars).where(tables.UserCars.car_id == item_id)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return UserCarDTO(
                car_id=result.car_id,
                user_id=result.user_id,
                make=result.make,
                model=result.model,
                year=result.year,
                color=result.color,
            )

    def get_all(self) -> tuple[list[UserCarDTO], int]:
        stmt = sa.select(tables.UserCars)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            results = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                UserCarDTO(
                    car_id=result.car_id,
                    user_id=result.user_id,
                    make=result.make,
                    model=result.model,
                    year=result.year,
                    color=result.color,
                )
                for result in results
            ], total

    def create(self, user_car_dto: UserCarDTO) -> None:
        new_user_car = tables.UserCars(
            car_id=user_car_dto.car_id or self.generate_uuid(),
            user_id=user_car_dto.user_id,
            make=user_car_dto.make,
            model=user_car_dto.model,
            year=user_car_dto.year,
            color=user_car_dto.color,
        )

        with self.sessionmaker.begin() as session:
            session.add(new_user_car)

    def update(self, item_id: str, user_car_dto: UserCarDTO) -> None:
        stmt = sa.select(tables.UserCars).where(tables.UserCars.car_id == item_id)

        with self.sessionmaker() as session:
            user_car = session.execute(stmt).scalar_one_or_none()
            if user_car is None:
                return

            user_car.user_id = user_car_dto.user_id
            user_car.make = user_car_dto.make
            user_car.model = user_car_dto.model
            user_car.year = user_car_dto.year
            user_car.color = user_car_dto.color

    def delete(self, item_id: str) -> None:
        stmt = sa.delete(tables.UserCars).where(tables.UserCars.car_id == item_id)

        with self.sessionmaker.begin() as session:
            session.execute(stmt)


# Создание экземпляра репозитория для использования в приложении.
user_cars_repository = UserCarsRepository(sessionmaker=get_sessionmaker())
