import socket
import threading

# These are variables used to configure the server.
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class Server:
    def __init__(self, callback, privateKeyCallback, public_key):
        self.public_key = public_key
        self.privateKeyCallback = privateKeyCallback
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.callback = callback
        self.aliases = []
        self.clients = []

    def handle_client(self, conn, addr):
        """
        This function handles a client connection by receiving and sending messages until the client
        disconnects.

        :param conn: conn is a socket object representing the connection between the server and the client.
        It is used to send and receive data between the two endpoints
        :param addr: The address of the client that has connected to the server. It is a tuple containing
        the IP address and the port number of the client
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
                    conn.send("Msg received".encode(FORMAT))
                else:
                    print(f"[{addr}] {msg}")
                    self.privateKeyCallback(msg)
                    conn.send(self.public_key.encode(FORMAT))
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                # if msg == DISCONNECT_MESSAGE:
                #     connected = False

                print(f"[{addr}] {msg}")
                self.callback(msg)
                conn.send("Msg received".encode(FORMAT))
        conn.close()

    def start(self):
        """
        This function starts a server that listens for incoming connections and creates a new thread to
        handle each client connection.
        """
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
