import socket

# These are variables that are used to configure the socket connection.
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.137.1"
ADDR = (SERVER, PORT)


# The Client class establishes a socket connection and sends/receives messages to/from a client.
class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

    def send(self, msg):
        """
        This function sends a message to a client and receives a response.

        :param msg: The message to be sent to the client. It should be a string
        """
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(FORMAT))


myClient = Client()
myClient.send("Hello Abdelrahman!")
input()
myClient.send("Hello Everyone!")
input()
myClient.send("Hello Tim!")

myClient.send(DISCONNECT_MESSAGE)
