from model import Task  # Importa a classe Task do arquivo model.py. Esta classe representa uma tarefa na lista.

# Função para adicionar uma tarefa à lista
def adicionar_tarefa(lista, valor, update_callback):
    # Verifica se o valor da tarefa não é uma string vazia ou apenas espaços em branco
    if valor.strip():  # O método strip() remove espaços em branco antes e depois da string, e a condição verifica se a string não está vazia
        task = Task(valor)  # Cria uma nova instância da classe Task, passando o valor da tarefa (nome) como argumento
        lista.controls.append(task)  # Adiciona a tarefa à lista de controles (lista de tarefas)
        update_callback()  # Chama a função de atualização para refletir as mudanças na interface

    pass  # O uso de pass aqui indica que não há mais código para ser executado após a verificação e adição da tarefa (não é necessário, pois a lógica já foi concluída)

# Função para excluir tarefas selecionadas da lista
def excluir_tarefas_selecionadas(lista, update_callback):
    # Filtra e mantém apenas as tarefas que não estão selecionadas
    lista.controls = [task for task in lista.controls if not task.is_selected()]
    update_callback()  # Chama a função de atualização para refletir as mudanças após a exclusão das tarefas selecionadas

    pass  # O uso de pass aqui indica que a função já foi concluída, sem necessidade de mais código
