import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5001

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"[{timestamp()}] Client left the chat.")
                break
            print(f"[{timestamp()}] Client: {data.decode()}")
        except:
            print(f"[{timestamp()}] Connection error.")
            break

def send_messages(conn):
    while True:
        try:
            msg = input()
            if msg.lower() == 'exit':
                print(f"[{timestamp()}] You left the chat.")
                conn.close()
                break
            conn.sendall(msg.encode())
            print(f"[{timestamp()}] You (sent): {msg}")
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[{timestamp()}] Server listening on {HOST}:{PORT}...")
    conn, addr = server_socket.accept()
    print(f"[{timestamp()}] Connected by {addr}")

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()
    send_messages(conn)
