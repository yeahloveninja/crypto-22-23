from numpy import log2
from random import randint


def fast_exp(inpy, inpx, inpz):
    q = inpy if 1 & inpx else 1
    while inpx:
        inpy = (pow(inpy,2)) % inpz
        inpx = inpx>>1
        if inpx & 1:
            q = (q * inpy) % inpz
    return q

def mul_inv(inpy, n):
    g, x, _ = egcd(inpy, n)
    if g == 1:
        return x % n


def m_r_funct(p): 
    params = sd_search(p) 
    s,d = params[0], params[1]
    if prep_div(p) == 1:  
        for _ in range(round(log2(p))):
            x = randint(1, p) 
            g = gcd_eu(x, p)
            if g != 1:
                return 0
            if (fast_exp(x, d, p)) == 1: 
                return 1
            elif (fast_exp(x, d, p)) == -1: 
                return 1
            else:
                for r in range(1, s - 1):  
                    qp = pow(2,r)
                    x_r = fast_exp(x, d * qp, p)
                    if x_r == -1:
                        return 1
                    elif x_r == 1:
                        return 0
                    else:
                        continue
    return 0


def prime_rnd(min, max):
    while True:
        rand_numer = randint(min, max)
        compare = m_r_funct(rand_numer)
        if compare == 1:
            return rand_numer

def egcd(inpx, inpy):
    if inpx == 0:
        return inpy, 0, 1
    return egcd(inpy % inpx, inpx), egcd(inpy % inpx, inpx) - (inpy // inpx) * egcd(inpy % inpx, inpx), egcd(inpy % inpx, inpx)

def sd_search(n):  
    d = n - 1  
    s = 0 
    while d % 2 == 0:
        s += 1
        d //= 2
    return s, d 


def gcd_eu(inpx, inpy):
    return inpx if inpy == 0 else gcd_eu(inpx , int(inpx % inpy))

def encrypt(message, e, n):
    return fast_exp(message, e, n)


def decrypt(encrypt_message, d, n):
    return fast_exp(encrypt_message, d, n)


def sign(message, d, n):
    return fast_exp(message, d, n)


def verify(message, signed_message, e, n):
    message_to_check = fast_exp(signed_message, e, n)
    return 1 if message == message_to_check else 0


def prep_div(num):
    for prime_num in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        return 0 if num % prime_num == 0 else 1

def generate_key_pair(p, q):
    n_oil = (p - 1) * (q - 1)
    while True:
        e = randint(2, n_oil - 1)
        n = p * q
        if gcd_eu(e, n_oil) == 0:
            continue
        else:
            return [(e, n), (mul_inv(e, n_oil), p, q)]


def receive_key(e, n, k1, s1, d1, n1):
    k, s = fast_exp(k1, d1, n1), fast_exp(s1, d1, n1)
    auth = fast_exp(s, e, n)
    if auth == k:
        return "Авторизований користувач"
    else:
        return "Не авторизований користувач"


def create_sign(message, d, n):
    return sign(message, d, n)


def check_sign(message, sign_message, e, n):
    verification = verify(message, sign_message, e, n)
    if verification == 1:
        return "Верифікація пройшла успішно"
    else:
        return "Верификація не пройшла"

def create_pair(min, max):
    p_list = []
    while True:
        p_list.extend(prime_rnd(min, max) for _ in range(3))
        if p_list[2] * p_list[3] >=p_list[0] * p_list[1]: 
            return p_list

def send_key(n, d, e1, n1, k):
    s_send, k_send = fast_exp(fast_exp(k, d, n), e1, n1), fast_exp(k, e1, n1)
    return k_send, s_send


MIN = 2 ** 255
MAX = 2 * MIN

n_server = 30917082915262018153573483920186964487956177587076973408317738523290518716003
e_server = 65537
message_server = 17
encrypt_server = encrypt(message_server, e_server, n_server)
print(encrypt_server)

sign_server = 25852320005391753845252256083997989028406097176929540733642651573387602909257

verify_server = check_sign(message_server, sign_server, e_server, n_server)
print(verify_server)