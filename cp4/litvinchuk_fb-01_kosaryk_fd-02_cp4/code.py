import random
from math import gcd

def ToBinary(n):
    """Число у двійкову систему"""
    bin_num = []
    for i in bin(int(n))[2:] :
        bin_num.append(int(i))
    return bin_num

def Solve(x,d,p):
    """Повертає обчислення виразу виду: (x^d)modp"""
    r = 1
    for i in ToBinary(d):
        r = ((r ** 2) * (x ** int(i))) % p
    return r

def MillerRabin(p):
    if p==2 or p==3:
        return True
    if p<2 or p%2 ==0:
        return False
    """Розклад p-1=d*2^s"""
    t = p-1
    s = 0
    while t%2 == 0:
        t = t//2
        s += 1
    d = t
    """Кількість раундів для тесту - 100"""
    for k in range(0,100):
        x = random.randint(2, p-1)
        if gcd(x,p) > 1: #число складене
            return False
        elif gcd(x,p) == 1:
            r = Solve(x, d, p)
            if r ==1 or r == -1: #p є сильно псевдопростим за основою x
                return True
            else:
                for j in range(1,s):
                    x_r = Solve(x, 2, p)
                    if x_r == -1:
                        return True
                    elif x_r == 1: #p є сильно псевдопростим за основою x
                        return False
                    else:
                        continue

def TryDivision(p):
    """Тест пробних ділень"""
    l = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]
    for j in l:
        if p%j == 0 and p//j!=1:
            return False
    return True

def GenNum(l):
    """Генерація простого числа довжини l біт"""
    ff = open('1.txt', 'a')
    m1 = 2**(l-1)+1
    m2 = 2**l-1
    while True:
       x = random.randint(m1,m2)
       for k in range(0,(m2-x+(1-x%2))//2):
           if x % 2 == 0:
              x+=1
           if TryDivision(x):
               if MillerRabin(x):
                   return x
           else:
               s = str(x)+'\n'
               ff.write(s)
           x+=2

def ExtendedEuclid(a, b):
    """ Повертає d=НСД(x,y) і x, y такі, що ax + by = d """
    if b == 0 :
        return a, 1, 0
    d, x, y = ExtendedEuclid(b, a % b)
    return d, y, x - (a // b) * y

def Inverse(a,b):
    """Обернене за модулем"""
    c = list(ExtendedEuclid(a,b))[1]
    return c

def GenerateKeyPair(p, q):
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(2,phi-1)
    while gcd(e,phi)!=1:
        e = random.randint(2,phi-1)
    d = Inverse(e,phi)
    if d < 0:
        d = d + phi
    open_key = [e,n]
    private_key = [d,n]
    return open_key,private_key

def Encrypt(M, open_key):
    return Solve(M,open_key[0],open_key[1])
def Decrypt(C, secret_key):
    return Solve(C, secret_key[0], secret_key[1])
def Sign(M,secret_key):
    return [M, Solve(M, secret_key[0], secret_key[1])]
def Verify(M, S,open_key):
    return M == Solve(S,open_key[0], open_key[1])

def SendKey(M, a_secret, b_open):
    k1 = Encrypt(M,b_open)
    s = Sign(M, a_secret)
    s1 = Encrypt(s[1],b_open)
    return [k1,s1]

def ReceiveKey(M, b_secret, a_open):
    m = Decrypt(M[0], b_secret)
    s = Decrypt(M[1], b_secret)
    if Verify(m,s,a_open):
        return m
    else:
        return False

def FromHex(a):
    return int(a, 16)

numbers = []
for i in range(0, 4):
    f = GenNum(256)
    if f not in numbers:
       numbers.append(f)
numbers = sorted(numbers)

A = GenerateKeyPair(numbers[0],numbers[1])
B = GenerateKeyPair(numbers[2],numbers[3])
p = numbers[0]
q = numbers[1]
p1 = numbers[2]
q1 = numbers[3]
print('---Згенеровані числа абонента А---')
print("p - \n", p)
print("q - \n", q)
print('\n---Згенеровані числа абонента В---')
print("p1 - \n", p1)
print("q1 - \n", q1)
A_secret_key = A[1]
A_open_key = A[0]
B_secret_key = B[1]
B_open_key = B[0]
print('\n---Ключі абонента А---\n')
print('Секретний -', A_secret_key,' \n','Відкритий -', A_open_key,' \n', )
print('\n---Ключі абонента B---\n')
print('Секретний -', B_secret_key,' \n','Відкритий -', B_open_key,' \n', )

message = GenNum(255)
print('\n---Відкрите повідомлення ---\n', message)
encrypt_message = Encrypt(message, A_open_key)
print('---Зашифроване повідомлення відкритим ключем А---\n', encrypt_message)
print('\n--Розшифроване повідомлення секретним ключем А---\n', Decrypt(encrypt_message, A_secret_key))
encrypt_message = Encrypt(message,B_open_key)
print('\n---Зашифроване повідомлення відкритим ключем B---\n', encrypt_message)
print('\n---Розшифроване повідомлення секретним ключем B---\n', Decrypt(encrypt_message, B_secret_key))
signature = Sign(message, A_secret_key)

print('\n---Перевірка цифрового підпису : ',Verify(message, signature[1], A_open_key))

key = GenNum(255)
print('\n\n---Ключ ---\n', key)
send_m = SendKey(key, A_secret_key, B_open_key)
print('\n---Повідомлення зашифроване відкритим ключем B ---\n', send_m[0])
print('\n---Підпис повідомлення секретним ключем А ---\n', send_m[1])
rec_m = ReceiveKey(send_m, B_secret_key, A_open_key)
print('\n---Отриманий ключ від А, розшифрований секретним ключем В ---\n', rec_m)
print('\n\n\n ---Перевірка---')
n = FromHex("0xA808A1372A745403E590C5D212ABDE6F4A6C3FB512882CD02C5C1D2C514F12B3")
e = FromHex("0x10001")
print('\n---Ключ сервера---\n', [e,n])
k = GenNum(255)
print('\n---Згенероване повідомлення---\n', k)
send_k= SendKey(k, A_secret_key, [e,n])
print('\n---Зашифроване повідомлення відкритим ключем сервера---\n', send_k[0])
#print('\n---Зашифроване повідомлення відкритим ключем сервера y 16-ій сиситемі ---\n', hex(send_k[0]))
print("\n---Цифровий підпис ---\n", send_k[1])
#print("\n---Цифровий підпис у 16-ій системі ---\n", hex(send_k[1]))
#print("\n---Відкритий ключ абонента А у 16-ій системі ---\n", [hex(A_open_key[0]), hex(A_open_key[1])])

 


