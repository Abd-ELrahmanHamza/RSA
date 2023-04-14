from rsa import RSA

DISCONNECT_MESSAGE = "!DISCONNECT"


# The Decrypt class contains methods for decrypting and decoding messages using RSA encryption.
class Decrypt:
    def __init__(self, senderPublicKey, rsa):
        self.rsa = rsa
        self.senderPublicKey = senderPublicKey
        self.messages = []

    def set_sender_public_key(self, senderPublicKey):
        """
        This function sets the sender public key attribute of an object to a given value.
        
        :param senderPublicKey: The parameter `senderPublicKey` is a variable that represents the public key
        of the sender in a cryptographic system. The `set_sender_public_key` function takes this public key
        as an argument and sets it as an attribute of the object that the function is called on. This
        function is typically used in a
        """
        self.senderPublicKey = senderPublicKey

    def start_decrypt(self, message):
        """
        The function decrypts a message using RSA encryption and returns the original message.
        
        :param message: The message to be decrypted or added to the list of messages to be decrypted. If the
        message is equal to the DISCONNECT_MESSAGE, the function will decrypt all the messages in the list
        and return the original message
        :return: If the message is equal to DISCONNECT_MESSAGE, the original message is returned after
        decrypting and decoding it. Otherwise, nothing is returned.
        """
        res = []
        if message == DISCONNECT_MESSAGE:
            self.messages = [int(message) for message in self.messages]
            decrypted_messages_private = self.decrypt(
                self.messages, self.rsa.D, self.rsa.N)
            # decrypted_messages_public = self.decrypt(decrypted_messages_private, self.senderPublicKey[0], self.senderPublicKey[1])
            decoded_messages = self.decode(decrypted_messages_private)
            original_message = self.concatenate_list(decoded_messages)
            self.messages.clear()
            return original_message
        else:
            self.messages.append(message)

    def decrypt(self, messages, exponent, N):
        """
        This function decrypts a list of messages using RSA encryption with a given exponent and modulus.
        
        :param messages: A list of encrypted messages that need to be decrypted
        :param exponent: The exponent is a part of the RSA encryption algorithm and is used to encrypt and
        decrypt messages. It is a positive integer that is kept secret by the owner of the private key. In
        the context of this function, the exponent is used to decrypt a list of messages that have been
        encrypted using the RSA
        :param N: N is the product of two large prime numbers used in the RSA encryption algorithm to
        generate the public and private keys. It is a part of the public key and is used to encrypt messages
        :return: a list of decrypted messages using the RSA algorithm with the given exponent and modulus.
        """
        decrypted_list = [self.rsa.RSA(message, exponent, N)
                          for message in messages]
        return decrypted_list

    def decode(self, decrypted_messages):
        """
        This function decodes a list of decrypted messages using a specific algorithm.
        
        :param decrypted_messages: a list of integers representing decrypted messages in a specific encoding
        scheme
        :return: a list of decoded messages, where each message is a string obtained by decoding a given
        integer using a specific algorithm. The input to the function is a list of integers representing
        encrypted messages, and the output is a list of strings representing the corresponding decrypted
        messages.
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
