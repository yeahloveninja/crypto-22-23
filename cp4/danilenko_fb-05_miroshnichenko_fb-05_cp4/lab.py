import random
import math


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


def extended_euclid(first_num: int, second_num: int) -> (int, int, int):
    if second_num == 0:
        return first_num, 1, 0
    d, x, y = extended_euclid(second_num, first_num % second_num)
    return d, y, x - (first_num // second_num) * y


def inverse_mod(first_num: int, second_num: int) -> int:
    return extended_euclid(first_num, second_num)[1]


def generate_rsa(p: int, q: int) -> (int, int, int):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randrange(2, phi - 1)
    d = inverse_mod(e, phi) % phi
    return d, n, e


p, q, p_1, q_1 = generate_key()
print(f"p = {p}, q = {q}")
print(f"p_1 = {p_1}, q_1 = {q_1}")
