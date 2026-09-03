import json

import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

tasks = {}
next_task_id = 1

while True:
    request = json.loads(socket.recv_string())
    operation = request.get("operacao")

    if operation == "teste_conexao":
        response = {"mensagem": "ACK"}
    elif operation == "criar":
        title = str(request.get("titulo", "")).strip()
        description = str(request.get("descricao", "")).strip()
        if not title:
            response = {"erro": "O título da tarefa não pode ser vazio."}
        else:
            task_id = str(next_task_id)
            next_task_id += 1
            tasks[task_id] = {
                "id": task_id,
                "titulo": title,
                "descricao": description,
                "status": "não completo",
            }
            response = tasks[task_id]
    elif operation == "buscar":
        task_id = str(request.get("id", ""))
        response = tasks.get(task_id, {"erro": "Tarefa não encontrada."})
    elif operation == "listar":
        response = {"tarefas": list(tasks.values())}
    elif operation == "atualizar":
        task_id = str(request.get("id", ""))
        if task_id in tasks:
            task = tasks[task_id]
            task["titulo"] = str(request.get("titulo", task["titulo"])).strip()
            task["descricao"] = str(request.get("descricao", task["descricao"])).strip()
            task["status"] = str(request.get("status", task["status"])).strip()
            response = task
        else:
            response = {"erro": "Tarefa não encontrada."}
    elif operation == "remover":
        task_id = str(request.get("id", ""))
        if task_id in tasks:
            del tasks[task_id]
            response = {"mensagem": "Tarefa removida."}
        else:
            response = {"erro": "Tarefa não encontrada."}
    else:
        response = {"erro": "Operação inválida."}

    print(f"Operação recebida: {operation}", flush=True)
    socket.send_string(json.dumps(response, ensure_ascii=False))

