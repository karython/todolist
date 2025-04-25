from model.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import Session


def cadastrar_tarefa(descricao: str, situacao: bool):
    try:
        # Criar uma nova instância do modelo Tarefa com os dados fornecidos
        nova_tarefa = Tarefa(descricao=descricao, situacao=situacao)
        session = Session()
        if descricao != '':
            # Adicionar a tarefa na sessão
            session.add(nova_tarefa)
            
            # Commit para salvar a tarefa no banco de dados
            session.commit()
            
            # Retorna o objeto Tarefa inserido
            session.refresh(nova_tarefa)
            return nova_tarefa

    except SQLAlchemyError as e:
        # Caso ocorra um erro, faz o rollback
        session.rollback()
        print(f"Erro ao cadastrar tarefa: {e}")
        return None
    finally:
        # Fechar a sessão após a operação
        session.close()