import random
import math


def miller_test(num, k=8):
    if num == 2 or num == 3:
        return True

    if num % 2 == 0:
        return False

    r, s = 0, num - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randrange(2, num - 1)
        x = pow(a, s, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False
    return True


def primary():
    bits = 256
    print("Not primary numbers\n")
    while True:
        prim_number = (random.randrange(2 ** (bits - 1), 2 ** bits))
        if not miller_test(prim_number):
            print(f"{prim_number}")
        else:
            return prim_number


def generete_key():
    while True:
        keys = []
        for _ in range(4):
            key = primary()
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys


def evclid_extended(first_number, second_number):
    if first_number == 0:
        return second_number, 0, 1
    else:
        div, koef_x, koef_y = evclid_extended(second_number % first_number, first_number)
    return div, koef_y - (second_number // first_number) * koef_x, koef_x


def mod_inverse(first_number, second_number):
    return list(evclid_extended(first_number, second_number))[1]


def rsa_key_pair(first_key, second_key):
    res = []
    n = first_key * second_key
    oiler = (first_key - 1) * (second_key - 1)
    e = random.randrange(2, oiler - 1)
    while math.gcd(e, oiler) != 1:
        e = random.randrange(2, oiler - 1)
    d = mod_inverse(e, oiler) % oiler
    res.append(d)
    res.append(n)
    res.append(e)
    return res


def encrypting(m, e, n):
    return pow(m, e, n)


def decryption(c, d, n):
    return pow(c, d, n)


def digital_sign(m, d, n):
    return pow(m, d, n)


def sign_check(m, s, e, n):
    return m == pow(s, e, n)


def key_send(k, d, e_1, n_1, n):
    k_1 = encrypting(k, e_1, n_1)
    s = digital_sign(k, d, n)
    s_1 = encrypting(s, e_1, n_1)
    return k_1, s_1


def key_receiving(key_1, s_1, d_1, n_1, e, n):
    key = decryption(key_1, d_1, n_1)
    s = decryption(s_1, d_1, n_1)
    if sign_check(key, s, e, n):
        return True, key
    else:
        return False, 0


gen_keys = generete_key()
p, q, p_1, q_1 = gen_keys[0], gen_keys[1], gen_keys[2], gen_keys[3]

rsa_keys_a = rsa_key_pair(p, q)
e, n, d = rsa_keys_a[0], rsa_keys_a[1], rsa_keys_a[2]

rsa_keys_b = rsa_key_pair(p_1, q_1)
e_1, n_1, d_1 = rsa_keys_b[0], rsa_keys_b[1], rsa_keys_b[2]


message = random.randint(0, n)
start_key = random.randint(0, n)
encrypted_key, dig_sign = key_send(start_key, d, e_1, n_1, n)

encrypted_msg = encrypting(message, e, n)
received_key = key_receiving(encrypted_key, dig_sign, d_1, n_1, e, n)
decrypted_msg = decryption(encrypted_msg, d, n)

print("\n㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛ Ключі персонажа А ㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛")
print(f'e: {e}\nn: {n}\nd: {d}\np: {p}\nq: {q}\n')

print("㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛ Ключі персонажа B ㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛㋛")
print(f'e_1: {e_1}\nn_1: {n_1}\nd_1: {d_1}\np_1: {p_1}\nq_1: {q_1}\n')
print(f'Start k: {start_key}\nMessage: {message}\n')


if received_key[0]:
    print(f'The key has been received: {received_key[1]}\n')
if not received_key[0]:
    print('Error getting the key')
print(f"Encrypted message: {encrypted_msg}\nDecrypted: message: {decrypted_msg}")
