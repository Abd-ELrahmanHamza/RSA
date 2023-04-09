class RSA:
    def __init__(self):
        self.P = 139273  # sympy.randprime(10000, 1000000)
        self.Q = 139291  # sympy.nextprime(P)
        self.E = 11
        self.D = 7054253411
        self.N = self.P * self.Q
        self.PHIN = (self.P - 1) * (self.Q - 1)

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
