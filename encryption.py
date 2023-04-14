# The `Encrypt` class contains methods for encrypting and encoding messages using RSA encryption.
class Encrypt:
    def __init__(self, senderPublicKey, rsa):
        self.senderPublicKey = senderPublicKey
        self.rsa = rsa

# The Decrypt class contains methods for decrypting and decoding messages using RSA encryption.
    def set_sender_public_key(self, senderPublicKey):
        """
        This function sets the sender's public key in an object.

        :param senderPublicKey: The parameter `senderPublicKey` is a variable that represents the public key
        of the sender in a cryptographic system. The `set_sender_public_key` function takes this public key
        as an argument and sets it as an attribute of the object that the function is called on. This
        function is typically used in a
        """
        self.senderPublicKey = senderPublicKey

    def start_encrypt(self, message):
        """
        This function takes a message, reverses it, splits it into a list, encodes the list, and encrypts it
        using a public key.

        :param message: The message to be encrypted as a string
        :return: The function `start_encrypt` is returning the `encrypted_list_public` which is the
        encrypted version of the input `message` using the sender's public key.
        """
        # Note the string is reversed
        string_list = self.splitString(message[::-1])
        encoded_list = self.encode(string_list)
        # encrypted_list_private = self.encrypt(
        #     encoded_list, self.rsa.D, self.rsa.N)
        # print("2", encrypted_list_private)
        encrypted_list_public = self.encrypt(
            encoded_list, self.senderPublicKey[0], self.senderPublicKey[1])
        return encrypted_list_public

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
        """
        The function encodes a list of strings into a list of integers using a specific algorithm.

        :param string_list: a list of strings that need to be encoded using a specific algorithm
        :return: an encoded list of integers, where each integer represents a string from the input string
        list. The encoding is done by converting each character in the string to a base-37 number and then
        summing up the values of these numbers multiplied by powers of 37.
        """
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
        """
        This function encrypts a list of encoded messages using RSA encryption with a given exponent and
        modulus.

        :param encoded_list: A list of integers representing encoded messages that need to be encrypted
        using RSA encryption
        :param exponent: The exponent is a parameter used in the RSA encryption algorithm to generate the
        public and private keys. It is a positive integer that is part of the public key and is used to
        encrypt messages. The exponent is typically a small prime number, such as 3 or 65537
        :param N: N is the modulus used in the RSA encryption algorithm. It is the product of two large
        prime numbers and is used to generate the public and private keys
        :return: an encrypted list of messages using the RSA encryption algorithm with the given exponent
        and modulus (N).
        """
        encrypted_list = [self.rsa.RSA(message, exponent, N)
                          for message in encoded_list]
        return encrypted_list
