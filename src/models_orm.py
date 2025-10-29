import datetime, enum
from typing import Annotated, Optional
from sqlalchemy import ForeignKey, CheckConstraint, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256

# --- Общие аннотации для удобства в ORM-моделях ---
intpk = Annotated[int, mapped_column(primary_key=True)]  # первичный ключ
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow,
)]

# --- Enum: режим занятости ---
class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"

# --- Таблица работников ---
class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str]

    # Связь: один работник → несколько резюме
    resumes: Mapped[list["ResumesOrm"]] = relationship(back_populates="worker")

    # Фильтрованная связь (только частичная занятость)
    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
        order_by="ResumesOrm.id.desc()",
    )

# --- Таблица резюме ---
class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))

    # Связь с работником
    worker: Mapped["WorkersOrm"] = relationship(back_populates="resumes")

    # Связь многие-ко-многим с вакансиями через таблицу откликов
    vacancies_replied: Mapped[list["VacanciesOrm"]] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replies",
    )

# --- Таблица вакансий ---
class VacanciesOrm(Base):
    __tablename__ = "vacancies"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]

    # Обратная связь многие-ко-многим с резюме
    resumes_replied: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replies",
    )

# --- Таблица откликов (связующая таблица) ---
class VacanciesRepliesOrm(Base):
    __tablename__ = "vacancies_replies"

    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"), primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id", ondelete="CASCADE"), primary_key=True)
    cover_letter: Mapped[Optional[str]]  # сопроводительное письмо

