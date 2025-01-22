from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict # используется для создания классов конфигурации, а SettingsConfigDict позволяет настраивать поведение этого класса.


class SQLiteSettings(BaseSettings):
    """
    Будет использовать функциональность Pydantic для управления настройками.
    """
    model_config = SettingsConfigDict(env_prefix="SQLITE_", extra="ignore", env_file=".env")
    db_name: str

    @property
    def dsn(self) -> str:                   # определяем метод dsn, который возвращает строку (DSN — Data Source Name) для подключения к базе данных SQLite.
        return f"sqlite:///{self.db_name}"  # формируем строку подключения к базе данных SQLite.
    

    """
    Класс настроек для работы с базой данных SQLite с использованием Pydantic.
    Он позволяет загружать настройки из переменных окружения и файла .env,
    а также предоставляет удобный способ получения строки подключения к базе данных через свойство dsn.

    """

class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TELEGRAM_", extra="ignore", env_file=".env")
    token: str


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_", extra="ignore", env_file=".env")
    host: str
    port: int = 5432
    username: str
    password: SecretStr
    db_name: str

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db_name}"


