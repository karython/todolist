from datetime import datetime
from model.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import Session


def cadastrar_tarefa(descricao: str, situacao: bool, data_entrega: str):
    """Cadastra uma nova tarefa no banco de dados."""
    session = Session()
    
    try:
        if isinstance(data_entrega, str):
            try:
                data_entrega = datetime.strptime(data_entrega, "%Y-%m-%d")  # Ajuste o formato conforme necessário
            except ValueError:
                raise ValueError("Data de entrega inválida. O formato esperado é YYYY-MM-DD.")
        # Cria uma nova instância do modelo Tarefa
        nova_tarefa = Tarefa(descricao=descricao, situacao=situacao, data_entrega=data_entrega)
        session.add(nova_tarefa)
        session.commit()  # Salva a tarefa no banco de dados
        print(f"Tarefa cadastrada com sucesso: {nova_tarefa.descricao}, {nova_tarefa.situacao}")
        return {"id": nova_tarefa.id, "descricao": nova_tarefa.descricao, "situacao": nova_tarefa.situacao}
    except SQLAlchemyError as e:
        session.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao cadastrar tarefa: {e}")
        return None
    finally:
        session.close()  # Fecha a sessão



def excluir_tarefa(tarefa_id: int):
    """Exclui uma tarefa do banco de dados pelo ID."""
    session = Session()
    try:
        # Busca a tarefa pelo ID
        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if tarefa:
            session.delete(tarefa)
            session.commit()
            print(f"Tarefa excluída com sucesso: ID {tarefa_id}")
            return True
        print(f"Tarefa com ID {tarefa_id} não encontrada.")
        return False
    except SQLAlchemyError as e:
        session.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao excluir tarefa: {e}")
        return False
    finally:
        session.close()  # Fecha a sessão


def editar_tarefa(tarefa_id: int, nova_descricao: str, nova_situacao: bool):
    """Edita uma tarefa existente no banco de dados."""
    session = Session()
    try:
        # Busca a tarefa pelo ID
        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if tarefa:
            print(f"Tarefa antes da edição: ID {tarefa.id}, Descrição: {tarefa.descricao}, Situação: {tarefa.situacao}")
            # Atualiza os campos da tarefa
            tarefa.descricao = nova_descricao
            tarefa.situacao = nova_situacao
            session.commit()  # Salva as alterações no banco de dados
            print(f"Tarefa após a edição: ID {tarefa.id}, Descrição: {tarefa.descricao}, Situação: {tarefa.situacao}")
            return True
        print(f"Tarefa com ID {tarefa_id} não encontrada.")
        return False
    except SQLAlchemyError as e:
        session.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao editar a tarefa: {e}")
        return False
    finally:
        session.close()  # Fecha a sessão


def buscar_tarefa_por_id(tarefa_id: int):
    """Busca uma tarefa pelo ID."""
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if tarefa:
            print(f"Tarefa encontrada: ID {tarefa.id}, Descrição: {tarefa.descricao}, Situação: {tarefa.situacao}")
            return tarefa
        print(f"Tarefa com ID {tarefa_id} não encontrada.")
        return None
    except SQLAlchemyError as e:
        print(f"Erro ao buscar tarefa: {e}")
        return None
    finally:
        session.close()  # Fecha a sessão


def listar_tarefas():
    """Lista todas as tarefas do banco de dados."""
    session = Session()
    try:
        tarefas = session.query(Tarefa).all()
        print(f"{len(tarefas)} tarefa(s) encontrada(s).")
        return tarefas
    except SQLAlchemyError as e:
        print(f"Erro ao listar tarefas: {e}")
        return []
    finally:
        session.close()  # Fecha a sessão