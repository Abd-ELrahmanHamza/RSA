from rsa import RSA
import socket
import threading
from encryption import Encrypt
from decryption import Decrypt

# The Client class establishes a socket connection and sends/receives messages to/from a client.
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.137.1"
ADDR = (SERVER, PORT)


# This is a Python class that sets up a client socket connection, sends and receives encrypted
# messages using RSA encryption, and runs on separate threads for sending and receiving.
class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.rsa = RSA()
        self.myPublicKey = self.rsa.get_public_key()
        self.senderPublicKey = 0
        self.encrypt = Encrypt(self.senderPublicKey, self.rsa)
        self.decrypt = Decrypt(self.senderPublicKey, self.rsa)

        # Send my public key
        self.send(str(self.myPublicKey[0]) + "-" + str(self.myPublicKey[1]))
        public_key_message = self.receive()
        if public_key_message == "PUBLIC_KEY":
            self.senderPublicKey = self.receive()
            self.senderPublicKey = [int(strPub)
                                    for strPub in self.senderPublicKey.split("-")]

        self.send(DISCONNECT_MESSAGE)

        self.encrypt.set_sender_public_key(self.senderPublicKey)
        self.decrypt.set_sender_public_key(self.senderPublicKey)

        receive_thread = threading.Thread(target=self.client_receive)
        receive_thread.start()

        send_thread = threading.Thread(target=self.client_send)
        send_thread.start()

    def client_receive(self):
        """
        This function receives messages and decrypts them if they are not a public key.
        """
        while True:
            message = self.receive()
            if message == "PUBLIC_KEY":
                self.senderPublicKey = self.receive()
                self.senderPublicKey = [
                    int(strPub) for strPub in self.senderPublicKey.split("-")]
                self.encrypt.set_sender_public_key(self.senderPublicKey)
                self.decrypt.set_sender_public_key(self.senderPublicKey)
            else:
                if len(message) > 0 and message != "Msg received":
                    decrypted_message = self.decrypt.start_decrypt(message)
                    if decrypted_message is not None:
                        print(decrypted_message)

    def client_send(self):
        """
        This function continuously encrypts user input and sends the encrypted data to a server.
        """
        while True:
            encrypted_list = self.encrypt.start_encrypt(input(""))
            self.sendList(encrypted_list)

    def send(self, msg):
        """
        This function sends a message over a client socket connection by first encoding the message and
        sending its length followed by the message itself.

        :param msg: The message to be sent, which is a string
        """
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def receive(self):
        """
        This function receives a message from a client by first receiving the length of the message and then
        receiving the message itself.
        :return: a response message received from a client. The message is received in two parts: first, the
        length of the message is received and decoded using the specified format (HEADER), and then the
        actual message is received and decoded using the same format (FORMAT). The function returns the
        decoded message as a string.
        """
        response_message = ""
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            response_message = self.client.recv(msg_length).decode(FORMAT)
        return response_message

    def sendList(self, encrypted_list):
        """
        This function sends each message in an encrypted list and then disconnects.

        :param encrypted_list: The parameter "encrypted_list" is a list of encrypted messages that the
        function "sendList" is supposed to send. The function iterates through each message in the list and
        sends it using the "send" method. Once all messages have been sent, the function sends a
        "DISCONNECT_MESSAGE"
        """
        for message in encrypted_list:
            self.send(str(message))
        self.send(DISCONNECT_MESSAGE)


client = Client()
