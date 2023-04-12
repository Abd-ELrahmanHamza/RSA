import sympy
import math


class RSA:
    def __init__(self, startPrime=100000, endPrime=10000000):
        self.P = 1  # sympy.randprime(100000, 1000000)  # 139273
        self.Q = 1  # sympy.nextprime(self.P)  # 139291
        self.E = 1  # 11
        self.D = 1  # 7054253411
        self.generatePrimes(startPrime, endPrime)
        self.N = self.P * self.Q
        self.PHIN = (self.P - 1) * (self.Q - 1)
        self.generate_public_key()
        self.generate_private_key()
        print(self.P, self.Q, self.D, self.E, self.PHIN, self.N)

    def generatePrimes(self, startPrime, endPrime):
        self.P = sympy.randprime(startPrime, endPrime)
        self.Q = sympy.randprime(startPrime, endPrime)
        while self.P == self.Q:
            self.Q = sympy.randprime(startPrime, endPrime)

    def get_public_key(self):
        return (self.E, self.N)

    def get_private_key(self):
        return self.D

    def generate_public_key(self):
        for i in range(2, self.PHIN):
            if math.gcd(i, self.PHIN) == 1:
                self.E = i
                break

    def generate_private_key(self):
        self.D = pow(self.E, -1, self.PHIN)

    def fast_power(self, base, exponent, modulus):
        result = 1
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            base = (base * base) % modulus
            exponent //= 2
        return result

    def RSA(self, message, exponent, N):
        return self.fast_power(message, exponent, N)
