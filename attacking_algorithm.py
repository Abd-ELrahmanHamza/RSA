from rsa import RSA
import sympy


def attack_RSA():
    rsa = RSA()
    public_key = rsa.get_public_key()
    print("public_key = ", public_key)

    prime_factors = sympy.primefactors(public_key[1])
    print("prime_factors = ", prime_factors)

    phin = (prime_factors[0]-1)*(prime_factors[1]-1)
    d = pow(public_key[0], -1, phin)
    print("private key = ", d)


attack_RSA()
