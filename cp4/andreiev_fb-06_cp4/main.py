import random


def ext_gcd(a, b):
    if a == 0:
        x = 0
        y = 1
        return (abs(b), x, y)
    else:
        gcd, y, x = ext_gcd(b % a, a)
        x = x - (b // a) * y
        return (gcd, x, y)


def inverse_mod(a, m):
    gcd, x, y = ext_gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        return 0


def simple_prime_check(num):
    return all([(num % i) != 0 for i in [2, 3, 5, 7, 11, 13, 17]])


def miller_rabin_test(num):

    if simple_prime_check(num) is False:
        return False
    else:
        d = num - 1
        s = 0

        while d % 2 == 0:
            s += 1
            d //= 2

        for k in range(100):
            x = random.randint(2, num)
            gcd = ext_gcd(x, num)[0]
            if gcd > 1:
                return False
            if gcd == 1:
                a = pow(x, d, num)
                if a == 1 or a == -1:
                    return True
                else:
                    for r in range(1, s):
                        xr = pow(x, (2 ** r) * d, num)
                        if xr == -1:
                            return True
                        if xr == 1:
                            return False
            else:
                return False


def get_rand_prime(range_min, range_max):
    while True:
        num = random.randint(range_min, range_max)
        if miller_rabin_test(num):
            return num


def get_keys(range_min, range_max):
    while True:
        p, q, p1, q1 = get_rand_prime(range_min, range_max), get_rand_prime(range_min, range_max), get_rand_prime(range_min, range_max), get_rand_prime(range_min, range_max)
        if (p * q) < (p1 * q1):
            return p, q, p1, q1


def generate_keys(p, q):
    n = p * q
    fi_n = (p - 1)*(q - 1)
    while True:
        e = random.randint(2, fi_n)
        if ext_gcd(e, fi_n)[0] == 1:
            d = inverse_mod(e, fi_n)
            return ((n, e), (d, p, q))
            

def encrypt_rsa(open_text, pub_key):
    n, e = pub_key
    return pow(open_text, e, n)


def decrypt_rsa(cipher_text, private_key):
    d, p, q = private_key
    n = p * q
    return pow(cipher_text, d, n)


def create_sign_rsa(open_text, private_key):
    d, p, q = private_key
    n = p * q
    return pow(open_text, d, n)


def verify_sign_rsa(S, M, pub_key):
    n, e = pub_key
    if pow(S, e, n) == M:
        print("Verification success")
    else:
        print("Verification fail")


def send_message(sender_open_key, sender_private_key, reciever_open_key, k):
    n, e = sender_open_key
    n1, e1 = reciever_open_key
    d = sender_private_key[0]
    s = pow(k, d, n)

    k1 = pow(k, e1, n1)
    s1 = pow(s, e1, n1)
    return k1, s1


def recieve_message(sender_open_key, reciever_private_key, reciever_open_key, message):
    n, e = sender_open_key
    n1, e1 = reciever_open_key
    d1 = reciever_private_key[0]
    k1, s1 = message

    k = pow(k1, d1, n1)
    s = pow(s1, d1, n1)

    sign = pow(s, e, n)
    if sign == k:
        print("Authentication success")
    else:
        print("Authentiacation failed")



# Тестування функцій
range_min = (2 ** 255) + 1
range_max = (2 ** 256) - 1

p, q, p1, q1 = get_keys(range_min, range_max)

A_public, A_private = generate_keys(p, q)
B_public, B_private = generate_keys(p1, q1)

print(f"For A: \n p = {p} \n q = {q} \n n = {A_public[0]} \n e = {A_public[1]} \n d = {A_private[0]} \n")
print(f"For B: \n p1 = {p} \n q1 = {q} \n n1 = {B_public[0]} \n e1 = {B_public[1]} \n d1 = {B_private[0]} \n")


msg = random.randint(0, A_public[0] - 1)
print(f"Msg: {msg}")

encrypted = encrypt_rsa(msg, B_public)
print(f"Encrypted msg: {encrypted}")

decrypted = decrypt_rsa(encrypted, B_private)
print(f"Decrypted msg: {decrypted}")


k = random.randint(0, A_public[0])
print(f"k = {k}")

send = send_message(A_public, A_private, B_public, k)
print(send)

recieve_message(A_public, B_private, B_public, send)

A_sign = create_sign_rsa(msg, A_private)
print(f"Sign: {A_sign}")

verify_sign_rsa(A_sign, msg, A_public)


# перевірка функцій за допомогою сайту

# n = int("92B9DBFF312ADB3B632556A769324CC6CA7A5920D2FEA6A9BE32BB8F01CBD9C7", 16)
# e = int("10001", 16)

# serv_pub_key = (n, e)

# my_msg = int("1525", 16)
# my_ciphertext = encrypt_rsa(my_msg, serv_pub_key)
# print(f"Ciphertext: {hex(my_ciphertext)}")

# my_sign = int("8C8AD159E021DBE3A081A894740466DCE47281820440CB56DADAC6CFA1509CDC", 16)
# print(f"Sign is: {my_sign}")

# verify_sign_rsa(my_sign, my_msg, serv_pub_key)

