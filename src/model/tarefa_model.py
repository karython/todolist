from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, Boolean

# Criação da base declarativa para os modelos
Base = declarative_base()

class Tarefa(Base):
    """Modelo da tabela de tarefas no banco de dados."""
    __tablename__ = 'tb_tarefa_PhilV'

    # Definição das colunas da tabela
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(Text, nullable=True)
    situacao = Column(Boolean, default=False)

    def __init__(self, descricao, situacao):
        """Inicializa uma nova instância da classe Tarefa."""
        self.descricao = descricao
        self.situacao = situacao

def create_tables(engine):
    """Cria as tabelas no banco de dados se não existirem."""
    Base.metadata.create_all(engine)


