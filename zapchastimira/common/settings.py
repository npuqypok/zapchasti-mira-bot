from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLiteSettings(BaseSettings):
    """
    Настройки для подключения к базе данных SQLite.

    Этот класс использует pydantic для загрузки настроек из переменных окружения и файла `.env`.
    Он определяет имя файла базы данных и формирует строку подключения (DSN).

    Attributes:
        db_name (str): Имя файла базы данных SQLite.

    Properties:
        dsn (str): Строка подключения к базе данных SQLite.
    """

    model_config = SettingsConfigDict(
        env_prefix="SQLITE_", extra="ignore", env_file=".env"
    )
    db_name: str

    @property
    def dsn(self) -> str:
        """
        Генерирует строку подключения к базе данных SQLite.

        Returns:
          str: строка подключения к базе данных SQLite
        """
        return f"sqlite:///{self.db_name}"


class TelegramSettings(BaseSettings):
    """
    Настройки для подключения к Telegram API.

    Этот класс использует pydantic для загрузки токена Telegram бота из переменных окружения и файла `.env`.

    Attributes:
        token (str): Токен Telegram бота.
    """

    model_config = SettingsConfigDict(
        env_prefix="TELEGRAM_", extra="ignore", env_file=".env"
    )
    token: str


class PostgresSettings(BaseSettings):
    """
    Настройки для подключения к базе данных PostgreSQL.

    Этот класс использует pydantic для загрузки настроек из переменных окружения и файла `.env`.
    Он определяет хост, порт, имя пользователя, пароль и имя базы данных,
    а также формирует строку подключения (DSN).

    Attributes:
        host (str): Хост базы данных PostgreSQL.
        port (int): Порт базы данных PostgreSQL (по умолчанию 5432).
        username (str): Имя пользователя для подключения к базе данных PostgreSQL.
        password (SecretStr): Пароль для подключения к базе данных PostgreSQL.
        db_name (str): Имя базы данных PostgreSQL.

    Properties:
        dsn (str): Строка подключения к базе данных PostgreSQL.
    """

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_", extra="ignore", env_file=".env"
    )
    host: str
    port: int = 5432
    username: str
    password: SecretStr
    db_name: str

    @property
    def dsn(self) -> str:
        """
        Генерирует строку подключения к базе данных PostgreSQL.

        Returns:
          str: строка подключения к базе данных PostgreSQL
        """
        return f"postgresql://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db_name}"
