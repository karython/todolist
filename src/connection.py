from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from model.tarefa_model import create_tables

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Classe para armazenar as configurações do banco de dados
class Config:
    DB_USER = os.getenv('DB_USER')  # Usuário do banco de dados
    DB_PASSWORD = os.getenv('DB_PASSWORD')  # Senha do banco de dados
    DB_HOST = os.getenv('DB_HOST')  # Host do banco de dados
    DB_NAME = os.getenv('DB_NAME')  # Nome do banco de dados
    DB_PORT = os.getenv('DB_PORT')  # Porta do banco (padrão: 3306 para MySQL)
    
    # URL de conexão para o SQLAlchemy
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Criação do engine do SQLAlchemy para conectar ao banco
engine = create_engine(Config.DATABASE_URL)

# Criação de sessões para interagir com o banco de dados
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tenta estabelecer conexão com o banco de dados e criar tabelas
try:
    with engine.connect() as connection:
        print('Conexão bem sucedida')  # Mensagem de sucesso
        create_tables(engine)  # Criação das tabelas do banco de dados
except Exception as e:
    print(f'Erro ao conectar: {e}')  # Exibe erro caso a conexão falhe
