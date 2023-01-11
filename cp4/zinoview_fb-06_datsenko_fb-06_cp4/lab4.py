from random import randint, getrandbits


def func(a: int, b: int):
    # function from lab 3 for finding roots of linear expression
    odds = [0, 1]
    if gcd(a, b) > 1: return 0
    val1, val2, m = b, a, []
    while val2:
        m.append(-(val1 // val2))
        val1, val2 = val2, val1 % val2
    for i in range(len(m) - 1): odds.append(m[i] * odds[-1] + odds[-2])
    return odds[-1] + b if odds[-1] < 0 else odds[-1]


def gcd(a: int, b: int):
    # Обчислення НСД двох чисел через алгоритм Евкліда
    b2, y = b, [-1]
    while y[-1] != 0:
        y.append(a - a // b * b)
        a, b = b, y[-1]
    return b2 if (y[-1] == 0 and len(y) == 2) else y[-2]


def pow(index: int, d: int, n: int):
    # Схема Горнера швидкого піднесення до степеня
    d_bin, result = list(bin(int(d))[2:]), 1
    for i in range(len(d_bin)):
        result = ((result * (index ** int(d_bin[i]))) ** 2) % n if i != len(d_bin) - 1 else (result * (
                index ** int(d_bin[i]))) % n
    return result


def test_prime(p: int):
    # тест Міллера-Рабіна на простоту
    for i in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        if p % i == 0: return False
    k, s, d = 8, 0, p - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    iteration = 0
    while iteration < k:
        x = randint(2, p - 1)
        if gcd(x, p) != 1: return False
        ps = pow(x, d, p)
        if ps == 1 or ps == -1:
            iteration += 1
            continue
        for r in range(1, s):
            x = pow(x, 2, p)
            if x == -1:
                return False
            elif x == 1:
                return True
        iteration += 1
        return False
    return True


def rand_prime(size: int):
    while True:
        value = getrandbits(size)
        if test_prime(value):
            return value


def create_pair():
    while True:
        p1, q1, p2, q2 = rand_prime(256), rand_prime(256), rand_prime(256), rand_prime(256)
        if p1 * q1 <= p2 * q2:
            return [[p1, q1], [p2, q2]]


def rsa_pair(p: int, q: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = 65537
        if gcd(e, phi) == 1:
            d = func(e, phi)
            return [[d, p, q], [e, n]]


def encrypt(m: int, e: int, n: int):
    # E(m) = c  |  m - plaintext; e, n - public key
    return pow(m, e, n)


def decrypt(c: int, d: int, n: int):
    # D(c) = m  |  c - ciphertext; d, n - secret key
    return pow(c, d, n)


def get_ds(m: int, d: int, n: int):
    # Confidentiality: creating digital signature and send it with text as a result
    # Returns message and signature  |  m - plaintext; d - secret key; n - public key;
    return [m, pow(m, d, n)]


def ds_is_verified(ms: list, e: int, n: int):
    # Authentication: returns True and False depending on a result of authentication process
    # Compare m and m', m' = (s^e)mod(n) |  m - text to send; d - secret key; n - public key;
    message, signature = ms[0], ms[1]
    return True if pow(signature, e, n) == message else False


def start():
    # ................  B ===(data)===> A  ................

    M = getrandbits(256)  # generating PT

    pairs = create_pair()  # creating pairs to get p,q for each A and B
    pq1, pq2 = pairs[0], pairs[1]


    # B sends request to A to transfer a message, so A generates keys: secret for itself and public for B
    # A sends public key to B
    # Also, B generates for itself secret key and public key for A for digital signature
    # B sends public key to A

    keys_a = rsa_pair(pq1[0], pq1[1])  # [d, p, q], [e, n]
    keys_b = rsa_pair(pq2[0], pq2[1])  # [d, p, q], [e, n]

    d1, p1, q1, e1, n1 = keys_a[0][0], keys_a[0][1], keys_a[0][2], keys_a[1][0], keys_a[1][1]
    d2, p2, q2, e2, n2 = keys_b[0][0], keys_b[0][1], keys_b[0][2], keys_b[1][0], keys_b[1][1]

    # B:
    C = encrypt(M, e1, n1)  # шифрування тексту юзером B, відкритим ключем A
    MS = get_ds(C, d2, n2)  # підписане повідомлення для B  |  MS2 = (message, signature)

    # A:
    D = decrypt(MS[0], d1, n1) if ds_is_verified(MS, e2, n2) else False

    if D:
        if D == M: print(f'B→A: OK!')
    else:
        print(f'B→A: Failed!')

    print(f'\np1 = {p1}\nq1 = {q1}\np2 = {p2}\nq2 = {q2}\n\nd1 = {d1}\nd2 = {d2}\ne = {e1}\nn1 = {n1}\nn2 = {n2}')
    print(f'\nM = {M}\nC = {C}\nS = {MS[1]}\nM\' = {D}')


if __name__ == '__main__':
    start()
