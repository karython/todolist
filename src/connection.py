# Importando as bibliotecas necessárias
from dotenv import load_dotenv  # Biblioteca para carregar variáveis de ambiente a partir de um arquivo .env
from sqlalchemy import create_engine  # Importa a função para criar uma conexão com o banco de dados
from sqlalchemy.orm import sessionmaker  # Importa a função para criar sessões de banco de dados
import os  # Biblioteca para trabalhar com variáveis de ambiente e sistemas de arquivos
from model.tarefa_model import create_tables  # Importa a função `create_tables` que cria as tabelas no banco de dados

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Classe de configuração que armazena as informações de conexão com o banco de dados
class Config:
    # Obtendo as variáveis de ambiente necessárias para a configuração do banco de dados
    DB_USER = os.getenv('DB_USER')  # Nome do usuário do banco de dados
    DB_HOST = os.getenv('DB_HOST')  # Endereço do host onde o banco de dados está rodando
    DB_NAME = os.getenv('DB_NAME')  # Nome do banco de dados
    DB_PORT = os.getenv('DB_PORT', 3306)  # Porta do banco de dados (valor padrão 3306)
    DB_PASSWORD = os.getenv('DB_PASSWORD')  # Senha do banco de dados
    print('DB_USER:', DB_USER)
    print('DB_HOST:', DB_HOST)
    print('DB_NAME:', DB_NAME)
    print('DB_PORT:', DB_PORT)
    print('DB_PASSWORD:', DB_PASSWORD)
    # Formando a URL de conexão com o banco de dados usando as variáveis de ambiente
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Cria o objeto `engine` que representa a conexão com o banco de dados, utilizando a URL definida acima
engine = create_engine(
    Config.DATABASE_URL,
    pool_size=10,
    max_overflow=5,
    pool_recycle=1800,
    pool_pre_ping=True,
    )

# Cria a fábrica de sessões, que será usada para criar sessões de interação com o banco de dados
Session = sessionmaker(bind=engine)

try:
    # Tenta estabelecer uma conexão com o banco de dados
    with engine.connect() as connection:
        print('Conexão bem sucedida')  # Se a conexão for bem-sucedida, imprime a mensagem
        # Chama a função create_tables para criar as tabelas no banco de dados
        create_tables(engine)
except Exception as e:
    # Se ocorrer um erro na conexão, imprime a mensagem de erro
    print(f'Erro ao conectar: {e}')