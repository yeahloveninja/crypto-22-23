import os
from math import gcd
from collections import OrderedDict
from Change_symbols import change_symbols

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
n = len(alphabet)

def Ext_Gcd(a, b): # НСД
    if a == 0:
        x = 0
        y = 1
        return (abs(b), x, y)
    else:
        gcd, y, x = Ext_Gcd(b % a, a)
        x = x - (b // a) * y
        return (gcd, x, y)


def Inverse_Mod(a, m): # пошук оберненого
    gcd, x, y = Ext_Gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        return 0


def ModuloEquation(a, b, mod):
    if gcd(a, mod) == 1: # якщо НСД = 1, то 1 корінь
        x = (Inverse_Mod(a, mod) * b) % mod
    elif b % gcd(a, mod) != 0: # немає коренів
        x = 0
    else: # коренів буде рівно d
        d = gcd(a, mod)
        x = ModuloEquation(int(a/d), int(b/d), int(mod/d)) 
    return x

def KeyAnsw(x, y):
    X = alphabet.index(x[0]) * n + alphabet.index(x[1])
    Y = alphabet.index(y[0]) * n + alphabet.index(y[1])
    print("X, Y ", X, Y)
    a = ModuloEquation(X, Y, n**2)
    b = (Y - X*n)%n**2
    return (a, b)

def KeyGen(x1, x2, y1, y2):
    X1 = alphabet.index(x1[0]) * n + alphabet.index(x1[1])
    X2 = alphabet.index(x2[0]) * n + alphabet.index(x2[1])
    Y1 = alphabet.index(y1[0]) * n + alphabet.index(y1[1])
    Y2 = alphabet.index(y2[0]) * n + alphabet.index(y2[1])
    a = ModuloEquation(X1-X2, Y1-Y2, n**2)
    b = (Y1 - a*X1)%n**2
    return (a, b)

def Mono_(text):
    LA = {}
    for let in alphabet:
        LA[let] = 0

    for let in text:
        LA[let] = LA[let] + 1

    LF = {}
    for let in alphabet:
        LF[let] = round(LA[let] / len(text), 5)

    return LF

def Bigrams_(text):
    BA = {}
    for let in alphabet:
        for bi in alphabet:
            key = let + bi
            BA[key] = 0

    i = 0
    while i < len(text) - 1:
        key = text[i] + text[i + 1]
        BA[key] = BA[key] + 1
        i = i + 2

    BF = {}
    for key in BA.keys():
        BF[key] = round((BA[key]) / ((len(text) / 2)), 5)

    return OrderedDict(sorted(BF.items(), key=lambda x: x[1], reverse=True))


def Decrypt_(text, key):
    op_text = ""
    i = 0
    while i < len(text):
        Y = alphabet.index(text[i]) * n + alphabet.index(text[i + 1])
        X = ModuloEquation(key[0], Y-key[1], n**2)

        x1 = X//n
        x2 = X%n

        op_text = op_text + alphabet[x1] + alphabet[x2]
        i += 2

    return op_text

def Test(text):
    Res = True

    popularLetters = ["о", "е", "а", "и", "т"]
    i = 0
    for l in OrderedDict(sorted(Mono_(text).items(), key=lambda x: x[1], reverse=True)):
        if i < 2:
            if l not in popularLetters:
                Res = False
        else:
            break
        i += 1
    if Res != False:
        
        unpopularLetters = ["ф", "э", "щ", "ц", "ш"]
        i = 0
        for l in OrderedDict(sorted(Mono_(text).items(), key=lambda x: x[1])):
            if i < 2:
                if l not in unpopularLetters:
                    Res = False
            else:
                break
            i += 1
        if Res != False:
            popularBi = ["ст", "но", "ен", "то", "на", "ов", "ни", "ра", "во", "ко"]
            i = 0
            print("work with bigrams in open text")
            for l in Bigrams_(text):
                if i < 4:
                    if l[0]+l[1] not in popularBi:
                        Res = False
                else:
                    break
                i += 1
            if Res != False:
                return True
            else:
                return False
        else:
            return False
    else:
        return False




def Analise(text):
    popularBi = ["ст", "но", "ен", "то", "на", "ов", "ни", "ра", "во", "ко"]

    bi = []
    i = 0
    for el in Bigrams_(text):
        if i < 5:
            bi.append(el[0]+el[1])
            i += 1
        else:
            break

    print(bi)
    keys = []
    for bigr in popularBi:
        for b in popularBi:
            for bigc in bi:
                for bc in bi:
                    if bigr != b and bigc != bc:
                        keys.append(KeyGen(bigr, b, bigc, bc))

    for key in keys:
        if key[0] == 0:
            keys.remove(key)

    print(len(keys))

    result = ""
    i = 0
    for key in keys:
        open = Decrypt_(text, key)
        Correct = Test(open)
        print(i)
        i += 1
        if Correct == True:
            print(key)
            result = open
            break
            
        else:
            result = ""
            

    return result


if __name__ == "__main__":
    path = os.getcwd()+r'\05.txt'
    path = change_symbols(path, space=False)
    res = os.getcwd()+r'\result.txt'

    with open(path, 'r') as f:
        text = f.read()
        f.seek(0)


    result = Analise(text)

    with open(res, 'w') as r:
        r.write(result)