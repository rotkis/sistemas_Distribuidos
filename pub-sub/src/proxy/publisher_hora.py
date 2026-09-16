import zmq
from datetime import datetime
from time import sleep

TOPIC = "hora"

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

# slow joiner: dá tempo do proxy aceitar a conexão antes do 1o envio
sleep(1)

while True:
    message = datetime.now().strftime("%H:%M:%S")
    print(f"[{TOPIC}] {message}", flush=True)
    pub.send_string(TOPIC, zmq.SNDMORE)
    pub.send_string(message)
    sleep(1)

pub.close()
context.close()