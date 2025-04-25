from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, Date

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = 'tb_tarefas_mine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(Text, nullable=True)
    dt = Column(Date, nullable=True)  # Coluna para a data de vencimento

    def __init__(self, descricao, dt=None):
        self.descricao = descricao
        self.dt = dt


def create_tables(engine):
    Base.metadata.create_all(engine)