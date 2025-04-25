'''
src/model/tarefa_model.py
Define o modelo Tarefa e a criação de tabelas no banco de dados.
'''

# Importando as bibliotecas necessárias.
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, Boolean, DateTime

# Criação de uma base declarativa para os modelos
Base = declarative_base()

# Modelo Tarefa que representa a tabela 'tb_tarefa_taskforce' no banco de dados
# "Mas o que é uma classe?" - Uma classe é um modelo para criar objetos. Ela define atributos e métodos que os objetos criados a partir dela terão.
class Tarefa(Base):
    __tablename__ = 'tb_tarefa_taskforce'

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único e autoincrementado
    data = Column(DateTime, nullable=False)  # Data e hora da tarefa, não pode ser nula
    descricao = Column(Text, nullable=True)  # Descrição da tarefa, pode ser nula

    # Construtor para inicializar a tarefa com descrição e situação
    # "Mas o que é um construtor?" - É um método especial que é chamado quando um objeto é criado.
    # Ele é usado para inicializar os atributos do objeto com valores específicos.
    def __init__(self, data, descricao):
        self.descricao = descricao
        self.data = data

# Função para criar as tabelas no banco de dados a partir do modelo
def create_tables(engine):
    Base.metadata.create_all(engine)  # Gera as tabelas no banco com base nos modelos declarados