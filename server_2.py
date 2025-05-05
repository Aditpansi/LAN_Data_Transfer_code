import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5001

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def handle_client(conn, addr):
    print(f"[{timestamp()}] Client {addr} joined the chat.")
    
    def receive():
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"[{timestamp()}] Client {addr} left the chat.")
                    break
                print(f"[{timestamp()}] Client: {data.decode()}")
            except:
                print(f"[{timestamp()}] Connection error with {addr}")
                break

    def send():
        while True:
            try:
                msg = input()
                if msg.lower() == 'exit':
                    print(f"[{timestamp()}] You ended the chat with {addr}.")
                    conn.close()
                    break
                conn.sendall(msg.encode())
                print(f"[{timestamp()}] You (sent): {msg}")
            except:
                break

    recv_thread = threading.Thread(target=receive, daemon=True)
    recv_thread.start()
    send()  # This blocks until you type "exit" or connection breaks
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[{timestamp()}] Server is listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        handle_client(conn, addr)  # Waits until client disconnects before accepting new one
