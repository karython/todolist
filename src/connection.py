from dotenv import load_dotenv  # Importa a função load_dotenv para carregar as variáveis de ambiente do arquivo .env
from sqlalchemy import create_engine  # Importa a função create_engine do SQLAlchemy para criar a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker  # Importa sessionmaker, que cria sessões para interagir com o banco de dados
import os  # Importa o módulo os para acessar variáveis de ambiente
from model.models import create_tables  # Importa a função create_tables, que cria as tabelas no banco de dados, de um arquivo model

load_dotenv()  # Carrega as variáveis de ambiente a partir do arquivo .env

# Definição da classe Config para armazenar as configurações do banco de dados
class Config:
    DB_USER = os.getenv('DB_USER')  # Obtém o nome de usuário do banco de dados a partir da variável de ambiente DB_USER
    DB_HOST = os.getenv('DB_HOST')  # Obtém o host do banco de dados a partir da variável de ambiente DB_HOST
    DB_NAME = os.getenv('DB_NAME')  # Obtém o nome do banco de dados a partir da variável de ambiente DB_NAME
    DB_PORT = os.getenv('DB_PORT', 3306)  # Obtém a porta do banco de dados a partir da variável de ambiente DB_PORT (se não definida, usa 3306 como valor padrão)
    DB_PASSWORD = os.getenv('DB_PASSWORD')  # Obtém a senha do banco de dados a partir da variável de ambiente DB_PASSWORD
    # Formata a URL de conexão com o banco de dados, usando as variáveis definidas
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Criação do engine (conexão com o banco de dados) usando a URL de conexão definida em Config.DATABASE_URL
engine = create_engine(Config.DATABASE_URL)

# Criação da sessão para interagir com o banco de dados. As sessões não confirmam automaticamente as transações.
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tentativa de conectar ao banco de dados e verificar se a conexão foi bem-sucedida
try:
    # Tenta se conectar ao banco de dados
    with engine.connect() as connection:
        print('Conexão bem sucedida')  # Se a conexão for bem-sucedida, imprime uma mensagem de sucesso
        create_tables(engine)  # Chama a função create_tables para criar as tabelas no banco de dados
except Exception as e:  # Se ocorrer algum erro durante a conexão
    print(f'Erro ao conectar: {e}')  # Imprime a mensagem de erro
