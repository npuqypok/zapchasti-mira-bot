from dataclasses import dataclass # используется для упрощения создания классов, которые в основном хранят данные.
import datetime
import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.common.db_utils import get_sessionmaker
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass
class UserDTO(RepositoryDTO):
    phone: str
    user_id: str | None = None
    tg_uid: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class UserRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> UserDTO | None: # получает пользователя по его уникальному идентификатору (item_id).
        stmt = sa.select(tables.User).where(tables.User.user_id == item_id) # запрос на выборку пользователя из таблицы User, где поле user_id соответствует переданному идентификатору.

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none() # выполняет SQL-запрос.
            if result is None:
                return None
            return UserDTO(phone=result.phone, user_id=result.user_id, tg_uid=result.tg_uid, created_at=result.created_at, updated_at=result.updated_at)

    def get_all(self) -> tuple[list[UserDTO], int]:
        stmt = sa.select(tables.User)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            res = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [UserDTO(phone=i.phone, user_id=i.user_id, tg_uid=i.tg_uid, created_at=i.created_at, updated_at=i.updated_at) for i in res], total

    def create(self, item: UserDTO) -> None:
        tmp = tables.User(
            user_id=item.user_id or self.generate_uuid(),
            phone=item.phone,
            tg_uid=item.tg_uid
        )

        with self.sessionmaker.begin() as session:
            session.add(tmp)
    
    def update(self, item_id: str, item: UserDTO) -> None:
        stmt = sa.select(tables.User).where(tables.User.user_id == item_id)

        with self.sessionmaker.begin() as session:
            user = session.execute(stmt).scalar_one_or_none()
            if user is None:
                return None
            user.phone = item.phone
            user.tg_uid = item.tg_uid

    def delete(self, item_id: str) -> None:
        stmt = sa.delete(tables.User).where(tables.User.user_id == item_id)
        with self.sessionmaker.begin() as session:
            session.execute(stmt)


user_repository = UserRepository(sessionmaker=get_sessionmaker())
# tmp = UserDTO(phone="89139911234", tg_uid="ssasq")
# user_repository.create(tmp)

print(user_repository.get_all())

tmp = user_repository.get_by_id("e17e25c7-f8ec-4912-95b3-8b63ef960658")
print(tmp)
tmp.tg_uid = "qwerr"
user_repository.update("e17e25c7-f8ec-4912-95b3-8b63ef960658", tmp)

tmp = user_repository.get_by_id("e17e25c7-f8ec-4912-95b3-8b63ef960658")
print(tmp)

user_repository.delete("e17e25c7-f8ec-4912-95b3-8b63ef960658")
tmp = user_repository.get_by_id("e17e25c7-f8ec-4912-95b3-8b63ef960658")
print(tmp)

