from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from src.models_orm import Workload

# --- DTO для таблицы workers ---
class WorkersAddDTO(BaseModel):
    username: str  # данные при добавлении нового работника

class WorkersDTO(WorkersAddDTO):
    id: int  # полная модель (чтение из БД)

# --- DTO для таблицы resumes ---
class ResumesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]
    workload: Workload  # enum (parttime / fulltime)
    worker_id: int      # связь с работником

class ResumesDTO(ResumesAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

# Резюме с вложенным объектом работника
class ResumesRelDTO(ResumesDTO):
    worker: "WorkersDTO"

# Работник с вложенными резюме
class WorkersRelDTO(WorkersDTO):
    resumes: list["ResumesDTO"]

# --- DTO для таблицы vacancies ---
class VacanciesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]

class VacanciesDTO(VacanciesAddDTO):
    id: int

# Вакансия без поля compensation (для оптимизации вывода)
class VacanciesWithoutCompensationDTO(BaseModel):
    id: int
    title: str

# --- DTO для связей резюме ↔ вакансии ---
# Полное резюме с работником и списком вакансий
class ResumesRelVacanciesRepliedDTO(ResumesDTO):
    worker: "WorkersDTO"
    vacancies_replied: list["VacanciesDTO"]

# То же самое, но без compensation у вакансий
class ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO(ResumesDTO):
    worker: "WorkersDTO"
    vacancies_replied: list["VacanciesWithoutCompensationDTO"]
