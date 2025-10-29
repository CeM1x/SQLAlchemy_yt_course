import datetime
from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Enum, ForeignKey, TIMESTAMP, text
)
from models_orm import Workload  # импорт enum-а из ORM-модели (режим работы)

# --- Общие метаданные для всех таблиц (Core API) ---
metadata_obj = MetaData()

# --- Таблица сотрудников ---
workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

# --- Таблица резюме ---
resumes_table = Table(
    "resumes",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String(256)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(Workload)),  # режим работы (из Enum)
    Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),  # связь с работником
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),  # дата создания
    Column("updated_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())"),
           onupdate=datetime.datetime.utcnow),  # автообновление даты
)

# --- Таблица вакансий ---
vacancies_table = Table(
    "vacancies",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("compensation", Integer, nullable=True),
)

# --- Таблица откликов (многие-ко-многим: резюме ↔ вакансии) ---
vacancies_replies_table = Table(
    "vacancies_replies",
    metadata_obj,
    Column("resume_id", ForeignKey("resumes.id", ondelete="CASCADE"), primary_key=True),
    Column("vacancy_id", ForeignKey("vacancies.id", ondelete="CASCADE"), primary_key=True),
)


