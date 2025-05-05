import socket
import threading
import time
from datetime import datetime

SERVER_IP = '192.168.0.1'
PORT = 5001

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def connect_to_server():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, PORT))
            print(f"[{timestamp()}] Connected to server.")
            return sock
        except:
            print(f"[{timestamp()}] Server not available. Retrying in 3 seconds...")
            time.sleep(3)

def chat(sock):
    def receive():
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    print(f"[{timestamp()}] Server disconnected.")
                    break
                print(f"[{timestamp()}] Server: {data.decode()}")
            except:
                break

    def send():
        while True:
            try:
                msg = input()
                if msg.lower() == 'exit':
                    print(f"[{timestamp()}] You left the chat.")
                    sock.close()
                    return
                sock.sendall(msg.encode())
                print(f"[{timestamp()}] You (sent): {msg}")
            except:
                break

    threading.Thread(target=receive, daemon=True).start()
    send()

# Keep reconnecting after server failure
while True:
    s = connect_to_server()
    chat(s)
    print(f"[{timestamp()}] Attempting to rejoin...")
