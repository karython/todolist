from dotenv import load_dotenv # Importa a função load_dotenv para carregar variáveis de ambiente do arquivo .env
from sqlalchemy import create_engine # Importa o create_engine para criar uma conexão com o banco de dados
from sqlalchemy.orm import sessionmaker # Importa sessionmaker para criar sessões de banco de dados
import os # Importa o módulo os para acessar variáveis de ambiente

from model.tarefa_model import create_tables # Importa a função create_tables do arquivo tarefa_model para criar as tabelas no banco

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env

class Config: # Classe para armazenar as configurações do banco de dados
        # Obtém as credenciais do banco de dados a partir das variáveis de ambiente
    DB_USER = os.getenv('DB_USER') 
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'     # Monta a URL de conexão com o banco de dados MySQL usando o driver pymysql

engine = create_engine(Config.DATABASE_URL)     # Cria a conxão com o banco de dados usando a URL definida

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Criação de uma sessão.

try:
    with engine.connect() as connection:
        print('Conexão bem sucedida')
        create_tables(engine)
except Exception as e:
    print(f'Erro ao conectar: {e}')