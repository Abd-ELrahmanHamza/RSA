import sympy
import math


class RSA:
    def __init__(self):
        self.P = 139273  # sympy.randprime(10000, 1000000)  # 139273
        self.Q = 139291  # sympy.nextprime(self.P)  # 139291
        self.E = 11
        self.D = 7054253411
        self.N = self.P * self.Q
        self.PHIN = (self.P - 1) * (self.Q - 1)

    def generate_public_key(self):
        for i in range(2, self.PHIN):
            if math.gcd(i, self.PHIN) == 1:
                self.E = i
                break

    def generate_public_key(self):
        pass

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
