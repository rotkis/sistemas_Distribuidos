import zmq

context = zmq.Context()
poller = zmq.Poller()

client_socket = context.socket(zmq.ROUTER)
client_socket.bind("tcp://*:5555")
poller.register(client_socket, zmq.POLLIN)
client_count = 0

server_socket = context.socket(zmq.DEALER)
server_socket.bind("tcp://*:5556")
poller.register(server_socket, zmq.POLLIN)
server_count = 0

while True:
    socks = dict(poller.poll())

    if socks.get(client_socket) == zmq.POLLIN:
        client_count += 1
        server_socket.send_multipart(client_socket.recv_multipart())
        print(f"Client messages: {client_count}", flush=True)

    if socks.get(server_socket) == zmq.POLLIN:
        server_count += 1
        client_socket.send_multipart(server_socket.recv_multipart())
        print(f"Server messages: {server_count}", flush=True)

