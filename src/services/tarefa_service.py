from model.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import Session
from model.tarefa_model import Tarefa


def cadastrar_tarefa(descricao: str, situacao: bool):
    try:
        # Criar uma nova instância do modelo Tarefa com os dados fornecidos
        nova_tarefa = Tarefa(descricao=descricao, situacao=situacao)
        session = Session()
        # Adicionar a tarefa na sessão
        session.add(nova_tarefa)
        
        # Commit para salvar a tarefa no banco de dados
        session.commit()
        
        # Retorna o ID da tarefa inserida
        return nova_tarefa.id

    except SQLAlchemyError as e:
        # Caso ocorra um erro, faz o rollback
        session.rollback()
        print(f"Erro ao cadastrar tarefa: {e}")
        return None
    finally:
        # Fechar a sessão após a operação
        session.close()
    
def listar_tarefas():
    try:
        session = Session()
        todas_tarefas = session.query(Tarefa).all()
        return todas_tarefas
    except SQLAlchemyError as e:
        print(f"Erro ao listar tarefas: {e}")
        return []
    finally:
        # Fechar a sessão após a operação
        session.close()

def listar_tarefas_id(id):
    try:
        session = Session()
        # Busca a tarefa pelo id no banco de dados
        tarefa = session.query(Tarefa).filter(Tarefa.id == id).first()
        return tarefa
    except SQLAlchemyError as e:
        print(f"Erro ao listar tarefa por id: {e}")
        return None
    finally:
        # Fechar a sessão após a operação
        session.close()

def excluir_tarefas(tarefas_id):
    # Criação de uma nova sessão para excluir as tarefas
    session = Session()
        
    try:

        # Busca a exc_tarefa pelo id no banco de dados
        exc_tarefa = session.query(Tarefa).filter(Tarefa.id == tarefas_id).first()
        
        # Verifica se a exc_tarefa existe
        if exc_tarefa:
            session.delete(exc_tarefa) 
            session.commit()
            return f'Tarefa excluída com sucesso!'
        else:
            return f'Tarefa não encontrada!'
        
    except Exception as e:
        session.rollback()
        return f'Erro ao excluir a tarefa {e}'
    
    finally:
        # Fecha a sessão após o processo
        session.close()

def editar_tarefa(tarefa_id: int, novo_descricao: str, novo_situacao: bool):
    session = Session()

    try:
        # Busca a tarefa pelo id no banco de dados
        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

        # Verifica se a tarefa existe
        if not tarefa:
            return f'Tarefa não encontrada!'
        # atualizar os valores do banco de dados
        
        tarefa.descricao = novo_descricao
        tarefa.situacao = novo_situacao

        session.commit()

        return f'Tarefa {tarefa_id} editada com sucesso!'
        
    except Exception as e:
        session.rollback()
        return f'Erro ao editar a tarefa: {e}'
    finally:
        # Fecha a sessão após o processo
        session.close()