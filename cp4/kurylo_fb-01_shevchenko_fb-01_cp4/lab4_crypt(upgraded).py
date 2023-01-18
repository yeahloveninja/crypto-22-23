import random
import math

def miller_rabin_test(n, q = 50):
    if n == 2 or n ==3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for i in range(q):
        a = random.randrange(2, n - 2)
        b = pow(a, d, n)

        if b == 2 or b == n - 1:
            continue
        for i in range(s - 1):
            b = pow(b, 2, n)
            if b == 1:
                return False
            if b == n - 1:
                break
        else:
            return False
    return True

def search_rand_prime(l):
    a = l - 1
    b = random.randrange(pow(2, a), pow(2, l))
    while not miller_rabin_test(b):
        b = random.randrange(pow(2, a), pow(2, l))
    return b

def generate_base_keys():
    p = search_rand_prime(256) # генерація для абонента A
    q = search_rand_prime(256)

    p1 = search_rand_prime(256) # генерація для абонента B
    q1 = search_rand_prime(256)
    n = p * q
    n1 = p1 * q1
    if n <= n1:
        return True
    else:
        generate_base_keys()
    return p, q, p1, q1, n, n1


def inverse(a, m):
    i = [0,1]
    
    while m != 0 and a != 0:
        if a > m: 
            i.append(a // m); a = a % m
        else: i.append(m // a); m = m % a

    for n in range(2,len(i)): 
        i[n] = i[n-2] - i[n] * i[n-1]
    return i[-2]

def generate_key_pair():
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while math.gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    phi1 = (p1 - 1) * (q1 - 1)
    e1 = random.randrange(2, phi1)
    while math.gcd(e1, phi1) != 1:
        e1 = random.randrange(2, phi1)
    d = inverse(e, phi) % phi
    d1 = inverse(e1, phi1) % phi1
    return e, e1, d, d1

def encrypt(M, e, n):
    C = pow(M, e, n)
    return C

def decrypt(C, d, n):
    M = pow(C, d, n)
    return M

def sign(M, d, n):
    global S
    S = pow(M, d, n)
    print("\nА підписав повідомлення S =", S)

def verify(S, e, n):
    M = pow(S, e, n)
    print("\nB перевіряє підпис M =", M)
    return M

def send_key(k, e1, n1, d, n):
    print("\nФормування повідомлення (k1, S1), відправка k =", k)
    S = pow(k, d, n)
    k1 = pow(k, e1, n1)
    S1 = pow(S, e1, n1)
    print("\nS =", S, "\n\nk1 =", k1, "\n\nS1 =", S1)
    print("\nПовідомлення сформоване, відправка до B")
    return S1, k1


def receive_key(k1, d1, n1, S1, e):
    print("\nОтримання повідомлення (k1, S1)")
    k = pow(k1, d1, n1)
    S = pow(S1, d1, n1)
    print("\nПеревірка k, S (Конфеденційність) k =", k, "\nS =", S)
    k = pow(S, e, n)
    print("\nПеревірка підпису А (Автентифікація) k =", k)
    return k

p, q, p1, q1, n, n1 = generate_base_keys()
e, e1, d, d1 = generate_key_pair()
print("p =", p, "\nq =", q, "\n\np1 =", p1, "\nq1 =", q1, "\n\nn =", n, "\nn1 =", n1, "\n\ne =", e, "\ne1 =", e1, "\n\nd =", d, "\nd1 =", d1) 

M = random.randrange(0, n - 1 )
k = random.randrange(0, n)
print("\nM =", M)
print("\nk =", k)
C = encrypt(M, e, n)
print("\nEncrypt M =", C)
print("\nDecrypt M =", decrypt(C, d, n))

sign(M, d, n)
verify(S, e, n)
S1, k1 = send_key(k, e1, n1, d, n)
receive_key(k1, d1, n1, S1, e)


# Перевірка скрипта з http://asymcryptwebservice.appspot.com/?section=rsa.
# M = int('15D6FF34BC649', 16)
# e = int('10001', 16)
# n = int('E10DE054035E3D2FF20B29BCD9D9F0F9D9CD1E2CA593B948BCC05AE32A2CC849', 16)
# A = encrypt(M, e, n)
# print(hex(A)[2:])

# C = int('D3405BC06F57271A3DC14F8ABCF7B08B6550A3EAB1906FD17BACAA5BB7C15746', 16)
