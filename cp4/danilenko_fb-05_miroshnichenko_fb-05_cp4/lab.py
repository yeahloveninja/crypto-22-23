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

    def send_key(self, msg: int, e1: int, n1: int) -> (int, int):
        encrypt_msg = pow(msg, e1, n1)
        sign = pow(msg, self.RSA.d, self.RSA.n)
        encrypt_sign = pow(sign, e1, n1)

        return encrypt_msg, encrypt_sign

    def receive_key(self, encrypt_msg: int, encrypt_sign: int, e: int, n: int) -> int:
        msg = pow(encrypt_msg, self.RSA.d, self.RSA.n)
        sign = pow(encrypt_sign, self.RSA.d, self.RSA.n)

        if pow(sign, e, n):
            print('Key matched!')
            return msg
        else:
            print('Key did not match!')


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


def generate_prime(bit_len: int) -> int:
    while True:
        number = (random.randrange(2 ** (bit_len - 1), 2 ** bit_len))
        if is_probably_prime(number):
            return number


def generate_key() -> (int, int, int, int):
    while True:
        keys = []
        for i in range(0, 4):
            key = generate_prime(256)
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys[0], keys[1], keys[2], keys[3]


p, q, p_1, q_1 = generate_key()
first_cli = Client(p, q)
second_cli = Client(p_1, q_1)
message, message_sign = first_cli.send_key(14, second_cli.RSA.e, second_cli.RSA.n)
result = second_cli.receive_key(message, message_sign, first_cli.RSA.e, first_cli.RSA.n)
print(f'Message - {result}')
