#PART1
import random
def gcdExtended(a, b):
    if a == 0:
        x = 0
        y = 1
        return (abs(b), 0, 1)
    gcd, y, x = gcdExtended(b % a, a) #recursion
    x = x - (b // a) * y
    return (gcd, x, y)
    
def modInverse(a, m):
    gcd, x, y = gcdExtended(a, m)
    if gcd != 1:
        answer = 0 #Inverse doesn't exist
    else:
        answer = ((x % m + m) % m)
    return answer

def MillerRabinTest(p):   #Miller-Rabin Test that helps to check whether number is prime ot not    
    s = 0
    d = p - 1
    while d % 2 == 0:
        s += 1
        d = d // 2
    for trials in range(100):  
        x = random.randrange(1, p+1)
        if gcdExtended(x, p)[0] == 1:  
            if pow(x, d, p) == 1 or pow(x, d, p) == -1 :  
                return True
            else:
                for r in range(1, s - 1):   
                    xr = pow(x, d * (2 ** r), p)
                    if xr == -1:
                        return True  
                    elif xr == 1:
                        return False
                    else:
                        continue
        else:
            return False
    return False

def PrimeTest(num): #additional test
    knownPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    if num in knownPrimes: #if num in list
        return True
    for prime in knownPrimes: # if it is divided by some number from list
        if (num % prime == 0):
            return False
    return MillerRabinTest(num) #go to Miller-Rabin Test


def get_prime():
    while True:
        minr = (2 ** 255) + 1
        maxr = (2 ** 256) - 1
        randnum = random.randrange(minr,maxr+1)
        if PrimeTest(randnum): #check if it is ok than return
            return randnum 

#PART2
def get_primepair():
    while True: #p,q,p1,q1
        p = get_prime()
        q = get_prime()
        p1 = get_prime()
        q1 = get_prime()
        pairs = [] #array that will contain pairs
        if (p * q) < (p1 * q1):
            pairs.append(p) #adding each num
            pairs.append(q)
            pairs.append(p1)
            pairs.append(q1)
            return pairs
        
        

p,q,p1,q1=get_primepair()
#print(p,"---",q,"---",p1,"---",q1)

#PART3
def get_keypair(p, q): #generate keys due to the rule
    n = p*q
    EulerFunc = (p-1)*(q-1)
    while True:
        e = random.randrange(2, EulerFunc)
        if gcdExtended(e, EulerFunc)[0] == 1:
            d = modInverse(e, EulerFunc)
            return [d, p, q], [n, e] 

a_private, a_public = get_keypair(p, q)
b_private, b_public = get_keypair(p1, q1)
print("---Alice:\n")
print("p: ",p,"\n")
print("q: ",q,"\n")
print("Alice's public key: ",a_public,"\n")
print("Alice's private key: ",a_private[0],"\n")
print("---Bob:\n")
print("p: ",p1,"\n")
print("q: ",q1,"\n")
print("Bob's public key: ",b_public,"\n")
print("Bob's private key: ",b_private[0],"\n")

#PREPARE MESSAGE
import binascii
def convert(message):
    return int(message.encode('utf-8').hex(), base=16)

def convert_totext(message):
    hexmss=hex(message)[2:]
    return binascii.unhexlify(hexmss).decode('utf-8')


text = "Catch me, if u can"
message = convert(text)

#PART4
def encrypt(message, public_key):
    return pow(message, public_key[1], public_key[0])
def decrypt(ct, private_key):
    n=private_key[1]*private_key[2]
    return pow(ct, private_key[0],n)
def sign(message,private_key):
    n=private_key[1]*private_key[2]
    return pow(message, private_key[0],n)
def verify(message, sign, public_key):
    testmessage = pow(sign, public_key[1], public_key[0])
    if  testmessage == message:
        print("(!)verification succeeded")
        return True
    else:
        print("(!)verification failed")
        return False

#PART5
def send(k, dest_public_key, src_private_key):
    print("--Ready to send message")
    k1 = encrypt(k, dest_public_key) #message
    s = sign(k, src_private_key) # create sign
    s1 = encrypt(s, dest_public_key) #encrypt it
    print("--Sending this ->")
    return [k1, s1]

def recieve(k1s1, dest_private_key, src_public_key):
    print("--Message was recieved")
    k = decrypt(k1s1[0], dest_private_key)
    s = decrypt(k1s1[1], dest_private_key)
    if verify(k, s, src_public_key):
        mess = convert_totext(k)
        print("--Message from receiver ->")
        return mess
    else:
        print("(!)аuthentication failed")
        return None

send=send(message,b_public,a_private)
print(send)
recieve = recieve(send,b_private,a_public)
print(recieve)

#--------------------------TESTS-----------------------

def to_hex(number):
    hex_n = hex(number)
    return hex_n[2:]
def from_hex(hex_n):
    numb = int(hex_n, base=16)
    return numb

#TEST1 - ENCRYPTION FUNCTION (ENCRYPT LOCAL, DECRYPT ON SERVER)
server_key_n = '8EFC6EED4D95A432ECB4EAECFEDCB5EB0B5BEBA4EA060B9C8264708D6AB73179'
server_key_n = from_hex(server_key_n)
#print(server_key_n)
server_key_e = '10001'
server_key_e = from_hex(server_key_e)

serv_key_pub = [server_key_n, server_key_e]

test_message = "Glory to Ukraine"
test_message = convert(test_message)

encrypted = to_hex(encrypt(test_message, serv_key_pub))
print('Text is encrypted!')
print("Here is your ciphertext -->  ",encrypted)

#TEST2 - DECRYPTION FUNCTION (DECRYPT LOCAL, ENCRYPT ON SERVER+ENCRYPT LOCAL)
print("Alice's public key: ",a_public,"\n")
my_key_n = to_hex(a_public[0])
#print(my_key_n)
my_key_e = to_hex(a_public[1])
#print(my_key_e)

tmessage = "Catch me if you can"
server_ciphertext = '3A4CE3D550E6A9CEE818DB740A8D05734ADB95E9E08E2BC3C7A824A05A8574BAE1D746C53A48CDB31179950CB555773C007B782CC5090045281FC11D65FF7FE9'

encrypted = to_hex(encrypt(convert(tmessage), a_public))
print(encrypted,"\n")

print("Alice's private key: ",a_private,"\n")
nserver_ciphertext = from_hex(server_ciphertext)
convert_totext(decrypt(nserver_ciphertext, a_private))

#TEST3 - VERIFY FUNCTION (SIGN ON SERVER, VERIFY LOCAL)
server_sign = '64D9B32067F8840071AEF3504F00F3868DABF3D9C2862126041C350025D8C17B'
server_sign = from_hex(server_sign)
server_key_n = '8EFC6EED4D95A432ECB4EAECFEDCB5EB0B5BEBA4EA060B9C8264708D6AB73179'
server_key_n = from_hex(server_key_n)
#print(server_key_n)
server_key_e = '10001'
server_key_e = from_hex(server_key_e)
serv_key_pub = [server_key_n, server_key_e]
mess = 'Hi'
mess = convert(mess)
verify(mess,server_sign,serv_key_pub)

#TEST4 - SIGN FUNCTION (SIGN LOCAL, VERIFY ON SERVER)
print("Alice's private key: ",a_private,"\n")
mess = 'Hi'
mess = convert(mess)
print(to_hex(sign(mess,a_private)),"\n")
print("Alice's public key: ",a_public,"\n")
my_key_n = to_hex(a_public[0])
print(my_key_n)
my_key_e = to_hex(a_public[1])
print(my_key_e)