import random
import math

# ---------------------- №1----------------------


def miller(p, q=30):
    if p <= 3:
        raise Exception('number should be more than 3. ')

    if p % 2 == 0:
        return False

    # Шукаємо непарне число d таке що  p-1 = d*2^s
    d = p - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(q):
        # Нехай "а" буде з наступного проміжку [2,...,p − 2]
        a = random.randint(2, p-2)

        # b = a^d mod p
        b = pow(a, d, p)

        if b == 1 or b == p-1:
            continue

        for _ in range(s-1):
            b = (b*b) % p
            if b == p-1:
                break
        else:
            return False
    return True


# ---------------------- №2----------------------


# Ф-ція для генерування простого числа
def makePrime(lenBits):
    while True:
        a = (random.randrange(2 ** (lenBits - 1), 2 ** lenBits))
        if miller(a):
            return a


def GenerateKeyPair():
    for i in range(0, 4):
        key = makePrime(256)
        keys.append(key)
    if keys[0] * keys[1] < keys[2] * keys[3]:
        return True
    else:

        keys.clear()
        GenerateKeyPair()


keys = []
GenerateKeyPair()
p = keys[0]
q = keys[1]
p1 = keys[2]
q1 = keys[3]

print('---------------------- №2----------------------')
print('Перша пара для абонента А:')
print('p: ', p, '\nq: ', q)
print('\nДруга пара для абонента В:')
print('p: ', p1, '\nq: ', q1, '\n')

# ---------------------- №3----------------------


# Ф-ція Eвкліда розширенного
def expandedEvklid(first, second):
    if first == 0:
        return second, 0, 1

    gcd, x0, y0 = expandedEvklid(second % first, first)
    x = y0 - (second // first) * x0
    y = x0

    # gcd - НСД(a, b), x - коефіцієнт перед first, y - коефіцієнт перед second
    return [gcd, x, y]


# Ф-ція для знаходження оберненого елементу
def reverseElement(number, module):
    gcd, x, y = expandedEvklid(number, module)

    if gcd == 1:
        return (x % module + module) % module

    else:
        return -1


# Ф-ція для знаходження ключових пар для RSA
def GenerateKeyPairRSA(p, q):
    n = p * q
    elerN = (p - 1) * (q - 1)
    e = random.randrange(2, elerN - 1)
    while math.gcd(e, elerN) != 1:
        e = random.randrange(2, elerN - 1)
    d = reverseElement(e, elerN) % elerN
    return d, n, e


print('---------------------- №3----------------------')
e, n, d = GenerateKeyPairRSA(keys[0], keys[1])
print('e = ', e)
print('n = ', n)
print('d = ', d, '\n')

e1, n1, d1 = GenerateKeyPairRSA(keys[2], keys[3])
print('e1 = ', e1)
print('n1 = ', n1)
print('d1 = ', d1, '\n')


print("---------Ключі для абонента А---------")
print('Відкриті ключі для А:')
print('e = ', e)
print('n = ', n)
print('Секретний ключ для А:')
print('d = ', d)
print('p = ', p)
print('q = ', q, '\n')

print("---------Ключі для абонента B---------")
print('Відкриті ключі для В:')
print('e1 = ', e1)
print('n1 = ', n1)
print('Секретний ключ для В:')
print('d1 = ', d1)
print('p1 = ', p1)
print('q1 = ', q1, '\n')


# ---------------------- №4----------------------


# Шифрування
def Encrypt(M, e, n):
    C = pow(M, e, n)
    return C


# Розшифрування
def Decrypt(C, d, n):
    M = pow(C, d, n)
    return M


# Підпис
def Sign(M, d, n):
    S = pow(M, d, n)
    return S


# Перевірка
def Verify(M, S, e, n):
    return M == pow(S, e, n)


# Надсилання ключа
def SendKey(k, d, e1, n1, M, e, n):
    K1 = pow(k, e1, n1)
    S = Sign(k, d, n)
    S1 = pow(S, e1, n1)
    E = Encrypt(M, e, n)

    return K1, S1, E


# отримання ключа
def ReceiveKey(K1, S1, d1, n1):
    K = pow(K1, d1, n1)
    print('Розшифрований k = ', k, '\n')
    S = pow(S1, d1, n1)

    if K:
        print('Ключ отримано\n')
        return K, S
    else:
        print('Ключ не вдалося отримати')


# аутентифікація
def authentication(S, e, n):
    k = pow(S, e, n)
    return k


M = random.randint(0, n)


print('---------------------- №4----------------------')

k = random.randint(0, n)
print('Початковий k = ', k, '\n')

print("Повідомлення: ", M, '\n')
# Абонент А формує повідомлення (K1, S1) і відправляє його В
# У ф-ції SendKey() А робить підпис, шифрує його в S1 та шифрує повідомлення
# Всі ці дії виконуються в SendKey()
K1, S1, E = SendKey(k, d, e1, n1, M, e, n)

# Абонент В за допомогою свого секретного ключа d1 знаходить конфіденційність (K, S)
# І за допомогою відкритого ключа А перевіряє підпис А(автентифікація)
K, S = ReceiveKey(K1, S1, d1, n1)
print("Шифрування: ", E)
D = Decrypt(E, d, n)
print("Розшифрування:", D)

elerFun = (p - 1) * (q - 1)
print("Ф-ція Ейлера:", elerFun)

print("Перевірка тексту: ", M == D)
k_rec = authentication(Sign(k, d, n), e, n)
print("Перевірка ключа: ", k == k_rec)

