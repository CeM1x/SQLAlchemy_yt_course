from typing import Annotated
from sqlalchemy import String, create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from config import settings

# --- Создание движков для синхронного и асинхронного подключения к БД ---

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,  # синхронный движок (psycopg)
    echo=True,  # логирование SQL-запросов
    # pool_size=5,
    # max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,  # асинхронный движок (asyncpg)
    echo=True,
)

# --- Фабрики сессий ---
session_factory = sessionmaker(sync_engine)                # синхронные сессии
async_session_factory = async_sessionmaker(async_engine)   # асинхронные сессии

# --- Аннотация типов для удобства в ORM-моделях ---
str_256 = Annotated[str, 256]

# --- Общие метаданные для всех моделей ---
orm_metadata = MetaData()

# --- Базовый класс для всех ORM-моделей ---
class Base(DeclarativeBase):
    metadata = orm_metadata
    type_annotation_map = {
        str_256: String(256)  # автоматическое преобразование str_256 → String(256)
    }

    repr_cols_num = 3   # сколько колонок показывать в __repr__
    repr_cols = tuple() # или можно задать вручную

    def __repr__(self):
        # Человекочитаемое представление модели (для отладки)
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
