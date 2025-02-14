import datetime
from dataclasses import dataclass

import sqlalchemy as sa

from zapchastimira.common import tables
from zapchastimira.common.db_utils import get_sessionmaker
from zapchastimira.repositories.base import BaseRepository, RepositoryDTO


@dataclass
class ContactDTO(RepositoryDTO):
    contact_id: str
    first_name: str
    last_name: str
    position: str
    phone: str
    email: str | None = None
    description: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class ContactRepository(BaseRepository):
    def get_by_id(self, item_id: str) -> ContactDTO | None:
        stmt = sa.select(tables.Contact).where(tables.Contact.contact_id == item_id)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return ContactDTO(
                contact_id=result.contact_id,
                first_name=result.first_name,
                last_name=result.last_name,
                position=result.position,
                phone=result.phone,
                email=result.email,
                description=result.description,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )

    def get_all(self) -> tuple[list[ContactDTO], int]:
        stmt = sa.select(tables.Contact)
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        with self.sessionmaker() as session:
            res = session.execute(stmt).scalars().all()
            total = session.execute(total_stmt).scalar_one()
            return [
                ContactDTO(
                    contact_id=i.contact_id,
                    first_name=i.first_name,
                    last_name=i.last_name,
                    position=i.position,
                    phone=i.phone,
                    email=i.email,
                    description=i.description,
                    created_at=i.created_at,
                    updated_at=i.updated_at,
                )
                for i in res
            ], total

    def create(self, item: ContactDTO) -> None:
        tmp = tables.Contact(
            contact_id=item.contact_id or self.generate_uuid(),
            first_name=item.first_name,
            last_name=item.last_name,
            position=item.position,
            phone=item.phone,
            email=item.email,
            description=item.description,
        )

        with self.sessionmaker.begin() as session:
            session.add(tmp)

    def update(self, item_id: str, item: ContactDTO) -> None:
        stmt = sa.select(tables.Contact).where(tables.Contact.contact_id == item_id)

        with self.sessionmaker.begin() as session:
            contact = session.execute(stmt).scalar_one_or_none()
            if contact is None:
                return None
            contact.first_name = item.first_name
            contact.last_name = item.last_name
            contact.position = item.position
            contact.phone = item.phone
            contact.email = item.email
            contact.description = item.description

    def delete(self, item_id: str) -> None:
        stmt = sa.delete(tables.Contact).where(tables.Contact.contact_id == item_id)
        with self.sessionmaker.begin() as session:
            session.execute(stmt)

    def get_contact_by_phone(self, phone: str) -> ContactDTO | None:
        stmt = sa.select(tables.Contact).where(tables.Contact.phone == phone)

        with self.sessionmaker() as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                return None
            return ContactDTO(
                contact_id=result.contact_id,
                first_name=result.first_name,
                last_name=result.last_name,
                position=result.position,
                phone=result.phone,
                email=result.email,
                description=result.description,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )


contact_repository = ContactRepository(sessionmaker=get_sessionmaker())
