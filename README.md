Text Utilities Cluster
A distributed text processing application demonstrating multiprocessing, multithreading, interprocess communication, and TCP/IP-based distributed computing.

Clients send text processing tasks to a controller, which distributes them through a message broker to worker processes. Workers compute results and send them back to the controller for the client.

Features
Multithreading: Controller handles multiple client connections simultaneously.
Multiprocessing: Worker processes handle multiple tasks in parallel using all CPU cores.
Distributed computing simulation: Controller, broker, workers, and clients run as separate scripts simulating nodes.
Interprocess communication: Broker manages task and result queues for workers.
Message broker: Ensures reliable communication between controller and workers.
Internode communication: TCP/IP sockets connect all nodes.
User input: Clients can choose task type (wordcount, linecount, palindrome) and input text dynamically.
Project Structure
text_cluster/
│
├── client.py        # User interface for submitting tasks
├── controller.py    # Multithreaded server handling clients and broker communication
├── broker.py        # Routes tasks and results between controller and workers
├── worker.py        # Multiprocessing worker handling text tasks
└── README.md        # Project documentation
Getting Started
Prerequisites
Python 3.8+
No external libraries required (uses socket, threading, multiprocessing, pickle, uuid)
Setup & Run
Open 4 terminals in VS Code (or CMD).

Start Broker:

python broker.py
Start Worker:
python worker.py
Start Controller:
python controller.py
Start Client(s):
python client.py
Follow the prompts to enter:

Task type: wordcount, linecount, or palindrome
Text to process
💡 You can open multiple client terminals to simulate multiple users connecting simultaneously.

Demo Example
Client Input:

Enter task type: palindrome
Enter text:
madam
Client Output:

[Client 1a2b3c4d] Sent palindrome task. Waiting for result...
[Client 1a2b3c4d] Result: palindrome → True
Multiple clients can run concurrently to demonstrate multithreading.
Worker processes run tasks in parallel to demonstrate multiprocessing.
How It Works
Client sends task + text to the controller over TCP.
Controller assigns each client connection to a thread.
Controller forwards the task to the broker, which queues it for workers.
Workers fetch tasks from the broker, process them using a multiprocessing pool, and send results back.
Broker sends results to the controller, which forwards them back to the client.
Tasks Implemented
wordcount → Counts total words in the text.
linecount → Counts total lines in the text.
palindrome → Checks if the text is a palindrome (ignores spaces and punctuation).
Notes
Designed to run on one machine for testing/demo purposes.
Each script simulates a separate node in a distributed system.
Fully demonstrates multithreading, multiprocessing, interprocess communication, and message brokering.
