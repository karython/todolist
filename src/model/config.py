from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Caminho do arquivo SQLite (você pode personalizar o nome do arquivo)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "banco_tarefas.db")

# Classe de configuração para SQLite
class Config:
    DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

# Criar a Engine para SQLite
engine = create_engine(
    Config.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário para evitar erro com múltiplas threads
)

# Criador de sessões (você pode usar isso em outro lugar para fazer `SessionLocal()`)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Testar a conexão
try:
    with engine.connect() as connection:
        print("Conexão com SQLite bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar: {e}")
