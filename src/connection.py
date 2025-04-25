from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os   #Navegar pelos diretórios
from model.tarefa_model import create_tables

load_dotenv() #Carregar variáveis de ambiente a partir de um arquivo .env

class Config:
    DB_USER = os.getenv('DB_USER') #getenv = pegar as credencias do .env
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT', 3306)
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(Config.DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) #sessão para interagir com o banco de dados

try:
    with engine.connect() as connection:
        print('Conexão bem sucedida')
        create_tables(engine)
except Exception as e:
    print(f'Erro ao conectar: {e}')