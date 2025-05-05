import socket
import threading

SERVER_IP = '192.168.0.1'  # Replace with your server's IP
PORT = 5001

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Server left the chat.")
                break
            print(f"Server: {data.decode()}")
        except:
            print("Connection error.")
            break

def send_messages(sock):
    while True:
        try:
            msg = input()
            if msg.lower() == 'exit':
                print("You left the chat.")
                sock.close()
                break
            sock.sendall(msg.encode())
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((SERVER_IP, PORT))
        print(f"Connected to {SERVER_IP}:{PORT}")

        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
        send_messages(client_socket)
    except:
        print("Failed to connect to the server.")
