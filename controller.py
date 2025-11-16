# controller.py
import socket
import threading
import pickle

BROKER_HOST = '10.0.0.129'
BROKER_PORT = 5001

clients = {}  # client_id -> connection

def handle_client(client_conn, client_addr, broker_conn):
    print(f"[Controller] Handling client {client_addr}")
    data = client_conn.recv(4096)
    if not data:
        return
    task = pickle.loads(data)
    clients[task[2]] = client_conn  # Save client connection by ID
    broker_conn.sendall(pickle.dumps(task))

def handle_results_from_broker(broker_conn):
    while True:
        try:
            data = broker_conn.recv(4096)
            if not data:
                continue
            result = pickle.loads(data)
            client_id = result["client_id"]
            if client_id in clients:
                clients[client_id].sendall(pickle.dumps(result))
        except:
            continue

def controller_server():
    broker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    broker_sock.connect((BROKER_HOST, BROKER_PORT))
    print("[Controller] Connected to broker.")

    threading.Thread(target=handle_results_from_broker, args=(broker_sock,), daemon=True).start()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', 5000))
    server_sock.listen(5)
    print("[Controller] Waiting for clients...")

    while True:
        client_conn, client_addr = server_sock.accept()
        threading.Thread(target=handle_client, args=(client_conn, client_addr, broker_sock), daemon=True).start()

if __name__ == "__main__":
    controller_server()
