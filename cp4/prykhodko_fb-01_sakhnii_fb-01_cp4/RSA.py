import random
import math
import egcd


def miller_rabin(p, k=32) -> bool:
    if any(p % i == 0 for i in [2, 3, 5, 7, 11]):
        return False
    else:
        s = 0
        d = p - 1
        while d % 2 == 0:
            s = s + 1
            d = d // 2

        for i in range(0, k):
            x = random.randrange(2, p)
            gcd = math.gcd(x, p)
            if gcd > 1:
                return False
            elif gcd == 1:
                a = pow(x, d, p)
                if a == 1 or a == -1:
                    return True
                else:
                    for r in range(1, s):
                        Xr = pow(x, d * (2 ** r), p)
                        if Xr == -1:
                            return True
                        if Xr == 1:
                            return False


def choose_prime_number(bit_size) -> int:
    N = (2 ** bit_size) - 1
    n = (2 ** (bit_size - 1)) - 1
    while True:
        x = random.randint(n, N)
        if x % 2 == 1:
            m = x
        else:
            m = x + 1
        composite_list = []
        for i in range(0, (N - m) // 2):
            possible_prime = m + (2 * i)
            if miller_rabin(possible_prime):
                prime_number = possible_prime
                # print(composite_list)
                return prime_number
            else:
                composite_list.append(possible_prime)


def generate_prime_pair(bit_size, quantity=1) -> list:
    prime_list = []
    for item in range(2 * quantity):
        prime_list.append(choose_prime_number(bit_size))
    return prime_list


def find_inverse_element(num, mod) -> int:
    gcd, x, y = egcd.egcd(num, mod)
    return x


def GenerateKeyPair(p, q) -> tuple:
    n = p * q
    fi_n = (p - 1) * (q - 1)
    e = random.randint(2, fi_n - 1)
    while math.gcd(e, fi_n) != 1:
        e = random.randrange(2, fi_n - 1)
    d = find_inverse_element(e, fi_n) % fi_n
    return e, n, d


def Encrypt(M, e, n) -> int:
    C = pow(M, e, n)
    return C


def Decrypt(C, d, n) -> int:
    M = pow(C, d, n)
    return M


def Sign(M, d, n) -> int:
    S = pow(M, d, n)
    return S


def Verify(M, S, e, n) -> bool:
    return M == pow(S, e, n)


def SendKey(K, e1, n1, d, n) -> tuple:
    K1 = Encrypt(K, e1, n1)
    S = Sign(K, d, n)
    S1 = Encrypt(S, e1, n1)
    return K1, S1


def ReceiveKey(K1, S1, d1, n1, e, n):
    K = Decrypt(K1, d1, n1)
    S = Decrypt(S1, d1, n1)
    if Verify(K, S, e, n):
        print("[♣]► Key was successfully received from authenticated user:", K, "\n")
    else:
        print("[!]► It doesn't matter what the key, because it was received from non-authenticated user.\n")
