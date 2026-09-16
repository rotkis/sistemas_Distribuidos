import os
import zmq

# TOPICS: lista separada por vírgula. "" (vazio) = assina tudo.
TOPICS = [t for t in os.environ.get("TOPICS", "").split(",") if t]
NAME = os.environ.get("NAME", "subscriber")

context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.connect("tcp://proxy:5556")

if TOPICS:
    for topic in TOPICS:
        sub.setsockopt_string(zmq.SUBSCRIBE, topic)
else:
    sub.setsockopt_string(zmq.SUBSCRIBE, "")

print(f"{NAME} inscrito em: {TOPICS or ['*']}", flush=True)

while True:
    topic, message = sub.recv_multipart()
    print(f"{NAME} <- [{topic.decode()}] {message.decode()}", flush=True)

sub.close()
context.close()