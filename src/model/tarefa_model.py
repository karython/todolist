from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, Boolean


Base = declarative_base()

class Tarefa(Base):
    __tablename__ = 'tb_tarefas_pietroenegueba'

    id = Column(Integer, primary_key=True ,autoincrement=True)
    descricao = Column(Text, nullable=True)
    situacao = Column(Boolean, default=False)

    def __init__ (self, descricao, situacao):
        self.descricao = descricao
        self.situacao = situacao


def create_tables(engine):
    Base.metadata.create_all(engine)