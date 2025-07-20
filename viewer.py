import socket
import pickle
import zlib
import numpy as np
import cv2

HOST = '192.168.15.38'  # IP do servidor remoto
PORT = 5000

s = socket.socket()
s.connect((HOST, PORT))

def enviar_comando(cmd):
    s.send(cmd.encode())

while True:
    size_data = s.recv(4)
    if not size_data:
        break
    size = int.from_bytes(size_data, 'big')
    buffer = b''
    while len(buffer) < size:
        buffer += s.recv(size - len(buffer))

    data = zlib.decompress(buffer)
    rgb = pickle.loads(data)
    img = np.frombuffer(rgb, dtype=np.uint8).reshape((1080, 1920, 3))

    cv2.imshow("Remoto", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('c'):
        enviar_comando("click")
    elif key == ord('m'):
        enviar_comando("move 500 300")
    elif key == ord('h'):
        enviar_comando("hotkey ctrl c")

