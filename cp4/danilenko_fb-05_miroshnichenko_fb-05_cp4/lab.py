import random
import math


class RSA:
    def __init__(self, p: int, q: int):
        self.p = p
        self.q = q
        self.e, self.n, self.d = self.generate_rsa(self.p, self.q)

    def extended_euclid(self, first_num: int, second_num: int) -> (int, int, int):
        if second_num == 0:
            return first_num, 1, 0
        d, x, y = self.extended_euclid(second_num, first_num % second_num)
        return d, y, x - (first_num // second_num) * y

    def inverse_mod(self, first_num: int, second_num: int) -> int:
        return self.extended_euclid(first_num, second_num)[1]

    def generate_rsa(self, first_key: int, second_key: int) -> (int, int, int):
        n = first_key * second_key
        phi = (first_key - 1) * (second_key - 1)
        e = random.randrange(2, phi - 1)
        while math.gcd(e, phi) != 1:
            e = random.randrange(2, phi - 1)
        d = self.inverse_mod(e, phi) % phi
        return d, n, e


class Client:
    def __init__(self, p: int, q: int):
        self.RSA = RSA(p, q)

    def Encrypt(M, e, n):
        C = pow(M, e, n)
        return C

    def Decrypt(C, d, n):
        M = pow(C, d, n)
        return M

    def Sign(M, d, n):
        S = pow(M, d, n)
        return S

    def Verify(M, S, e, n):
        return M == pow(S, e, n)

    def SendKey(k, n):
        K1 = pow(k, e1, n1)
        S = pow(k, d, n)
        S1 = pow(S, e1, n1)

        return K1, S1

    def ReceiveKey(K1, S1, d1, n1, e, n):
        K = pow(K1, d1, n1)
        print('Розшифрований k = ', k, '\n')
        S = pow(S1, d1, n1)

        if pow(K, S, e, n):
            print('Ключ отримано\n')
            return K
        else:
            print('Ключ не вдалося отримати')

    def authentication(S, e, n):
        k = pow(S, e, n)
        return k


def is_probably_prime(num: int, count: int = 10) -> bool:
    if num in (2, 3):
        return True
    if num == 1 or num % 2 == 0:
        return False

    s = num - 1
    r = 0
    while s % 2 == 0:
        s //= 2
        r += 1

    for _ in range(count):
        a = random.randint(2, num - 2)
        x = pow(a, s, num)
        if x == 1:
            continue
        for _ in range(r):
            if x == num - 1:
                break
            x = (x * x) % num
        else:
            return False
    return True

def generate_prime(self, bit_len: int) -> int:
    while True:
        number = (random.randrange(2 ** (bit_len - 1), 2 ** bit_len))
        if self.is_probably_prime(number):
            return number

def generate_key(self) -> (int, int, int, int):
    while True:
        keys = []
        for i in range(0, 4):
            key = self.generate_prime(256)
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys[0], keys[1], keys[2], keys[3]


p, q, p_1, q_1 = generate_key()
print(f"p = {p}, q = {q}")
print(f"p_1 = {p_1}, q_1 = {q_1}")
print()
print('RSA')
e, n, d = generate_rsa(p, q)
print(f'e = {e}')
print(f'n = {n}')
print(f'd = {d}')

e_1, n_1, d_1 = generate_rsa(p_1, q_1)
print(f'e_1 = {e_1}')
print(f'n_1 = {n_1}')
print(f'd_1 = {d_1}')

