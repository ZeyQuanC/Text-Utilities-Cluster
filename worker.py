# worker.py
import socket
import pickle
import multiprocessing

def word_count(text):
    return len(text.split())

def line_count(text):
    return text.count('\n') + 1

def palindrome_check(text):
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]

def process_task(task):
    task_type, text, client_id = task
    if task_type == "wordcount":
        result = word_count(text)
    elif task_type == "linecount":
        result = line_count(text)
    elif task_type == "palindrome":
        result = palindrome_check(text)
    else:
        result = "Unknown task"
    return {"client_id": client_id, "task": task_type, "result": result}

def worker_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5002))
    print("[Worker] Connected to broker.")

    pool = multiprocessing.Pool()

    while True:
        try:
            data = sock.recv(4096)
            if not data:
                continue
            task = pickle.loads(data)
            result = pool.apply(process_task, (task,))
            sock.sendall(pickle.dumps(result))
        except:
            continue

if __name__ == "__main__":
    worker_client()
