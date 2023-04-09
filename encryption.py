from client import Client
from rsa import RSA

# These are variables that are used to configure the socket connection.
DISCONNECT_MESSAGE = "!DISCONNECT"


class Encrypt:
    def __init__(self):
        self.myClient = Client()
        self.rsa = RSA()
        self.myPublicKey = self.rsa.get_public_key()
        self.senderPublicKey = 0

    def start_encrypt(self, message):
        # Send my public key
        self.senderPublicKey = self.sendMessage(str(self.myPublicKey[0]) + "-" + str(self.myPublicKey[1]))
        self.senderPublicKey = [int(strPub) for strPub in self.senderPublicKey.split("-")]
        print("senderPublicKey = ", self.senderPublicKey)
        self.myClient.send(DISCONNECT_MESSAGE)

        # Note the string is reversed
        string_list = self.splitString(message[::-1])
        encoded_list = self.encode(string_list)
        encrypted_list_private = self.encrypt(
            encoded_list, self.rsa.D, self.rsa.N)
        encrypted_list_public = self.encrypt(
            encrypted_list_private, self.senderPublicKey[0], self.senderPublicKey[1])
        print(string_list)
        print(encoded_list)
        print(encrypted_list_private)
        print(encrypted_list_public)
        self.sendList(encrypted_list_public)

    def splitString(self, str):
        """
        The function splits a given string into a list of substrings of length 5, padding the last substring
        with spaces if necessary.

        :param str: The input string that needs to be split into chunks of 5 characters each
        :return: The function `splitString` takes a string as input and returns a list of strings where each
        string has a maximum length of 5 characters. If the last string in the list has less than 5
        characters, it is padded with spaces to make it 5 characters long.
        """
        string_list = [str[i:i + 5] for i in range(0, len(str), 5)]
        string_list[-1] = string_list[-1] + (5 - len(string_list[-1])) * ' '
        return string_list

    def encode(self, string_list):
        encoded_list = []
        for str in string_list:
            summation = 0
            for i in range(5):
                if str[i].isalpha():
                    summation += (ord(str[i]) - ord('a') + 10) * (37 ** i)
                elif str[i].isnumeric():
                    summation += (ord(str[i]) - ord('0')) * (37 ** i)
                else:
                    summation += (36) * (37 ** i)
            encoded_list.append(summation)
        return encoded_list

    def encrypt(self, encoded_list, exponent, N):
        encrypted_list = [self.rsa.RSA(message, exponent, N)
                          for message in encoded_list]
        return encrypted_list

    def sendMessage(self, message):
        """
        This function sends a message using a client object.

        :param message: The message parameter is a string that represents the message that the client wants
        to send. It could be any text-based message that the client wants to transmit to the server or
        another client
        """
        return self.myClient.send(message)

    def sendList(self, encrypted_list):
        """
        This function sends each message in an encrypted list and then disconnects the client.

        :param encrypted_list: A list of encrypted messages that are to be sent by the client
        """
        for message in encrypted_list:
            self.sendMessage(str(message))
        self.myClient.send(DISCONNECT_MESSAGE)


encryption = Encrypt()
encryption.start_encrypt("hloaaaaaaaa 23190821")
# encryption.sendMessage("Hello Abdelrahman! world world")
