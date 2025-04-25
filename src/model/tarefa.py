from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
import enum
from datetime import datetime, timedelta
from sqlalchemy.orm import declarative_base
from connection import engine

Base = declarative_base()

# Enums para prioridade e classe
class PrioridadeEnum(enum.Enum):
    alta = "alta"
    media = "media"
    baixa = "baixa"

class ClasseEnum(enum.Enum):
    saude = "saude"
    casa = "casa"
    trabalho = "trabalho"
    lazer = "lazer"

class Tarefa(Base):
    __tablename__ = "tb_enzo_netto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    status = Column(Boolean, default=False)
    prioridade = Column(Enum(PrioridadeEnum), default=PrioridadeEnum.media)
    classe = Column(Enum(ClasseEnum), nullable=False)
    data_inicio = Column(DateTime, default=datetime.now)
    data_entrega = Column(DateTime, default=lambda: datetime.now() + timedelta(days=1))
    descricao = Column(Text, nullable=True)  

Base.metadata.create_all(engine)
