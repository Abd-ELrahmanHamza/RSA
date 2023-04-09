from server import Server
from rsa import RSA

# These are variables used to configure the server.
DISCONNECT_MESSAGE = "!DISCONNECT"


# This is a Python class that creates a server that listens for incoming connections and handles each
# client connection in a separate thread.


class Decrypt:
    def __init__(self):
        self.rsa = RSA()
        self.senderPublicKey = 0
        self.myPublicKey = self.rsa.get_public_key()
        self.messages = []
        self.myServer = Server(self.start_decrypt, self.privateKeyCallback,
                               str(self.myPublicKey[0]) + "-" + str(self.myPublicKey[1]))
        print("[STARTING] server is starting...")
        self.myServer.start()

    def start_decrypt(self, message):
        print(message)
        if message == DISCONNECT_MESSAGE:
            self.messages = [int(message) for message in self.messages]
            decrypted_messages_private = self.decrypt(self.messages, self.rsa.D, self.rsa.N)
            decrypted_messages_public = self.decrypt(
                decrypted_messages_private, self.senderPublicKey[0], self.senderPublicKey[1])
            decoded_messages = self.decode(decrypted_messages_public)
            original_message = self.concatenate_list(decoded_messages)
            print("decrypted_messages_private = ", decrypted_messages_private)
            print("decrypted_messages_public = ", decrypted_messages_public)
            print("decoded_messages = ", decoded_messages)
            print("original_message = ", original_message)
            self.messages.clear()
        else:
            self.messages.append(message)

    def decrypt(self, messages, exponent, N):
        decrypted_list = [self.rsa.RSA(message, exponent, N) for message in messages]
        return decrypted_list

    def decode(self, decrypted_messages):
        """
        The function decodes a list of messages using a specific algorithm and returns the decoded messages
        as a list of strings.
        :return: a list of decoded messages, where each message is a string obtained by decoding the
        corresponding message in the input list using a specific algorithm.
        """
        decoded_messages = []
        for message in decrypted_messages:
            string_message = ""
            while message:
                character = message % 37
                if character < 10:
                    character = chr(character + ord('0'))
                elif character == 36:
                    character = ' '
                else:
                    character = chr(character + ord('a') - 10)
                string_message = string_message + character
                message = int(message / 37)
            decoded_messages.append(string_message)
        return decoded_messages

    def concatenate_list(self, decoded_messages):
        """
        This function concatenates a list of decoded messages, removes any trailing whitespace, and returns
        the resulting string in reverse order.

        :param decoded_messages: decoded_messages is a list of strings that represent decoded messages. The
        function concatenates all the strings in the list, removes any trailing whitespace, and returns the
        resulting string in reverse order
        :return: a concatenated string of all the elements in the input list `decoded_messages`, with any
        trailing whitespace removed and the order of the characters reversed.
        """
        return ("".join(decoded_messages)).rstrip()[::-1]

    def privateKeyCallback(self, senderPublicKey):
        self.senderPublicKey = [int(strPub) for strPub in senderPublicKey.split("-")]
        print("self.senderPublicKey", self.senderPublicKey)


decryption = Decrypt()
