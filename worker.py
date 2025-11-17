import socket
import pickle
import multiprocessing
import worker_config  # contains BROKER_IP and BROKER_PORT
import socket as sk

def word_count(text):
    return len(text.split())

def line_count(text):
    return text.count('\n') + 1

def palindrome_check(text):
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]

def process_task(task):
    task_type, text, client_id = task

    # Perform work
    if task_type == "wordcount":
        result = word_count(text)
    elif task_type == "linecount":
        result = line_count(text)
    elif task_type == "palindrome":
        result = palindrome_check(text)
    else:
        result = "Unknown task"

    # --- Worker identity info ---
    worker_name = sk.gethostname()
    worker_ip = sk.gethostbyname(worker_name)

    # Log to worker terminal
    print(f"[Worker {worker_name} @ {worker_ip}] Executed task: {task_type} for Client {client_id}")

    # Return result + metadata
    return {
        "client_id": client_id,
        "task": task_type,
        "result": result,
        "worker_name": worker_name,
        "worker_ip": worker_ip
    }

def worker_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    broker_address = (worker_config.BROKER_IP, worker_config.BROKER_PORT)
    print(f"[Worker] Connecting to broker at {broker_address}...")
    sock.connect(broker_address)
    print("[Worker] Connected to broker.")

    # Pool of CPU processes
    pool = multiprocessing.Pool()

    # Loop forever waiting for tasks
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                continue

            task = pickle.loads(data)
            result = pool.apply(process_task, (task,))
            sock.sendall(pickle.dumps(result))

        except Exception as e:
            print("[Worker] Error:", e)
            continue

if __name__ == "__main__":
    worker_client()
