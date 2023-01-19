import re

crypt = open('crypt.txt', 'r', encoding='utf-8').read()

def InputLetter(crypt_t, letter):
    l = len(letter)
    counter = l * [0]
    for j in range(0, l):
        cou = crypt_t.count(letter[j])
        counter[j] = cou
        cou *= cou-1
    element = sum(counter)
    element *= (l*(l-1))**-1
    return element

def Divide(crypt_t, end):
    lst = []
    for i in range(0, end):
        stance = crypt_t[i::end]
        lst.append(stance)
    return lst

def DivideIndex(lst, letter):
    l_letter = len(letter)
    l_lst = len(lst)
    counter = l_letter * [0]
    for j in range(0, l_lst):
        counter[j] = InputLetter(lst[j], letter)
    element = sum(counter)
    element = (l_lst)**-element
    return element

def Key(lst, letter1, letter2):
    l_lst = len(lst)
    l_letter = len(letter1)
    k = []
    for i in range(0, l_lst):
        f = []
        for j in range(0, l_letter):
            f.append(lst[i].count(letter1[j]))
        y = f.index(max(f))
        x = letter1.find(letter2)
        k.append(letter1[(y - x) % l_letter])
    key = ''
    for i in k:
        key += i
    return key

def Decrypt(crypt_t, k, letter):
    key = []
    for i in k:
        key.append(letter.find(i))
    l_crypt = len(crypt_t)
    encrypt = []
    l_key = len(key)
    l_letter = len(letter)
    for j in range(0, l_crypt):
        encrypt.append(letter[(letter.find(crypt[j]) - key[j % l_key]) % l_letter])
    encr = ''
    for k in encrypt:
        encr += k
    print(encr)
    return encr

alphabet_str = ''
for i in range(ord('а'), ord('я')+1):
    alphabet_str += (chr(i))
l_alph = len(alphabet_str)

key = Key(Divide(crypt, 15), alphabet_str, 'о')
key = 'арудазовархимаг'
encrypted = Decrypt(crypt, key, alphabet_str)

