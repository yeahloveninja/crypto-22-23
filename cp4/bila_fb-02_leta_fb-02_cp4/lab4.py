from random import randint


# 1
def my_gcd(a, b):   # пошук НСД
    if b == 0:
        if a < 0:
            return -a
        else:
            return a
    else:
        return my_gcd(b, a % b)


def check_plain(dig):  # перевірка числа на простоту
    plain_digs = [2, 3, 5, 7, 11, 13]
    for plain_dig in plain_digs:
        if dig % plain_dig == 0:  # якщо непросте:
            return 0
        else:
            return 1


def test(p):  # тест Міллера-Рабіна
    is_pseudo = 0
    s = 0
    p1 = p - 1
    d = p1
    while d % 2 == 0:   # крок 0
        s += 1
        d = d // 2
    if check_plain(p) == 1:
        for k in range(150):  # крок 1
            x = randint(1, p)  # генеруємо х
            if my_gcd(x, p) == 1:  # якщо НСД це 1
                if (pow(x, d, p)) in [1, -1]:  # крок 2.1
                    is_pseudo = 1  # число псевдопросте
                    return is_pseudo
                else:
                    for r in range(1, s - 1):  # крок 2.2
                        x_r = pow(x, d * pow(2, r), p)
                        if x_r == -1:
                            is_pseudo = 1  # число псевдопросте
                            return is_pseudo
                        elif x_r == 1:
                            is_pseudo = 0
                            return is_pseudo
                        else:
                            continue   # перейдемо до наступного значення r
                    if is_pseudo == 1:
                        return is_pseudo
            else:
                is_pseudo = 0
                return is_pseudo
    return is_pseudo


def generate_plain(length):   # пошук випадкового простого числа з заданого інтервалу
    start = pow(2, (length - 1))
    end = pow(2, length)
    while True:
        random = randint(start, end)
        if test(random):
            return random


# 2
def key_combination():   # функція для генерації 2 пар простих чисел
    i = 0
    while i < 4:
        pq = generate_plain(256)   # довжина 256 біт
        combination.append(pq)
        i += 1
    if combination[0] * combination[1] < combination[2] * combination[3]:
        return True
    else:
        combination.clear()
        key_combination()


# 3
def my_expanded_gcd(a, m):  # обчислення оберненого за розширеним алгоритмом Евкліда
    ans = [0, 1]
    while a != 0 and m != 0:
        if a > m:
            ans.append(a // m)
            a = a % m
        elif m > a:
            ans.append(m // a)
            m = m % a
        else:
            print('Inverse does not exist')
    for i in range(2, len(ans) - 1):
        ans[i] = ans[i - 2] + (-ans[i]) * ans[i - 1]
    return ans[-2]


def key_combination_rsa(p, q):   # генерація ключових пар для RSA
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = randint(2, phi_n - 1)
    while my_gcd(e, phi_n) != 1:
        e = randint(2, phi_n - 1)
    d = my_expanded_gcd(e, phi_n) % phi_n
    return d, n, e


# 4
def to_encrypt(M, e, n):  # шифрування
    C = pow(M, e, n)
    return C


def to_decrypt(C, d, n):  # розшифрування
    M = pow(C, d, n)
    return M


def to_sign(M, d, n):  # створення цифрового підпису
    S = pow(M, d, n)
    return S


def to_check(M, S, e, n):  # перевірка цифрового підпису
    return M == pow(S, e, n)


def to_send(k, d, e1, n1, n):
    k1 = to_encrypt(k, e1, n1)  # Абонент А формує повідомлення k1 s1 і відправляє його абоненту B
    s = to_sign(k, d, n)
    s1 = to_encrypt(s, e1, n1)
    return k1, s1


def to_receive(k1, s1, d1, n1, e, n):
    k = to_decrypt(k1, d1, n1)     # Абонент B за допомогою свого секретного ключа d1 знаходить k s
    print('decr k', k)
    s = to_decrypt(s1, d1, n1)
    ch = to_check(k, s, e, n)  # за допомогою відкритого ключа e абонент B перевіряє підпис А
    return k


combination = []
key_combination()
p, q, p1, q1 = combination[0], combination[1], combination[2], combination[3]
print('Combination for А:')
print('p: ', p)
print('q: ', q)
print('\nCombination for В:')
print('p1: ', p1)
print('q1: ', q1)

e, n, d = key_combination_rsa(combination[0], combination[1])
"""print('\ne = ', e)
print('n = ', n)
print('d = ', d)"""
e1, n1, d1 = key_combination_rsa(combination[2], combination[3])
"""print('\ne1 = ', e1)
print('n1 = ', n1)
print('d1 = ', d1)"""

print("\nА's keys:")
print('d = ', d)  # секретний ключ
print('p = ', p)
print('q = ', q)
print('n = ', n)   # відкритий ключ
print('e = ', e)
print("\nB's keys:")
print('d1 = ', d1)  # секретний ключ
print('p1 = ', p1)
print('q1 = ', q1)
print('n1 = ', n1)   # відкритий ключ
print('e1 = ', e1)

M = randint(0, n)  # вибираємо відкрите повідомлення M
E = to_encrypt(M, e, n)
D = to_decrypt(E, d, n)

print("\nOur message: ", M)
print("Encrypting: ", E)
print("Decrypting: ", D)
phi = (p - 1) * (q - 1)
print("Phi: ", phi)

if M == D:
    print("\nChecking message: Correct.")
else:
    print("\nChecking message: Incorrect.")

k = randint(0, n)

k1, s1 = to_send(k, d, e1, n1, n)

received_k = to_receive(k1, s1, d1, n1, e, n)
print('Checking key:', k == received_k)

"""Checking...."""

n_hex = '8151DBE01E38BCFAD69AF5A7018AD9725E6E8FEF2556964E02D1173992A98077'
e_hex = '10001'
check_n = int(n_hex, 16)
check_e = int(e_hex, 16)
my_message_hex = 'A91'
my_message = 2705
print(to_encrypt(my_message, check_e, check_n))
# output:
# 54978380305847369047303250572451177412363843279305469386038678280741947866138

signed_message = int('5A6A2C0C427011ED2AD4C1F4B3E73C6B4CF2C4281C23151CAEAEBE282B9C61F2', 16)
print(to_check(my_message, signed_message, check_e, check_n))
