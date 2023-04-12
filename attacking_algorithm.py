from rsa import RSA
import sympy
import time
import math

import matplotlib.pyplot as plt


def attack_RSA(E, N):

    prime_factors = sympy.primefactors(N)
    P = prime_factors[0]
    Q = prime_factors[1]
    # print("prime_factors : P =", P, " Q =", Q)

    phin = (P-1)*(Q-1)
    # print("Phi(N) =", phin)

    D = pow(E, -1, phin)
    return D


def attack(start_prime, end_prime):
    rsa = RSA(startPrime=start_prime, endPrime=end_prime)
    public_key = rsa.get_public_key()
    E = public_key[0]
    N = public_key[1]
    print("public_key : E =", E, " N =", N, " N =", bin(N))
    start_time = time.time()
    D = attack_RSA(E, N)
    end_time = time.time()

    print("private calculated key : D =", D)
    print("Actual private key =", rsa.get_private_key())
    return D, N, end_time - start_time


if __name__ == "__main__":
    execution_time_list = []
    number_of_bits_list = []
    number_of_bits = 4
    while number_of_bits <= 64:
        start_prime = int('1' + '0'*(number_of_bits-1), 2)
        end_prime = int('1' + '1'*(number_of_bits-1), 2)
        D, N, execution_time = attack(start_prime, end_prime)
        number_of_bits_list.append(int(math.log2(N)))
        execution_time_list.append(execution_time)
        print("Number of bits =", int(math.log2(N)))
        print("Time to attack in milliseconds =", (execution_time)*1000, "ms")
        print()
        number_of_bits *= 2

    # plot the execution time
    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(number_of_bits_list, execution_time_list)

    # Customize the plot
    ax.set_title("Number of bits in N vs Execution time in milliseconds")
    ax.set_xlabel("Number of bit in N")
    ax.set_ylabel("Execution time in milliseconds")

    # Display the plot
    plt.show()
