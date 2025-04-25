from model.tarefa_model import Tarefa
from datetime import datetime
from connection import Session

def cadastrar_tarefa(descricao, situacao, data_adicionada, data_conclusao):
    session = Session()
    try:
        nova_tarefa = Tarefa(
            descricao=descricao,
            situacao=situacao,
            data_adicionada=data_adicionada,
            data_conclusao=data_conclusao
        )
        session.add(nova_tarefa)
        session.commit()
        return nova_tarefa
    except Exception as e:
        session.rollback()
        print("Erro ao cadastrar tarefa:", e)
        return None
    finally:
        session.close()

def listar_tarefas():
    session = Session()
    try:
        return session.query(Tarefa).all()
    finally:
        session.close()

def atualizar_tarefa(tarefa_id, nova_descricao, nova_situacao, nova_data_conclusao):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter_by(id=tarefa_id).first()
        if tarefa:
            tarefa.descricao = nova_descricao
            tarefa.situacao = nova_situacao
            tarefa.data_conclusao = nova_data_conclusao
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print("Erro ao atualizar tarefa:", e)
        return False
    finally:
        session.close()

def excluir_tarefa_por_id(tarefa_id):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter_by(id=tarefa_id).first()
        if tarefa:
            session.delete(tarefa)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print("Erro ao excluir tarefa:", e)
        return False
    finally:
        session.close()
