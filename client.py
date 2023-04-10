from rsa import RSA
import socket
import threading
from encryption import Encrypt

# The Client class establishes a socket connection and sends/receives messages to/from a client.
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.137.1"
ADDR = (SERVER, PORT)


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.alias = "New user"
        self.rsa = RSA()
        self.myPublicKey = self.rsa.get_public_key()
        self.senderPublicKey = 0

        # Send my public key
        self.send(str(self.myPublicKey[0]) + "-" + str(self.myPublicKey[1]))
        self.senderPublicKey = self.receive()
        self.senderPublicKey = [int(strPub) for strPub in self.senderPublicKey.split("-")]
        # print("senderPublicKey = ", self.senderPublicKey)
        self.send(DISCONNECT_MESSAGE)

        self.encrypt = Encrypt(self.senderPublicKey, self.rsa)
        receive_thread = threading.Thread(target=self.client_receive)
        receive_thread.start()

        send_thread = threading.Thread(target=self.client_send)
        send_thread.start()

    def client_receive(self):
        while True:
            try:
                message = self.receive()
                if message == "alias?":
                    client.send(self.alias.encode('utf-8'))
                else:
                    if len(message) > 0 and message != "Msg received":
                        print(message)
            except:
                print('Error!')
                self.client.close()
                break

    def client_send(self):
        while True:
            encrypted_list = self.encrypt.start_encrypt(input("Enter Message:"))
            self.sendList(encrypted_list)

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def receive(self):
        response_message = self.client.recv(2048).decode(FORMAT)
        return response_message

    def sendList(self, encrypted_list):
        for message in encrypted_list:
            self.send(str(message))
        self.send(DISCONNECT_MESSAGE)


client = Client()
