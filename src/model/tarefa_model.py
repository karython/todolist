# Importando as classes necessárias do SQLAlchemy
from sqlalchemy.orm import declarative_base  # Para criar a classe base das tabelas (ORM)
from sqlalchemy import Column, Text, Integer, Boolean  # Tipos de coluna utilizados para definir os campos das tabelas

# Cria a classe base que será utilizada para definir os modelos do banco de dados
Base = declarative_base()

# Definindo a classe 'Tarefa' que mapeia a tabela 'tb_tarefa_jvgaleguin' no banco de dados
class Tarefa(Base):
    # Nome da tabela no banco de dados
    __tablename__ = 'tb_tarefa_jessegaleguin'

    # Definindo as colunas da tabela

    # Coluna de ID, que é chave primária e autoincrementada
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Coluna de descrição da tarefa, que é do tipo Texto e pode ser nula
    descricao = Column(Text, nullable=True)

    # Coluna de situação da tarefa, que é do tipo Booleano e tem valor padrão 'False' (Pendente)
    situacao = Column(Boolean, default=False)

    data_entrega = Column(Text, nullable=True)  # Coluna para armazenar a data de entrega da tarefa

    # Construtor da classe, inicializando os campos de descrição e situação
    def __init__(self, descricao, situacao=False, data_entrega=None):
        self.descricao = descricao
        self.situacao = situacao
        self.data_entrega = data_entrega
# Função para criar as tabelas no banco de dados
def create_tables(engine):
    # Cria todas as tabelas definidas pela classe Base (ou seja, as tabelas que herdam de Base)
    Base.metadata.create_all(engine)