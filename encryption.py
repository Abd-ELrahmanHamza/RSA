import socket
import numpy as np

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


class Encrypt:
    def __init__(self):
        self.myClient = Client()

    def sendMessage(self, message):
        """
        This function sends a message and a disconnect message through a client connection.

        :param message: The message that the client wants to send to the server
        """
        self.myClient.send(message)

    def encrypt(self, message):
        # Note the string is reversed
        string_list = self.splitString(message[::-1])
        print(string_list)
        encoded_list = self.encode(string_list)
        print(encoded_list)
        self.sendList(encoded_list)
        pass

    def splitString(self, str):
        """
        The function splits a given string into a list of substrings of length 5, padding the last substring
        with spaces if necessary.

        :param str: The input string that needs to be split into chunks of 5 characters each
        :return: The function `splitString` takes a string as input and returns a list of strings where each
        string has a maximum length of 5 characters. If the last string in the list has less than 5
        characters, it is padded with spaces to make it 5 characters long.
        """
        string_list = [str[i:i+5] for i in range(0, len(str), 5)]
        string_list[-1] = string_list[-1] + (5-len(string_list[-1]))*' '
        return string_list

    def encode(self, string_list):
        encoded_list = []
        for str in string_list:
            summation = 0
            for i in range(5):
                if str[i].isalpha():
                    summation += (ord(str[i])-ord('a')+10) * (37**i)
                elif str[i].isnumeric():
                    summation += (ord(str[i])-ord('0')) * (37**i)
                else:
                    summation += (36) * (37**i)
            encoded_list.append(summation)
        return encoded_list

    def sendList(self, encrypted_list):
        for message in encrypted_list:
            self.sendMessage(str(message))
        self.myClient.send(DISCONNECT_MESSAGE)


encryption = Encrypt()
encryption.encrypt("hello world hi s7")
# encryption.sendMessage("Hello Abdelrahman! world world")
