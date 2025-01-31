from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLiteSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SQLITE_", extra="ignore", env_file=".env")
    db_name: str

    @property
    def dsn(self) -> str:
        return f"sqlite:///{self.db_name}"
    

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

