import httpx    # библиотека для запросов API
import pydantic     # библиотека для работы с файлами .env
import pydantic_settings

class BaseSettings(pydantic_settings.BaseSettings):
    """
    Позволяет работать с файлами из каталога .env
    """
    model_config = pydantic_settings.SettingsConfigDict( extra="ignore", env_file=".env")
    api_token: str

settings = BaseSettings()
result = httpx.get(f"https://api.telegram.org/bot{settings.api_token}/getMe")

print(result.json())

