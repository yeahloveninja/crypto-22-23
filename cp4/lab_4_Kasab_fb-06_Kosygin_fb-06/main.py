from random import randint
from math import log2

MIN = 2 ** 256
MAX = 2 * MIN - 2
e = 2 ** 16 + 1

def FindNSD(a, b): # нахождение НСД
    if b == 0:
        return abs(a)
    else:
        return FindNSD(b, a % b)

def ExpEuclidAlgorithm(a, b): # расширенный алгоритм Эквлида
    if a == 0:
        return b, 0, 1
    gcd, _, __ = ExpEuclidAlgorithm(b % a, a)
    x = __ - (b // a) * _
    y = _
    return gcd, x, y

def FindInvertedModElement(b, n): # нахождение обратного по модулю элемента
    g, x, _ = ExpEuclidAlgorithm(b, n)
    if g == 1:
        return x % n

def FastPower(b, a, m): # вставить вот эту функцию вместо предыдущей
    a = bin(a)[2:]
    r = 1
    for i in range(len(a) - 1, -1, -1):
        r = (r * b ** int(a[i])) % m
        b = (b ** 2) % m
    return r

def SimpleTest(p): # тест на простоту
    d = p - 1
    s = 0
    for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 51, 53]:
        if p % prime == 0:
            return False
        else:
            while d % 2 == 0: # если d делиться на 2 то делим на 2 и добавляем к степени +1
                s = s + 1
                d = d // 2
            for _ in range(round(log2(p))): # вибираємо _ з діапазону log2(p)
                x = randint(1, p) # вибираємо рандомне число з діапазону (1,p)
                if FindNSD(x, p) == 1: # (2.1) якщо найбільший спільний дільник == 1 то переходимо до наступних кроків
                    if (FastPower(x, d, p)) in [1, -1]:  # якщо (x^d)mod p == 1 або -1 то переходимо до настоупного кроку
                        return True
                    else:
                        for r in range(1, s - 1): # (2.2) вибираємо r з діапазону 1,s-1
                            if FastPower(x, d * (2 ** r), p) == -1:
                                return True
                            elif FastPower(x, d * (2 ** r), p) == 1:
                                return False
                            else:
                                continue
                else:
                    return False
    return False

def FindPairs(min, max):
    pairs = []
    while len(pairs) < 4:
        rand_numer = randint(min, max)
        if SimpleTest(rand_numer):
            pairs.append(rand_numer)
    if pairs[0] * pairs[1] <= pairs[2] * pairs[3]:
        return pairs
    else:
        return FindPairs(min, max)

def FindKeyPair(p, q):
    oiler_n = (p - 1) * (q - 1)
    n = p * q
    while True:
        if FindNSD(e, oiler_n) == 1:
            d = FindInvertedModElement(e, oiler_n)
            return [(e, n), (d)]
        else:
            continue

def Verify(message, signed_message, e, n):
    message_to_check = FastPower(signed_message, e, n)
    if message == message_to_check:
        return True
    else:
        return False

def SendKey(n, d, e1, n1, k):
    s = FastPower(k, d, n)
    return FastPower(k, e1, n1), FastPower(s, e1, n1)

def CheckSign(message, sign_message, e, n):
    verification = Verify(message, sign_message, e, n)
    if verification:
        return "Verify"
    else:
        return "Not verify"

def ReceiveKey(e, n, k1, s1, d1, n1):
    k = FastPower(k1, d1, n1)
    s = FastPower(s1, d1, n1)
    if CheckSign(k, s, e, n) == "Verify":
        return "Auth"
    else:
        return "Not auth"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def encrypt(message, e, n):
    return FastPower(message, e, n)

def decrypt(encrypt_message, d, n):
    return FastPower(encrypt_message, d, n)

def Sign(message, d, n):
    return FastPower(message, d, n)

def CreateSign(message, d, n):
    return Sign(message, d, n)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FoundedPairs = FindPairs(MIN, MAX)
PForA = FoundedPairs[0]
QForA = FoundedPairs[1]
PForB = FoundedPairs[2]
QForB = FoundedPairs[3]
keys_A = FindKeyPair(PForA, QForA)
keys_B = FindKeyPair(PForB, QForB)
message = randint(MIN, MAX)
e_A = keys_A[0][0]
n_A = keys_A[0][1]
d_A = keys_A[1]
e_B = keys_B[0][0]
n_B = keys_B[0][1]
d_B = keys_B[1]

A_encrypt = encrypt(message, e_A, n_A)
k = randint(0, n_A)
send = SendKey(n_A, d_A, e_B, n_B, k)
k1 = send[0]
s1 = send[1]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("p: " + str(FoundedPairs[0]))
print("q: " + str(FoundedPairs[1]))
print("p1: " + str(FoundedPairs[2]))
print("q1: " + str(FoundedPairs[3]))

print("\ne_A: " + str(keys_A[0][0]))
print("n_A: " + str(keys_A[0][1]))
print("d_A: " + str(keys_A[1]))
print("e_B: " + str(keys_B[0][0]))
print("n_B: " + str(keys_B[0][1]))
print("d_B: " + str(keys_B[1]))

print("\nkeys_A: " + str(keys_A))
print("keys_B: " + str(keys_B))

print("\nmessage: " + str(message))
print("Зашивроване повідомлення: " + str(A_encrypt))
print("Розшифроване повідомлення: " + str(decrypt(A_encrypt, d_A, n_A)))

print("\nКлюч k: " + str(k))
print("Ключ k1: " + str(k1))
print("Ключ s1: " + str(s1))

print("\n" + CheckSign(message, CreateSign(message, d_A, n_A), e_A, n_A))
print(ReceiveKey(e_A, n_A, k1, s1, d_B, n_B))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 16: 
# MOD = 975A520F21D133D2A05F167565FA4667D7047188DEC62B9924136D387F356B9F
# MSG = 123321
# e = 10001
# 10: 
Serverkey_net = 68458822723064282581670949529857628029767980649954088402552635093188307413919
MSG_net = 1192737
print(encrypt(MSG_net, e, Serverkey_net))

# Signature_16 = 43C1CF598E82191DA0A2C84D951577E41A0C0AE9A880B12B5EF2F3A2D0DD9887
Signature_10 = 30647393414517979894207132422897301279128145217284139372244085575598701648007
print(CheckSign(MSG_net, Signature_10, e, Serverkey_net))