import random
import math


# Generate prime dig and check if it's prime (task 1)
def genDig(lenBits):
    while True:
        rrange_from = 2 ** (lenBits - 1)
        rrange_to = 2 ** lenBits
        a = (random.randrange(rrange_from, rrange_to))
        if millerTest(a):
            return a

# Calculate reversed num of e
def euclid(totient, e):
    if e == 0:
        return totient, 0, 1
    else:
        div, y, x = euclid(e, totient % e)
    return div, x - (totient // e) * y, y

# Generate p,q for A and p1,q1 for B (task 2)
def GenerateKeyPair():
    while True:
        keys = []
        for div in range(4):
            key = genDig(256)
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys


def generate_rsa_keypair(p, q):
    n = p * q
    # Euler's function
    totient = (p-1) * (q-1)
    e = random.randrange(2, totient-1)
    # check if gcd of e and totient is 1
    while math.gcd(e, totient) != 1:
        e = random.randrange(2, totient-1)
    # find d that will -> d*e = 1
    d = (euclid(totient, e))[1] % totient
    return d,n,e

# check if number is prime (task 1)
def millerTest(n, k=10):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        r //= 2
        s += 1
    for div in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

gen_keys = GenerateKeyPair()
p, q, p1, q1 = gen_keys[0], gen_keys[1], gen_keys[2], gen_keys[3]

# find values for A
d,n,e = generate_rsa_keypair(p, q)
print("--------->Keys for A <----------")
print(f"Secret keys:\nd: {d}\np: {p}\nq: {q}")
print(f"Public keys:\nn: {n}\n")
print("\n<-------------------------------------------------------------------->\n")

# find values for B
d1,n1,e1 = generate_rsa_keypair(p1, q1)
print("--------->Keys for B <----------")
print(f"Secret keys:\nd1: {d1}\np1: {p1}\nq1: {q1}")
print(f"Public keys:\nn1: {n1}\ne1: {e1}")
print("\n<-------------------------------------------------------------------->")

def Decrypt(c, d, n):
    return pow(c, d, n)

def Encrypt(m, e, n):
    return pow(m, e, n)

def Sign(m, d, n):
    return pow(m, d, n)

def SendKey(k, d, e1, n1, n):
    k_1 = Encrypt(k, e1, n1)
    s = Sign(k, d, n)
    s_1 = Encrypt(s, e1, n1)
    return k_1, s_1

def ReceiveKey(key1, s1, d1, n1, e, n):
    try:
        key = Decrypt(key1, d1, n1)
        s = Decrypt(s1, d1, n1)
        if SignCheck(key, s, e, n):
            return True, key
        else:
            return False, 0
    except Exception as e:
        return False, str(e)


def SignCheck(m, s, e, n):
    return m == pow(s, e, n)


start_key = random.randint(0, n)
encrypted_key, dig_sign = SendKey(start_key, d, e1, n1, n)
received_key = ReceiveKey(encrypted_key, dig_sign, d1, n1, e, n)

message = random.randint(0, n)
encrypted_msg = Encrypt(message, e, n)
decrypted_msg = Decrypt(encrypted_msg, d, n)
print(f'Our key: {start_key}')
print(f'Message: {message}\n')

if received_key[0]:
    print(f'Key: {received_key[1]}\n')
if not received_key[0]:
    print('Error getting the key')
print(f"Encrypted message: {encrypted_msg}\nDecrypted: message: {decrypted_msg}")
