import zmq
from random import randint
from time import sleep

TOPIC = "numero"

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

sleep(1)

while True:
    message = str(randint(1, 6))
    print(f"[{TOPIC}] {message}", flush=True)
    pub.send_string(TOPIC, zmq.SNDMORE)
    pub.send_string(message)
    sleep(1)

pub.close()
context.close()