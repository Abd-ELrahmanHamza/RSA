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
        self.send(msg, client)

    def handle_client(self, conn, addr):
        """
        This function handles a client connection, sends and receives messages, and broadcasts messages
        to other clients.

        :param conn: conn is a socket object representing the connection between the server and the
        client. It is used to send and receive data between the two endpoints
        :param addr: The address of the client that has connected to the server. It is a tuple
        containing the IP address and the port number of the client
        """
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
                        self.send("PUBLIC_KEY", conn)
                        self.send(self.clients_public_keys[0], conn)

                        self.send("PUBLIC_KEY", self.clients[0])
                        self.send(msg, self.clients[0])
                    else:
                        print("xxxxxx N0 sending public key")
                        self.send("NO_PUBLIC_KEY", conn)
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

    def send(self, msg, client):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)


# This is a Python class that creates a server that listens for incoming connections and handles each
# client connection in a separate thread.
myServer = Server()
print("[STARTING] server is starting...")
myServer.start()
