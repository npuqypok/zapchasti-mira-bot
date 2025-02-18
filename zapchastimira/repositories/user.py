import datetime
from dataclasses import dataclass

import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.common.db_utils import get_sessionmaker
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass(kw_only=True)
class UserDTO(RepositoryDTO):
    phone: str | None = None
    user_id: str | None = None
    tg_uid: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    state: tables.UserStateEnum


class UserRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> UserDTO | None:
        stmt = sa.select(tables.User).where(tables.User.user_id == item_id)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return UserDTO(
                phone=result.phone,
                user_id=result.user_id,
                tg_uid=result.tg_uid,
                created_at=result.created_at,
                updated_at=result.updated_at,
                state=result.state,
            )

    def get_all(self) -> tuple[list[UserDTO], int]:
        stmt = sa.select(tables.User)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            res = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                UserDTO(
                    phone=i.phone,
                    user_id=i.user_id,
                    tg_uid=i.tg_uid,
                    created_at=i.created_at,
                    updated_at=i.updated_at,
                    state=i.state,
                )
                for i in res
            ], total

    def create(self, item: UserDTO) -> None:
        tmp = tables.User(
            user_id=item.user_id or self.generate_uuid(),
            phone=item.phone,
            tg_uid=item.tg_uid,
            state=item.state,
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

    def set_state(self, user_id: str, state: tables.UserStateEnum) -> None:
        stmt = sa.update(tables.User).where(tables.User.user_id == user_id).values(state=state)

        with self.sessionmaker.begin() as session:
            session.execute(stmt)

    def delete(self, item_id: str) -> None:
        stmt = sa.delete(tables.User).where(tables.User.user_id == item_id)
        with self.sessionmaker.begin() as session:
            session.execute(stmt)

    def get_user_by_phone(self, phone: str) -> UserDTO | None:
        stmt = sa.select(tables.User).where(tables.User.phone == phone)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
        return UserDTO(
            phone=result.phone,
            user_id=result.user_id,
            tg_uid=result.tg_uid,
            created_at=result.created_at,
            updated_at=result.updated_at,
            state=result.state,
        )

    def get_user_by_telegram_id(self, tg_uid: str) -> UserDTO | None:
        stmt = sa.select(tables.User).where(tables.User.tg_uid == tg_uid)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
        return UserDTO(
            phone=result.phone,
            user_id=result.user_id,
            tg_uid=result.tg_uid,
            created_at=result.created_at,
            updated_at=result.updated_at,
            state=result.state,
        )


user_repository = UserRepository(sessionmaker=get_sessionmaker())
