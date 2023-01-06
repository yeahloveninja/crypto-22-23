from random import randint


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def checkprime(num):
    numbers = [2, 3, 5, 7, 11, 13, 17, 19]
    for prime in numbers:
        if num % prime == 0:
            return 0
        else:
            return 1


def mod_pow(a, d, mod):
    x = 1
    while d != 0:
        if d % 2 == 1:
            x = (x * a) % mod
            d = d // 2
            a = (a * a) % mod
        else:
            d = d // 2
            a = (a * a) % mod
    return x


def s_d(number):
    s = 0
    p = number - 1
    d = p
    while d % 2 == 0:
        s = s + 1
        d = d // 2
    return s, d


def miller_test(p):
    prime = 0
    sd = s_d(p)
    if checkprime(p) == 1:
        for k in range(100):
            x = randint(1, p)
            g = gcd(x, p)
            if g == 1:
                if (mod_pow(x, sd[1], p)) in [1, -1]:
                    prime = 1
                    return prime
                else:
                    for r in range(1, sd[0] - 1):
                        xr = mod_pow(x, sd[1] * (2 ** r), p)
                        if xr == -1:
                            prime = 1
                            return prime
                        elif xr == 1:
                            prime = 0
                            return prime
                        else:
                            continue
                    if prime == 1:
                        return prime
            else:
                prime = 0
                return prime
    return prime


def random_num(min_max):
    k = 0
    while k == 0:
        rand_num = randint(min_max[0], min_max[1])
        step1_prime = checkprime(rand_num)
        if step1_prime:
            step2_prime = miller_test(rand_num)
            if step2_prime:
                return rand_num


def make_pairs(min_v=(2 ** 255) + 1, max_v=(2 ** 256) - 1):
    while True:
        numbers = [random_num([min_v, max_v]), random_num([min_v, max_v]), random_num([min_v, max_v]),
                   random_num([min_v, max_v])]
        if (numbers[0] * numbers[1]) <= (numbers[2] * numbers[3]) and len(set(numbers)) == 4:
            return (numbers[0], numbers[1]), (numbers[2], numbers[3])


def modular_inverse(a, mod):
    x = euclid(a, mod)
    if x < 0:
        return x % mod
    return x


def euclid(a, n):
    scheme = [0, 1]
    while a != 0 and n != 0:
        if n > a:
            scheme.append(n // a)
            n = n % a
        elif n < a:
            scheme.append(a // n)
            a = a % n
    for i in range(2, len(scheme) - 1):
        scheme[i] = scheme[i - 2] + (-scheme[i]) * scheme[i - 1]
    return scheme[-2]


def generate_keys(p, q):
    n = p * q
    fi = (p - 1) * (q - 1)
    count = 1
    while count == 1:
        e = randint(2, fi - 1)
        if gcd(e, fi) == 1:
            d = modular_inverse(e, fi)
            return e, n, d
        else:
            count = 1


def Encrypt(b, mes):
    e = b[0]
    n = b[1]
    c = mod_pow(mes, e, n)
    return c


def Decrypt(b, mes):
    d = b[2]
    n = b[1]
    m = mod_pow(mes, d, n)
    return m


def Sign(a, mes):
    d = a[2]
    n = a[1]
    s = mod_pow(mes, d, n)
    return s


def Verify(a, mes, s):
    e = a[0]
    n = a[1]
    m = mod_pow(s, e, n)
    if m == mes:
        return 1
    else:
        return 0


def SendKey(a, b, k):
    k1 = mod_pow(k, b[0], b[1])
    n = a[1]
    s = mod_pow(k, a[2], n)
    s1 = mod_pow(s, b[0], b[1])
    return k1, s1


def ReceiveKey(a, b, sendkey):
    k = mod_pow(sendkey[0], b[2], b[1])
    s = mod_pow(sendkey[1], b[2], b[1])
    auth = mod_pow(s, a[0], a[1])
    if auth == k:
        return print("Аутентифікація вдала!")
    else:
        return print("Помилка аутентифікації!")


def create_signature(a, mes):
    encrypt_m = Encrypt(a, mes)
    sign_m = Sign(a, encrypt_m)
    return encrypt_m, sign_m


def check_signature(a, encrypt_m, sign_m):
    ver = Verify(a, encrypt_m, sign_m)
    if ver == 1:
        print("Перевірка підпису вдала")
    else:
        print("Повідомлення спотворене!")


pairs_for_subscribers = make_pairs()
# print(pairs_for_subscribers)
abonent_A = generate_keys(pairs_for_subscribers[0][0], pairs_for_subscribers[0][1])
abonent_B = generate_keys(pairs_for_subscribers[1][0], pairs_for_subscribers[1][1])
print(f'Ключі для абонента А у HEX форматі:')
k_abonent_A = ['e', 'n', 'd']
for i in range(len(k_abonent_A)):
    print(f'{k_abonent_A[i]} : {hex(abonent_A[i])}')
print(f'Ключі для абонента B у HEX форматі:')
k_abonent_B = ['e1', 'n1', 'd1']
for i in range(len(k_abonent_B)):
    print(f'{k_abonent_B[i]} : {hex(abonent_B[i])}')
message = randint(0, abonent_A[1] - 1)
print(hex(message))
encrypt = Encrypt(abonent_B, message)
print(hex(encrypt))
decrypt = Decrypt(abonent_B, encrypt)
print(hex(decrypt))
signature = create_signature(abonent_A, message)
check_signature(abonent_A, signature[0], signature[1])
k = randint(0, abonent_A[1])
send = SendKey(abonent_A, abonent_B, k)
ReceiveKey(abonent_A, abonent_B, send)
