
from sqlalchemy.orm import Session
from model.tarefa import Tarefa, PrioridadeEnum, ClasseEnum
from connection import SessaoLocal
from datetime import datetime, timedelta

def validar_tarefa(nome, classe, data_inicio, data_entrega):
    if not nome or not classe:
        raise ValueError("Nome e Classe são obrigatórios.")
    if data_entrega < data_inicio:
        raise ValueError("Data de entrega não pode ser anterior ao início.")

def criar_tarefa(nome, classe, prioridade='media', data_inicio=None, data_entrega=None, descricao=None,):
    sessao = SessaoLocal()
    try:
        if not data_inicio:
            data_inicio = datetime.now()
        if not data_entrega:
            data_entrega = data_inicio.replace(hour=23, minute=59) + timedelta(days=1)
        validar_tarefa(nome, classe, data_inicio, data_entrega)
        nova_tarefa = Tarefa(
            nome=nome,
            classe=ClasseEnum(classe),
            prioridade=PrioridadeEnum(prioridade),
            data_inicio=data_inicio,
            data_entrega=data_entrega,
            descricao=descricao,
            status=False
        )
        sessao.add(nova_tarefa)
        sessao.commit()
        sessao.refresh(nova_tarefa)
        return nova_tarefa
    except Exception as e:
        sessao.rollback()
        raise e
    finally:
        sessao.close()

def listar_tarefas():
    sessao = SessaoLocal()
    try:
        tarefas = sessao.query(Tarefa).order_by(Tarefa.prioridade.desc(), Tarefa.data_entrega.asc()).all()
        return tarefas
    finally:
        sessao.close()

def editar_tarefa(tarefa_id, nome, classe, prioridade, data_inicio, data_entrega, descricao,):
    sessao = SessaoLocal()
    try:
        tarefa = sessao.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if tarefa:
            validar_tarefa(nome, classe, data_inicio, data_entrega)
            tarefa.nome = nome
            tarefa.classe = ClasseEnum(classe)
            tarefa.prioridade = PrioridadeEnum(prioridade)
            tarefa.data_inicio = data_inicio
            tarefa.data_entrega = data_entrega
            tarefa.descricao = descricao
            sessao.commit()
    finally:
        sessao.close()

def alternar_status_tarefa(tarefa_id, concluida):
    sessao = SessaoLocal()
    try:
        tarefa = sessao.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if tarefa:
            tarefa.status = concluida
            sessao.commit()
    finally:
        sessao.close()

def deletar_tarefa(tarefa_id):
    sessao = SessaoLocal()
    try:
        tarefa = sessao.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if tarefa:
            sessao.delete(tarefa)
            sessao.commit()
    finally:
        sessao.close()
