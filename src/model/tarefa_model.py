from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, Boolean


Base = declarative_base()

class Tarefa(Base):
    __tablename__ = 'tb_tarefa_jonabraz'

    id = Column(Integer, primary_key=True ,autoincrement=True)
    descricao = Column(Text, nullable=True)
    situacao = Column(Boolean, default=False)

    def __init__ (self, descricao, situacao):
        self.descricao = descricao
        self.situacao = situacao

    def __repr__(self):
        return f"<Tarefa(id={self.id}, descricao={self.descricao}, situacao={self.situacao})>"

def create_tables(engine):
    Base.metadata.create_all(engine)