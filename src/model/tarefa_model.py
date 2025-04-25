from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "neguebapietro"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False)
    situacao = Column(Boolean, default=False)
    data_adicionada = Column(DateTime, nullable=False)  # Substitui data_hora por data_adicionada
    data_conclusao = Column(DateTime, nullable=True)    # Mantém data_conclusao

    def __init__(self, descricao, situacao, data_adicionada=None, data_conclusao=None):
        self.descricao = descricao
        self.situacao = situacao
        self.data_adicionada = data_adicionada or datetime.now()
        self.data_conclusao = data_conclusao

    def __repr__(self):
        return f"<Tarefa(id={self.id}, descricao={self.descricao}, situacao={self.situacao}, data_adicionada={self.data_adicionada}, data_conclusao={self.data_conclusao})>"

def create_tables(engine):
    Base.metadata.create_all(engine)