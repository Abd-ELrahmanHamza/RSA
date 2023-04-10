import socket
import threading
from encryption import Encrypt

# These are variables used to configure the server.
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.aliases = []
        self.clients = []
        self.clients_public_keys = []

    def broadcast(self, msg, client):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        print(f"[SENDING] PUBLIC KEY.")
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] {msg}")
                else:
                    print(f"[{addr}] {msg}")
                    if len(self.clients_public_keys) != 0:
                        print("==========sending public key")
                        message = "PUBLIC_KEY".encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        conn.send(send_length)
                        conn.send(message)

                        message = self.clients_public_keys[0].encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        conn.send(send_length)
                        conn.send(message)

                        message = "PUBLIC_KEY".encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        self.clients[0].send(send_length)
                        self.clients[0].send(message)

                        message = msg.encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        self.clients[0].send(send_length)
                        self.clients[0].send(message)
                    else:
                        print("xxxxxx N0 sending public key")
                        message = "NO_PUBLIC_KEY".encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        conn.send(send_length)
                        conn.send(message)
                    self.clients_public_keys.append(msg)
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"[{addr}] {msg}")
                self.broadcast(msg, self.clients[1 - self.clients.index(conn)])
        conn.close()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


# This is a Python class that creates a server that listens for incoming connections and handles each
# client connection in a separate thread.
myServer = Server()
print("[STARTING] server is starting...")
myServer.start()
