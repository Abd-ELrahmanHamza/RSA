import socket
import threading

# These are variables used to configure the server.
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


# This is a Python class that creates a server that listens for incoming connections and handles each
# client connection in a separate thread.
class Server:
    def __init__(self, callback):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.callback = callback

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
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False

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


class Decrypt:
    def __init__(self):
        self.messages = []
        self.myServer = Server(callback=self.decrypt)
        print("[STARTING] server is starting...")
        self.myServer.start()

    def decrypt(self, message):
        print(message)
        if message == DISCONNECT_MESSAGE:
            self.messages = [int(message) for message in self.messages]
            decoded_messages = self.decode()
            original_message = self.concatenate_list(decoded_messages)
            print("decoded_messages = ", decoded_messages)
            print("original_message = ", original_message)
        else:
            self.messages.append(message)

    def decode(self):
        decoded_messages = []
        for message in self.messages:
            string_message = ""
            while message:
                character = message % 37
                if character < 10:
                    character = chr(character+ord('0'))
                elif character == 36:
                    character = ' '
                else:
                    character = chr(character+ord('a')-10)
                print(character)
                print(message % 37)
                string_message = string_message + character
                message = int(message/37)
            print("string_message = ", string_message)
            decoded_messages.append(string_message)
        return decoded_messages

    def concatenate_list(self, decoded_messages):
        return ("".join(decoded_messages)).rstrip()[::-1]


decryption = Decrypt()
