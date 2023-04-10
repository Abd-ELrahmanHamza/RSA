import sympy
import math


class RSA:
    def __init__(self):
        print("Here")
        self.P = sympy.randprime(100000, 1000000)  # 139273
        self.Q = sympy.nextprime(self.P)  # 139291
        self.E = 1  # 11
        self.D = 1  # 7054253411
        self.N = self.P * self.Q
        self.PHIN = (self.P - 1) * (self.Q - 1)
        self.generate_public_key()
        self.generate_private_key()
        print(self.P, self.Q, self.D, self.E, self.PHIN, self.N)

    def get_public_key(self):
        return (self.E, self.N)

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
