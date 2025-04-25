import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Carregar variáveis do .env
load_dotenv()

# Obter credenciais do banco de dados
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Criar URL de conexão com MySQL
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Criar a engine do SQLAlchemy
engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        print('Conectado!')
except Exception as ex:
    print('Não conectado!')

# Criar sessão para interagir com o banco de dados
SessaoLocal = sessionmaker(bind=engine)