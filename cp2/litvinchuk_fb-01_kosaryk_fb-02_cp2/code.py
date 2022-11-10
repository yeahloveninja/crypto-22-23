import re
import random

f = open("text.txt", encoding='utf-8')
text = f.read()
text = re.sub( r'[^а-яё ]', ' ', text.lower())
text = text.replace(' ', '')

letters = []
for i in range(ord('а'), ord('я')+1):
    letters.append(chr(i))

#створення ключів
keys=[]
lenKeys=[2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
for i in lenKeys:
    key = random.choices(letters, k = i)
    keys.append(''.join(key))

#букви -> цифри
def ToNum(t):
    toNum = []
    for i in t:
        toNum.append(letters.index(i))
    return toNum

#цифри -> букви
def ToLet(t):
    inLet = []
    for i in t:
        inLet.append(letters[i])
    return ''.join(inLet)

#кодування
def Vigenere(text,key):
    text = ToNum(text)
    key = ToNum(key)
    PairsLet = {}
    iter = 0
    NumL = 0

    #словник (номер букви в тексті: номер букви ВТ, номер букви К )
    for i in text:
        PairsLet[NumL] = [i, key[iter]]
        NumL += 1
        iter += 1
        if (iter >= len(key)):
            iter = 0
    #список символів ШТ в цифрах
    l = []
    for v in PairsLet:
        go = (PairsLet[v][0] + PairsLet[v][1])%32
        l.append(go)
    EncText = ToLet(l)  #шт
    return EncText

#обчислення індексу відповідності
def Index(text):
    s=0
    for i in letters:
        s = s + text.count(i)*(text.count(i)-1)
    index = (1/(len(text)*(len(text)-1))) * s
    return index

print('-----ВТ')
print(text)
print('Значення індексу відповідності у ВТ : ', Index(text))
for i in keys:
    print("Шифрування ключем довжиною", len(i), i)
    print('-----ШТ')
    print(Vigenere(text,i))
    print('Значення індексу відповідності у ШТ : ', Index(Vigenere(text,i)))
