from rsa import RSA

DISCONNECT_MESSAGE = "!DISCONNECT"


class Decrypt:
    def __init__(self, senderPublicKey, rsa):
        self.rsa = rsa
        self.senderPublicKey = senderPublicKey
        self.myPublicKey = self.rsa.get_public_key()
        self.messages = []

    def set_sender_public_key(self, senderPublicKey):
        self.senderPublicKey = senderPublicKey

    def start_decrypt(self, message):
        print("received", message)
        print("separator")
        res = []
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
            res = self.messages.copy()
            self.messages.clear()
            return res
        else:
            self.messages.append(message)

    def decrypt(self, messages, exponent, N):
        decrypted_list = [self.rsa.RSA(message, exponent, N) for message in messages]
        return decrypted_list

    def decode(self, decrypted_messages):
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
        return ("".join(decoded_messages))[::-1]
