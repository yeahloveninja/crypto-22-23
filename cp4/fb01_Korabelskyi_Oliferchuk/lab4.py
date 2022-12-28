import random
from math import gcd

max = pow(2, 255) + 1
min = pow(2, 256) - 1
def TextToInt(txt):
    return int(txt.encode('utf-8').hex(), 16)

def IntToText(txt):
    return bytes.fromhex(hex(txt)[2:]).decode('ASCII')

def miller_rabin_test(n):
    prime_numbers = [2, 3, 5, 7, 11]
    s = 0
    d = n - 1
    if n == 2:
        return True

    if 0 in list(map(lambda x: n % x, prime_numbers)):
        return False

    while d % 2 == 0:
        s += 1
        d //= 2

    for i in range(100):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:

            return False
    return True

def rand_num():
    number = random.randrange(min, max)
    while not miller_rabin_test(number):
        number = random.randrange(min, max)
    return number

def RSA(p, q):
    n = p * q
    e = random.randrange(2, (p - 1) * (q - 1))
    while gcd(e, (p - 1) * (q - 1)) != 1:
        e = random.randrange(2, (p - 1) * (q - 1))
    d = pow(e, -1, (p - 1) * (q - 1))
    prKey = (d, p, q)
    opKey = (n, e)
    return prKey, opKey

def Enc(message, n, e):
    p = pow(message, e, n)
    return p

def Dec(encrMsg, d, n):
    p = pow(encrMsg, d, n)
    return p

def DigSign(message, d, n):
    p = pow(message, d, n)
    return p

def SignVerification(message, sign, opKey):
    n, e = opKey
    if pow(sign, e, n) != message:
        return False
    else:
        return True


def SendMessage(message, opKey, prKey):
    n, e = opKey
    d, p, q = prKey
    EncMessage = Enc(message, n, e)
    sign = DigSign(message, d, p, q)
    return EncMessage, sign


def RecieveMessage(EncMsg, sign, opKey, prKey):
    n, e = opKey
    d, p, q = prKey
    SMS = Dec(EncMsg, d, p, q)
    if SignVerification(SMS, sign, opKey):
        return SMS
    else:
        return 1

print("Input message:")
text = input()
print('Message: ', text)
message = TextToInt(text)
p = rand_num()
q = rand_num()
p1 = rand_num()
q1 = rand_num()
while p * q > p1 * q1:
    p = rand_num()
    q = rand_num()
RSA1, RSA2 = RSA(p, q), RSA(p1, q1)
EncSMS, sign = SendMessage(message, RSA2[1], RSA1[0])
print('EncMessage: ',EncSMS, '\nSignature: ',sign, '\nMessage was sent...\n')
message = RecieveMessage(EncSMS, sign, RSA1[1], RSA2[0])
print(message)
txt = IntToText(message)
print('Message we get: ',txt)




def check():
    print("\nCheck function\n")
    text = 112
    n = int("BFF0CEC9F2700B0C3F92B2E1BCD94307", 16)
    e = int("10001", 16)
    key_pair = [n, e]
    enc = Enc(text, n, e)
    dsign = int("8C29822E50FBF97DDB83ADFB95CF3084", 16)
    verifstat = SignVerification(text, dsign, key_pair)
    print('Message: ', text)
    print('modulus = ', n)
    print('exponent = ', e)
    print('EncMessage: ', enc)
    print('Signature: ', dsign)
    print('Sign Verification Status: ', verifstat)


check()
