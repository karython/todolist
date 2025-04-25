from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from model.tarefa_model import create_tables

load_dotenv()

class Config:
    DB_USER = os.getenv('DB_USER') 
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Configura o pool de conexões com limite
engine = create_engine(
    Config.DATABASE_URL,
    pool_size=10,  # Limita o número de conexões simultâneas
    max_overflow=5,  # Número máximo de conexões extras
    pool_recycle=3600,  # Recicla conexões após 1 hora
    pool_timeout=30,  # Tempo limite para obter uma conexão
)

# Usa scoped_session para gerenciar sessões reutilizáveis
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

try:
    with engine.connect() as connection:
        print('Conexão bem sucedida')
        create_tables(engine)
except Exception as e:
    print(f'Erro ao conectar: {e}')