from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from zapchastimira.common.settings import PostgresSettings


def get_sessionmaker() -> sessionmaker[Session]:
    """
    Создает фабрику сессий SQLAlchemy для подключения к базе данных PostgreSQL.

    Эта функция использует настройки подключения из `PostgresSettings` и
    создает движок SQLAlchemy. Затем она создает `sessionmaker`,
    который используется для создания сессий базы данных.

    Returns:
        sessionmaker[Session]: Фабрика сессий, готовая для создания новых сессий.
    """
    db_settings = PostgresSettings()
    engine = create_engine(db_settings.dsn)
    return sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """
    Создает и возвращает сессию базы данных SQLAlchemy.

    Эта функция использует `get_sessionmaker` для создания сессии базы данных.
    Сессия возвращается в контексте генератора, что позволяет использовать ее в
    блоке `with`, обеспечивая автоматическое закрытие сессии после использования.
    """
    db = get_sessionmaker()()
    try:
        yield db
    finally:
        db.close()
