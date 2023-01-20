from random import randint


def nsd(a, b): # нсд
    while a*b != 0:
        if a >= b:
            a = a % b
        else:
            b = b % a
    return a + b


def bezout(a, n):
    answer = [0, 1]
    while a != 0 and n != 0:
        if n > a:
            answer.append(n // a)
            n = n % a
        elif n < a:
            answer.append(a // n)
            a = a % n
    for i in range(2, len(answer) - 1):
        answer[i] = answer[i - 2] + (-answer[i]) * answer[i - 1]
    x = answer[-2]
    if x < 0:
        return x % n
    return x


def pipipupucheck(num): #проверка числа на простоту
    numeric = [2, 3, 5, 7, 11, 13, 17, 19]
    for numeric_simple in numeric:
        if num % numeric_simple == 0:
            return False
        else:
            return True


def fastpow (c, d, mod): # алгоритм возведения в степень
    y = 1
    while d != 0:
        if d % 2 == 1:
            y = (y * c) % mod
            d = d // 2
            c = (c * c) % mod
        else:
            d = d // 2
            c = (c * c) % mod
    return y


def preparingfortest(numeric): #Подготовка к тесту Миллера
    s = 0
    moda = numeric - 1
    d = moda
    while d % 2 == 0:
        s = s + 1
        d = d // 2
    return s, d


def maintest_Miller(simple):
    numeric_simple = 0
    sd = preparingfortest(simple)
    if pipipupucheck(simple) == 1:
        for i in range(100):
            x = randint(1, simple)
            n = nsd(x, simple)
            if n == 1:
                if (fastpow(x, sd[1], simple)) in [1, -1]:
                    numeric_simple = 1
                    return numeric_simple
                else:
                    for r in range(1, sd[0] - 1):
                        xR = fastpow(x, sd[1] * (2 ** r), simple)
                        if xR == -1:
                            numeric_simple = 1
                            return numeric_simple
                        elif xR == 1:
                            numeric_simple = 0
                            return numeric_simple
                        else:
                            continue
                    if numeric_simple == 1:
                        return numeric_simple
            else:
                numeric_simple = 0
                return numeric_simple
    return numeric_simple


def coincidence_num(min_max):
    k = 0
    while k == 0:
        rand_num = randint(min_max[0], min_max[1])
        step1_prime = pipipupucheck(rand_num)
        if step1_prime:
            step2_prime = maintest_Miller(rand_num)
            if step2_prime:
                return rand_num


def livetogether(min_v=(2 ** 255) + 1, max_v=(2 ** 256) - 1):
    while True:
        numeric = [coincidence_num([min_v, max_v]), coincidence_num([min_v, max_v]), coincidence_num([min_v, max_v]),
                   coincidence_num([min_v, max_v])]
        if (numeric[0] * numeric[1]) <= (numeric[2] * numeric[3]) and len(set(numeric)) == 4:
            return (numeric[0], numeric[1]), (numeric[2], numeric[3])


def Encrypt(b, mes):
    e = b[0]
    n = b[1]
    C = fastpow(mes, e, n)
    return C


def Decrypt(b, mes):
    d = b[2]
    n = b[1]
    M = fastpow(mes, d, n)
    return M


def Sign(a, mes):
    d = a[2]
    n = a[1]
    S = fastpow(mes, d, n)
    return S


def Verify(a, mes, s):
    e = a[0]
    n = a[1]
    M = fastpow(s, e, n)
    if M == mes:
        return True
    else:
        return False


def CreatingKeys(a, b):
    n = a * b
    phi = (a - 1) * (b - 1)
    meter = 1
    while meter == 1:
        e = randint(2, phi - 1)
        if nsd(e, phi) == 1:
            d = bezout(e, phi)
            return e, n, d
        else:
            meter = 1


def SendKey(a, b, k):
    #print(a)
    #print(b)
    k1 = Encrypt(b, k)
    #n = a[1]
    S = Sign(a, k)
    S1 = Encrypt(b, S)
    return k1, S1


def got_key(a, b, sendkey):
    k = Decrypt(b, sendkey[0])
    s = Decrypt(b, sendkey[1])
    login = Verify(a, k, s)
    if login == 1:
        return print("Пипипупу1")
    else:
        return print("Не вышло")


def create_signature(a, mes):
    encrypt_m = Encrypt(a, mes)
    sign_M = Sign(a, encrypt_m)
    return encrypt_m, sign_M


def check_signature(a, encrypt_M, sign_M):
    ver = Verify(a, encrypt_M, sign_M)
    if ver == True:
        print("Пипипупу2")
    else:
        print("Не вышло")


def final():
    partners = livetogether()
    print(partners)
    partner1 = CreatingKeys(partners[0][0], partners[0][1])
    #print(partner1)
    partner2 = CreatingKeys(partners[1][0], partners[1][1])
    print(f'пара ключей 1:')
    key_partner1 = ['e', 'n', 'd']
    for i in range(len(key_partner1)):
        print(f'{key_partner1[i]} : {partner1[i]}')
    print(f'пара ключей 2:')
    key_partner2 = ['e1', 'n1', 'd1']
    for i in range(len(key_partner2)):
        print(f'{key_partner2[i]} : {partner2[i]}')
    report = randint(0, partner1[1] - 1)
    print(report)
    encrypt = Encrypt(partner2, report)
    print(encrypt)
    decrypt = Decrypt(partner2, encrypt)
    print(decrypt)
    caption = create_signature(partner1, report)
    check_signature(partner1, caption[0], caption[1])
    k = randint(0, partner1[1])
    b = 15
    test_send = [23, 15, 18]
    send = SendKey(partner1, partner2, k)
    got_key(partner1, partner2, send)

final()
# exp = '10001'
mod = 'BDAFB62ED0B290497205D4768C4BE3F9ED6F0FE125A77B268F2871F7DB813E47'
#mod = '42'
n = int(mod, base=16)
#85797583998544640711737405761966135740046954643331660431393077356296392490567 mod 16
#print(n)
e = int('10001', 16)
b = e, n
message = 66 #42 в 16
print(Encrypt(b,66))  # 56923092262062670029369080183419769797982230129887409317214508866303825977460 answer
sign = int('2DE786C271DB6F9E96CD9DECB722BD3C7BB9DC3B0712BB3E44D1C14A1E7E6AF5', 16)
print(Verify(b, message, sign))
# cyphertext = '7DD95417588D2D3272D294856681467C317FFF19BE570EAEF11563FBF86EA074'
# decrypted = '42'
# signature = '2DE786C271DB6F9E96CD9DECB722BD3C7BB9DC3B0712BB3E44D1C14A1E7E6AF5'
