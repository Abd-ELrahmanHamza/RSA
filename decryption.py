import socket
import threading
import sympy

# These are variables used to configure the server.
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
P = 139273  # sympy.randprime(10000, 1000000)
Q = 139291  # sympy.nextprime(P)
E = 11
D = 7054253411
N = P * Q
PHIN = (P - 1) * (Q - 1)


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
        self.myServer = Server(callback=self.start_decrypt)
        print("[STARTING] server is starting...")
        self.myServer.start()

    def start_decrypt(self, message):
        print(message)
        if message == DISCONNECT_MESSAGE:
            self.messages = [int(message) for message in self.messages]
            decrypted_messages = self.decrypt()
            decoded_messages = self.decode(decrypted_messages)
            original_message = self.concatenate_list(decoded_messages)
            print("decrypted_messages = ", decrypted_messages)
            print("decoded_messages = ", decoded_messages)
            print("original_message = ", original_message)
        else:
            self.messages.append(message)

    def fast_power(self, base, exponent, modulus):
        result = 1
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            base = (base * base) % modulus
            exponent //= 2
        return result

    def RSA(self, message):
        return self.fast_power(message, D, N)

    def decrypt(self):
        decrypted_list = [self.RSA(message=message)
                          for message in self.messages]
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
                print(character)
                print(message % 37)
                string_message = string_message + character
                message = int(message / 37)
            print("string_message = ", string_message)
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


decryption = Decrypt()
