# broker.py
import socket
import threading
import queue
import pickle

TASK_QUEUE = queue.Queue()
RESULT_QUEUE = queue.Queue()

controller_conn = None
workers = []

def handle_controller():
    global controller_conn
    while True:
        try:
            data = controller_conn.recv(4096)
            if not data:
                break
            task = pickle.loads(data)
            TASK_QUEUE.put(task)
        except:
            break

def handle_worker(conn):
    while True:
        try:
            # Send a task to worker
            if not TASK_QUEUE.empty():
                task = TASK_QUEUE.get()
                conn.sendall(pickle.dumps(task))
                # Wait for result
                result_data = conn.recv(4096)
                if result_data:
                    result = pickle.loads(result_data)
                    RESULT_QUEUE.put(result)
                    # Send result to controller
                    if controller_conn:
                        controller_conn.sendall(pickle.dumps(result))
        except:
            break

def broker_server():
    global controller_conn
    # Listen for controller
    controller_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controller_sock.bind(('localhost', 5001))
    controller_sock.listen(1)
    print("[Broker] Waiting for controller...")
    controller_conn, _ = controller_sock.accept()
    print("[Broker] Controller connected.")
    threading.Thread(target=handle_controller, daemon=True).start()

    # Listen for workers
    worker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker_sock.bind(('localhost', 5002))
    worker_sock.listen(3)
    print("[Broker] Waiting for workers...")

    while True:
        wconn, _ = worker_sock.accept()
        workers.append(wconn)
        threading.Thread(target=handle_worker, args=(wconn,), daemon=True).start()
        print("[Broker] Worker connected.")

if __name__ == "__main__":
    broker_server()
