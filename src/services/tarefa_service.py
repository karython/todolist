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


def excluir_tarefa(tarefa_id):
    session = Session()
    try:

        exc_tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        
        if exc_tarefa:
            session.delete(exc_tarefa)
            session.commit()
            return f'Tarefa excluida com sucesso'
        else:
            return f'Tarefa não encontrada'

    except Exception as e:
        # rollback
        session.rollback()
        return f'Erro ao excluir tarefa {e}'
    finally:
        # fechar a conexao
        session.close()

def editar_tarefa(tarefa_id: int, nova_descricao: str, nova_situacao: bool):
    session = Session()
    try:
        tarefa = session.query(Tarefa.id == tarefa_id).first()

        if not tarefa:
            return 'Tarefa não encontrada!'

        # atualizar os valores no banco  
        tarefa.descricao = nova_descricao
        tarefa.situacao = nova_situacao

        
        session.commit()

        return f'Tarefa {tarefa_id} atualizada com sucesso!'
    
    except Exception as e:
        session.rollback()
        return f'Erro ao editar tarefa {e}'
    finally:
        session.close()