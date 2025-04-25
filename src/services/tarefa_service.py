from model.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import Session
from datetime import date

def cadastrar_tarefa(descricao: str, dt: str):
    session = Session()
    try:
        # Normaliza a descrição para minúsculas
        descricao_normalizada = descricao.strip().lower()

        # Verifica se já existe uma tarefa com a mesma descrição
        if session.query(Tarefa).filter(Tarefa.descricao == descricao_normalizada).first():
            return "Tarefa já existe."

        # Criar uma nova instância do modelo Tarefa com os dados fornecidos
        nova_tarefa = Tarefa(
            descricao=descricao_normalizada,
            dt=dt  # Data fornecida
        )
        
        # Adicionar a tarefa na sessão
        session.add(nova_tarefa)
        
        # Commit para salvar a tarefa no banco de dados
        session.commit()
        
        # Retorna uma cópia do objeto Tarefa inserido
        tarefa_cadastrada = session.query(Tarefa).get(nova_tarefa.id)
        return tarefa_cadastrada

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
            return f"Tarefa {tarefa_id} excluída com sucesso!"
        else:
            return f"Tarefa {tarefa_id} não encontrada!"

    except Exception as e:
        session.rollback()
        print(f"Erro ao excluir tarefa: {e}")
        return f"Erro ao excluir tarefa {tarefa_id}: {e}"
    finally:
        session.close()

def editar_tarefa(tarefa_id: int, nova_descricao: str):
    session = Session()
    try:
        # Normaliza a nova descrição para minúsculas
        nova_descricao_normalizada = nova_descricao.strip().lower()

        # Verifica se já existe uma tarefa com a mesma descrição
        if session.query(Tarefa).filter(Tarefa.descricao == nova_descricao_normalizada, Tarefa.id != tarefa_id).first():
            return "Tarefa já existe."

        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

        if tarefa:
            tarefa.descricao = nova_descricao_normalizada
    
            session.commit()
            return f"Tarefa {tarefa_id} editada com sucesso!"
        else:
            return f"Tarefa {tarefa_id} não encontrada!"

    except Exception as e:
        session.rollback()
        return f"Erro ao editar tarefa: {e}"
    finally:
        session.close()

def atualizar_vencimento():
    """Atualiza o status de vencimento das tarefas no banco de dados."""
    session = Session()
    try:
        tarefas = session.query(Tarefa).all()
        for tarefa in tarefas:
            # Verifica se a data de conclusão é anterior à data corrente
            if tarefa.dt and tarefa.dt < date.today():
                print(f"Tarefa vencida: ID={tarefa.id}, Descrição={tarefa.descricao}, Data={tarefa.dt}")
            else:
                print(f"Tarefa não vencida: ID={tarefa.id}, Descrição={tarefa.descricao}, Data={tarefa.dt}")
    except Exception as e:
        session.rollback()
        print(f"Erro ao verificar vencimento: {e}")
    finally:
        session.close()