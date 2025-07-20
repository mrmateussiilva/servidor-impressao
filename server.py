# server.py
import socket
import threading
import mss
import pickle
import zlib
import pyautogui

HOST = '0.0.0.0'
PORT = 5000

def capturar_e_enviar(conn):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            img = sct.grab(monitor)
            w, h = img.size
            header = pickle.dumps((w, h))
            header_size = len(header).to_bytes(4, 'big')

            data = pickle.dumps(img.rgb)
            compressed = zlib.compress(data, 9)
            img_size = len(compressed).to_bytes(4, 'big')

            try:
                conn.sendall(header_size + header + img_size + compressed)
            except:
                break

def receber_comandos(conn):
    while True:
        try:
            cmd = conn.recv(1024).decode()
            if not cmd:
                break
            exec_comando(cmd)
        except:
            break

def exec_comando(cmd):
    parts = cmd.strip().split()
    if parts[0] == 'move':
        x, y = int(parts[1]), int(parts[2])
        pyautogui.moveTo(x, y)
    elif parts[0] == 'click':
        pyautogui.click()
    elif parts[0] == 'write':
        pyautogui.write(" ".join(parts[1:]))
    elif parts[0] == 'press':
        pyautogui.press(parts[1])
    elif parts[0] == 'hotkey':
        pyautogui.hotkey(*parts[1:])

print("[*] Aguardando conexão...")
s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print("[+] Conectado por", addr)

threading.Thread(target=capturar_e_enviar, args=(conn,), daemon=True).start()
receber_comandos(conn)

