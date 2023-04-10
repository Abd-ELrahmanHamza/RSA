class Encrypt:
    def __init__(self, senderPublicKey, rsa):
        self.senderPublicKey = senderPublicKey
        self.rsa = rsa

    def set_sender_public_key(self, senderPublicKey):
        self.senderPublicKey = senderPublicKey

    def start_encrypt(self, message):
        # Note the string is reversed
        string_list = self.splitString(message[::-1])
        encoded_list = self.encode(string_list)
        encrypted_list_private = self.encrypt(
            encoded_list, self.rsa.D, self.rsa.N)
        encrypted_list_public = self.encrypt(
            encrypted_list_private, self.senderPublicKey[0], self.senderPublicKey[1])
        # print(string_list)
        # print(encoded_list)
        # print(encrypted_list_private)
        # print(encrypted_list_public)
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
