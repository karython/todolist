from model.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import Session


def cadastrar_tarefa(descricao: str, situacao: bool):
    try:
        # Criar uma nova instância do modelo Tarefa com os dados fornecidos
        nova_tarefa = Tarefa(descricao=descricao, situacao=situacao)
        session = Session()
        # Adicionar a tarefa na sessão
        session.add(nova_tarefa)
        
        # Commit para salvar a tarefa no banco de dados
        session.commit()
        
        # Retorna o objeto Tarefa inserido
        return nova_tarefa

    except SQLAlchemyError as e:
        # Caso ocorra um erro, faz o rollback
        session.rollback()
        print(f"Erro ao cadastrar tarefa: {e}")
        return None
    finally:
        # Fechar a sessão após a operação
        session.close()


def excluir_tarefa(id_tarefa: int):
    try:
        session = Session()
        
        # Buscar a tarefa pelo ID
        tarefa = session.query(Tarefa).filter(Tarefa.id == id_tarefa).first()
        
        if tarefa:
            # Deletar a tarefa encontrada
            session.delete(tarefa)
            session.commit()
            print(f"Tarefa com id {id_tarefa} excluída com sucesso!")
            return True
        else:
            print(f"Tarefa com id {id_tarefa} não encontrada.")
            return False
        
    except SQLAlchemyError as e:
        # Caso ocorra um erro, faz o rollback
        session.rollback()
        print(f"Erro ao excluir tarefa: {e}")
        return False
    finally:
        # Fechar a sessão após a operação
        session.close()


