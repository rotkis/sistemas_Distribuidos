import json

import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

def request(operation, **data):
    socket.send_string(json.dumps({"operacao": operation, **data}))
    return json.loads(socket.recv_string())


def show_response(response):
    if "erro" in response:
        print(response["erro"])
    else:
        print(json.dumps(response, ensure_ascii=False, indent=2))


def list_tasks():
    response = request("listar")
    print("Lista de tarefas:")
    if not response["tarefas"]:
        print("Nenhuma tarefa cadastrada.")
    for task in response["tarefas"]:
        print(
            f"{task['id']}. {task['titulo']} | "
            f"{task['descricao']} | {task['status']}"
        )


print("Testando conexão com servidor")
show_response(request("teste_conexao"))

print("\nCriando tarefa")
created_task = request(
    "criar",
    titulo="teste",
    descricao="teste de tarefa",
)
show_response(created_task)
task_id = created_task["id"]

print("\nBuscando tarefa")
show_response(request("buscar", id=task_id))

print("\nListando tarefas")
list_tasks()

print("\nAtualizando tarefa")
show_response(
    request(
        "atualizar",
        id=task_id,
        titulo="atualizacao",
        descricao="teste de update",
        status="completa",
    )
)

print("\nListando tarefas após atualização")
list_tasks()

print("\nRemovendo tarefa")
show_response(request("remover", id=task_id))

print("\nListando tarefas após remoção")
list_tasks()
