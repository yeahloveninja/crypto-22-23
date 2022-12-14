from random import randint
from math import log2

MIN = 2 ** 256
MAX = 2 * MIN - 2


def euclid_gcd(a, b):
    if b == 0:
        return abs(a)
    else:
        return euclid_gcd(b, a % b)


def find_params_s_d(n):  # нахождения параметорв уравнения n-1=2^s*d
    d = n - 1  # параметр d в начале когда s равно 0 => 2^s(0) = 1
    s = 0  # параметр s в начале равен 0
    while d % 2 == 0:  # если d делиться на 2 то делим на 2 и добавляем к степени +1
        s = s + 1
        d = d // 2
    return s, d  # возвращаем значения


def fast_exp(b, a, m):
    r = 1
    if 1 & a:
        r = b
    while a:
        a >>= 1
        b = (b * b) % m
        if a & 1:
            r = (r * b) % m
    return r


def prep_div(num):
    prime_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for prime_num in prime_nums:
        if num % prime_num == 0:
            return 0
        else:
            return 1


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def mul_inv(b, n):  # знаходження оберненого елемента
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def miller_rabin_test(p):  # тест на простоту
    pr = 0
    params = find_params_s_d(p)  # знаходимо s та d
    s = params[0]
    d = params[1]
    rounds = round(log2(p))
    if prep_div(p) == 1:  # якщо p пройшло попередню перевірку починаємо тест
        for k in range(rounds):  # вибираємо k з діапазону log2(p)
            x = randint(1, p)  # вибираємо рандомне число з діапазону (1,p)
            g = euclid_gcd(x, p)
            if g == 1:  # (2.1) якщо найбільший спільний дільник == 1 то переходимо до наступних кроків
                if (fast_exp(x, d, p)) in [1, -1]:  # якщо (x^d)mod p == 1 або -1 то переходимо до настоупного кроку
                    pr = 1
                    return pr
                else:
                    for r in range(1, s - 1):  # (2.2) вибираємо r з діапазону 1,s-1
                        x_r = fast_exp(x, d * (2 ** r),
                                       p)  # якщо (x^(d*2^r))mod p == -1 то число сильно просте, якщо 1 то непросте
                        if x_r == -1:
                            pr = 1
                            return pr
                        elif x_r == 1:
                            pr = 0
                            return pr
                        else:
                            continue
            else:
                pr = 0
                return pr
    return pr


def random_prime(min, max):
    k = 0
    while k == 0:
        rand_numer = randint(min, max)
        check_prime = miller_rabin_test(rand_numer)
        if check_prime == 1:
            return rand_numer


def create_pair(min, max):
    while True:
        pairs = [random_prime(min, max), random_prime(min, max), random_prime(min, max), random_prime(min, max)]
        if pairs[0] * pairs[1] <= pairs[2] * pairs[3]:  # перевірка для подальшої роботи системи, n<=n1 якщо навпаки то абонент повинен переробити свою пару p,q
            return pairs


def generate_key_pair(p, q):
    oiler_n = (p - 1) * (q - 1)
    while True:
        n = p * q
        e = randint(2, oiler_n - 1)
        if euclid_gcd(e, oiler_n) == 1:
            d = mul_inv(e, oiler_n)
            return [(e, n), (d, p, q)]
        else:
            continue


# pairs_found = create_pair(MIN, MAX)

# p1 = pairs_found[0]
# q1 = pairs_found[1]
# p2 = pairs_found[2]
# q2 = pairs_found[3]

# print("p1 " + str(p1))
# print("q1 " + str(q1))
# print("p2 " + str(p2))
# print("q2 " + str(q2))

# keys_A = generate_key_pair(p1, q1)
# keys_B = generate_key_pair(p2, q2)

# e_A = keys_A[0][0]
# n_A = keys_A[0][1]
# d_A = keys_A[1][0]

# print("e для абонента А : ", str(e_A))
# print("n для абонента А : ", str(n_A))
# print("d для абонента А : ", str(d_A))

# e_B = keys_B[0][0]
# n_B = keys_B[0][1]
# d_B = keys_B[1][0]

# print("e для абонента В : ", str(e_B))
# print("n для абонента В : ", str(n_B))
# print("d для абонента В : ", str(d_B))

# message = randint(0, n_A - 1)
# print("Message : " + str(message))


def encrypt(message, e, n):
    encrypt_message = fast_exp(message, e, n)
    return encrypt_message


def decrypt(encrypt_message, d, n):
    message = fast_exp(encrypt_message, d, n)
    return message


def sign(message, d, n):
    signed_message = fast_exp(message, d, n)
    return signed_message


def verify(message, signed_message, e, n):
    message_to_check = fast_exp(signed_message, e, n)
    if message == message_to_check:
        return 1
    else:
        return 0


def send_key(n, d, e1, n1, k):
    k1 = fast_exp(k, e1, n1)
    s = fast_exp(k, d, n)
    s1 = fast_exp(s, e1, n1)
    return k1, s1


def receive_key(e, n, k1, s1, d1, n1):
    k = fast_exp(k1, d1, n1)
    s = fast_exp(s1, d1, n1)
    auth = fast_exp(s, e, n)
    if auth == k:
        return "Auth"
    else:
        return "Not Auth"


def create_sign(message, d, n):
    signed_message = sign(message, d, n)
    return signed_message


def check_sign(message, sign_message, e, n):
    verification = verify(message, sign_message, e, n)
    if verification == 1:
        return ["Verification ok", message]
    else:
        return ["Verification failed", message]


# A_encrypt = encrypt(message, e_A, n_A)
# A_decrypt = decrypt(A_encrypt, d_A, n_A)

# print("Зашивроване повідомлення : " + str(A_encrypt))
# print("Розшифроване повідомлення : " + str(A_decrypt))

# k = randint(0, n_A)

# print("Ключ k : " + str(k))

# send = send_key(n_A, d_A, e_B, n_B, k)

# k1 = send[0]
# s1 = send[1]

# receive = receive_key(e_A, n_A, k1, s1, d_B, n_B)

# print(receive)
# print("Ключ k1 : " + str(k1))
# print("Ключ s1 : " + str(s1))

# signature = create_sign(message, d_A, n_A)
# check_signature = check_sign(message, signature, e_A, n_A)

# print(check_signature)

# modudlus D9669737576D37A8B7CA4C1DF394514D51200E350C8E027D408EF3B79C4CBA9B
# public exp 10001
# message 22( 16 hex)
# cyphertext 85322BCFE1025904FEF434D6BFB28FE34A45DE2B1837E9C49175882F7DF45820
# signature 35EADA246FE0A0C28D1EB49E92AE11A982E8890E2543ACB3F4B516C0253958F7

# mod D9669737576D37A8B7CA4C1DF394514D51200E350C8E027D408EF3B79C4CBA9B
ACLE_n = 98333150198878732362049457536571285314575200836982636537534492909076445182619
# public exp (e) 10001
ACLE_e = 65537
# message 22
ACLE_message = 34

# encrypt 60246253594311452391106401177082839448753614472186264481298290795565785831456
ACLE_encrypt = encrypt(ACLE_message, ACLE_e, ACLE_n)

# signature 35EADA246FE0A0C28D1EB49E92AE11A982E8890E2543ACB3F4B516C0253958F7
ACLE_sign = 24387528751115011838962269802416685358045221117918323190434208470255678347511

ACLE_verify = check_sign(ACLE_message, ACLE_sign, ACLE_e, ACLE_n)
print(ACLE_verify)