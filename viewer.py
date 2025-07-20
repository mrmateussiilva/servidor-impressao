# viewer.py
import socket
import pickle
import zlib
import numpy as np
import cv2

HOST = '192.168.15.8'  # Substitua pelo IP da máquina controlada
PORT = 5000

def recv_exact(sock, size):
    data = b''
    while len(data) < size:
        more = sock.recv(size - len(data))
        if not more:
            raise EOFError("Conexão encerrada.")
        data += more
    return data

s = socket.socket()
s.connect((HOST, PORT))

def enviar_comando(cmd):
    s.send(cmd.encode())

while True:
    try:
        # 1. Recebe cabeçalho com resolução
        header_size = int.from_bytes(recv_exact(s, 4), 'big')
        w, h = pickle.loads(recv_exact(s, header_size))

        # 2. Recebe imagem
        size_data = recv_exact(s, 4)
        size = int.from_bytes(size_data, 'big')
        buffer = recv_exact(s, size)

        # 3. Reconstrói imagem
        data = zlib.decompress(buffer)
        rgb = pickle.loads(data)
        img = np.frombuffer(rgb, dtype=np.uint8).reshape((h, w, 3))
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
    except Exception as e:
        print("[ERRO]", e)
        break

cv2.destroyAllWindows()

