'''
/src/services/tarefa_service.py
Definir funções para gerenciar tarefas no banco de dados.
'''
# Importando as bibliotecas necessárias.
from model.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import Session
from datetime import datetime

# Cadastrar uma nova tarefa no banco de dados.
def cadastrar_tarefa(data: datetime, descricao: str):
    try:
        nova_tarefa = Tarefa(data=data, descricao=descricao)  # Cria uma tarefa
        session = Session()
        session.add(nova_tarefa)  # Adiciona à sessão
        session.commit()  # Salva no banco
        session.refresh(nova_tarefa)  # Atualiza o objeto
        return nova_tarefa  # Retorna a nova tarefa
    except SQLAlchemyError as e:
        session.rollback()  # Reverte mudançasit c em caso de erro
        print(f"Erro ao cadastrar tarefa: {e}")
        return None
    finally:
        session.close()  # Fecha a sessão

# Remover uma tarefa pelo ID
def remover_tarefa(id: int):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter(Tarefa.id == id).first()  # Busca a tarefa
        if tarefa:
            session.delete(tarefa)  # Remove do banco
            session.commit()  # Confirma a exclusão
            return True
        else:
            print(f"Tarefa com ID {id} não encontrada.")
            return False
    except Exception as e:
        session.rollback()  # Reverte mudanças em caso de erro
        print(f"Erro deletando tarefa: {e}")
        return False
    finally:
        session.close()  # Fecha a sessão

# Atualizar uma tarefa pelo ID
def atualizar_tarefa(tarefa_id: int, descricao: str, data: datetime):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()  # Busca a tarefa
        if tarefa: 
            tarefa.descricao = descricao  # Atualiza a descrição
            tarefa.data = data  # Atualiza a situação
            session.commit()  # Salva alterações
            session.refresh(tarefa)  # Atualiza o objeto
            return tarefa  # Retorna a tarefa atualizada
        else:
            print(f"Tarefa com ID {tarefa_id} não encontrada.")
            return None
    except Exception as e:
        session.rollback()  # Reverte mudanças em caso de erro
        print(f"Erro atualizando tarefa: {e}")
        return None
    finally:
        session.close()  # Fecha a sessão

def query_tarefa(): # Uma query é uma consulta ao banco de dados.
    session = Session()
    try:
        tarefas = session.query(Tarefa).all()  # Busca todas as tarefas
        return tarefas  # Retorna a lista de tarefas
    except Exception as e:
        print(f"Erro ao consultar tarefas: {e}")
        return None
    finally:
        session.close()  # Fecha a sessão