# client.py
import socket
import pickle
import uuid

def send_task(task_type, text, client_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('10.0.0.197', 5000))
    task = (task_type, text, client_id)
    sock.sendall(pickle.dumps(task))
    print(f"\n[Client {client_id}] Sent {task_type} task. Waiting for result...")

    result_data = sock.recv(4096)
    result = pickle.loads(result_data)
    print(f"[Client {client_id}] Result: {result['task']} → {result['result']}")
    sock.close()

if __name__ == "__main__":
    print("=== Text Utilities Client ===")
    print("Available tasks:")
    print("  1. wordcount")
    print("  2. linecount")
    print("  3. palindrome")
    print("-----------------------------")

    task_type = input("Enter task type: ").strip().lower()
    while task_type not in ["wordcount", "linecount", "palindrome"]:
        print("Invalid task type. Try again.")
        task_type = input("Enter task type: ").strip().lower()

    print("\nEnter your text below (press ENTER twice when done):")
    print("(Tip: You can paste multiple lines)")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    text_data = "\n".join(lines)

    client_id = str(uuid.uuid4())[:8]  # short random ID
    send_task(task_type, text_data, client_id)

