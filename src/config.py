from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Конфигурация приложения через .env-файл
class Settings(BaseSettings):
    # Параметры подключения к базе данных
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        # URL для асинхронного подключения через asyncpg
        # пример: postgresql+asyncpg://postgres:root@localhost:5432/db_name
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        # URL для синхронного подключения через psycopg
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Загрузка переменных из .env, который лежит на уровень выше текущего файла
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent.parent / ".env")


# Инициализация настроек при старте приложения
settings = Settings()
