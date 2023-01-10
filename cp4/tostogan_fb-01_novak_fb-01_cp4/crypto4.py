import random as rd
import math as m
import time
from progress.bar import Bar


prosti = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

def test_milrab(p):

	for pr in prosti:
		if p%pr == 0:
			return False
			break
		
	if p % 2 == 0:
        	return False
 
        	
	c=0
	d=p-1
	while d % 2 == 0:
        	d //= 2
        	c += 1
	st = c
	
	for k in range(0, 17):
		x = rd.randint(2, p-1)
		g = m.gcd(x,p)
		if g>1:
			return False		
		else:
			t = pow(x, d, p)
			if t in [1,-1]:
				return True
			else:
				for r in range(1, st-1):
					x_r = pow(x,d*pow(2,r),p)
					if x_r == 1:
						return False
					elif x_r == -1:
						return True
					else:
						continue
						
							
def proste(bit):#Генеруємо просте число	
    while True:
        p = (rd.randrange(2 ** (bit - 1), 2 ** bit))
        if test_milrab(p):
            return p


kluchi = []
def GenerateKeyPair():
	for i in range(0,4):
		kluch = proste(256)
		kluchi.append(kluch)
	if kluchi[0]*kluchi[1] > kluchi[2]*kluchi[3]:
		kluchi.clear()
		GenerateKeyPair()
	return True


def evkl(a, b): #розширений алгоритм евкліда
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = evkl(b, a % b)
        return d, y, x - y * (a // b)
        
def obern(a, b): #обернене 
    if (m.gcd(a, b)!= 1):
        return None
    else:
    	d, x, y = evkl(b, a % b)
    	return y
    	
def GenerateKeyPairRSA(p, q):
    n = p * q
    phiN = (p - 1) * (q - 1)
    e = rd.randrange(2, phiN - 1)
    while m.gcd(e, phiN) != 1:
        e = rd.randrange(2, phiN - 1)
    d = obern(e, phiN) % phiN
    return [e, n, d]   	



def Encrypt(M, e, n): #Шифрування
    C = pow(M, e, n)
    return C

def Decrypt(C, d, n): #Розшифрування
    M = pow(C, d, n)
    return M

def Sign(M, d, n): # Цифровий підпис
    S = pow(M, d, n)
    return S

def Verify(M, S, e, n):#Перевірка
    return M == pow(S, e, n)


def SendKey(k, d, e_1, n_1, n): #Надсилання ключа
    K_1 = Encrypt(k, e_1, n_1)
    S = Sign(k, d, n)
    S_1 = Encrypt(S, e_1, n_1)
    return K_1, S_1


def ReceiveKey(K_1, S_1, d_1, n_1, e, n): #Oтримання ключа
    K = Decrypt(K_1, d_1, n_1)
    S = Decrypt(S_1, d_1, n_1)

    if Verify(K, S, e, n):
        print('Bob отримав ключ\n')
        print('Розшифрований k =', k, '\n')
        return K
    else:
        print('Bob не отримав ключ')


GenerateKeyPair()
rs_A=GenerateKeyPairRSA(kluchi[0], kluchi[1])
rs_B=GenerateKeyPairRSA(kluchi[2], kluchi[3])
print('---------------------Згенеровані ключі---------------------')
print('---------абонент Alica')
print('Відкритий ключ:')
print('e =', rs_A[0], '\nn =', rs_A[1])
print('Секретний ключ:')
print('p =', kluchi[0], '\nq =', kluchi[1],'\nd =', rs_A[2])
print('\n---------абонент Bob')
print('Відкритий ключ:')
print('e =', rs_B[0], '\nn =', rs_B[1])
print('Секретний ключ:')
print('p =', kluchi[2], '\nq =', kluchi[3],'\nd =', rs_B[2])


print('\n----------------------Робота з повідомленням----------------------')
M = rd.randint(0, rs_A[1])
k = rd.randint(0, rs_A[1])
print('Початковий k:', k, '\n')

print('Згенероване повідомлення: ', M, '\n') #Абонент Аlice формує повідомлення
K1, S1 = SendKey(k, rs_A[2], rs_B[0], rs_B[1], rs_A[1]) #Аlice робить підпис, шифрує його в S1 та надсилає
E = Encrypt(M, rs_A[0], rs_A[1])
print('\nAlice шифрує повідомлення і надсилає Bob')
with Bar('Encoding...') as bar:
    for i in range(100):
        time.sleep(0.02)
        bar.next()
print("\nЗашифроване повідомлення: ", E, '\n')
#Абонент Вob за допомогою свого секретного ключа d1 знаходить (K, S)
K = ReceiveKey(K1, S1, rs_B[2], rs_B[1], rs_A[0], rs_A[1])

if K!=None:
	print('Вob розшифровує повідомлення')
	D = Decrypt(E, rs_A[2], rs_A[1])    
	with Bar('Decoding...') as bar:
    		for i in range(100):
        		time.sleep(0.02)
        		bar.next()
	print("\nРозшифроване повідомлення:", D)
	print('\nПеревірка тексту: ')
	with Bar('Processing...') as bar:
    		for i in range(100):
        		time.sleep(0.02)
        		bar.next()
	if M == D:
		print('\nOбмін повідомленням між Alice і Bob успішний')
else:
	print('\nOбмін повідомленням неуспішний')








