from collections import Counter
from itertools import permutations
import os
alph = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
topFiveRusBigrams = ['ст', 'но', 'то', 'на', 'ен']
impossibleRusBigrams = ('аь', 'еь', 'жы', 'уь', 'хы', 'хь', 'цщ', 'цю', 'чф', 'чц', 'чщ', 'шы', 'щъ', 'щы', 'ыь', 'ьы', 'эы', 'эь',
'юы', 'юь', 'яы', 'яь', 'ьь')

with open('10.txt', 'r', encoding='utf-8') as file:
        txt = file.read().lower().replace('\n', '')

def EuclidsAlgorytm(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x, y = EuclidsAlgorytm(b, a % b)
        return gcd, y, x - y * (a // b)


def AlgLineal(a, b, m):
    gcd, a1, y = EuclidsAlgorytm(a, m)
    result = []
    if gcd == 1:
        if ((a * a1) % m) == 1:
            result.append((a1 * b) % m)
            return result
    else:
        if b % gcd != 0:
            return None
        else:
            gcd, q, a1 = EuclidsAlgorytm(a, m)
            for i in range(gcd - 1):
                x = (a1 * b) % m + i * m
                result.append(x)
            return result


def CountOfBigrams(txt):
    bigrams = Counter([txt[i: i + 2] for i in range(0, len(txt), 2)])
    top = bigrams.most_common(5)
    topBigramTxt = [bigrams[0] for bigrams in top]
    return topBigramTxt
BigramTxt = CountOfBigrams(txt)

#print(BigramTxt)

def Swaps(freq, topRusBigrams): # створює пари біграм (х1-х2)(у1-у2)
    perm = permutations(freq)
    result = []
    for p in perm:
        comb = {}
        for i in range(len(topRusBigrams)):
            comb[topRusBigrams[i]] = p[i]
        result.append(comb)
    return result

def countIndex(bigram): # присвоєння числа біграмі
    return  alph.index(bigram[0]) * (len(alph)) + alph.index(bigram[1])

def XY():    # Х - біграми мови, У - біграми ШТ, створення пар
    Xs = []
    Ys = []
    for num in topFiveRusBigrams:
        Xs.append(countIndex(num))
    for num in BigramTxt:
        Ys.append(countIndex(num))
    print(Xs,Ys)
    return Xs, Ys
Xs, Ys = XY()

def SearchOfKey(pair):
    y1 = pair[0][0]
    x1 = pair[0][1]
    y2 = pair[1][0]
    x2 = pair[1][1]
    a = AlgLineal(x1 - x2, y1 - y2, len(alph) ** 2)
    b = []
    if a:
        for elements in range(len(a)):
            b.append((y1 - (x1 * a[elements])) % len(alph) ** 2)
        return (a[0], b[0])


def decryption(a, b, m, txt):
    lenTxt = len(txt)
    decrText = []
    gcd, a1, q = EuclidsAlgorytm(a, m)
    if lenTxt % 2 == 1: lenTxt -= 1
    for bi in [txt[i: i + 2] for i in range(0, lenTxt, 2)]:
        y = countIndex(bi)
        x = (y - b) * a1 % m
        x2 = x % 31
        x1 = ((x - x2) // 31) % 31
        letter1 = alph[x1]#індекс букви дає з алфавіту букву
        letter2 = alph[x2]
        if  letter1 + letter2  not in impossibleRusBigrams:
            if a != 0:
                decrText.append(letter1 + letter2) # додається біграмма у ВТ
        else:
            decrText.clear()
            return OurKeys, decrText

    if len(decrText) > 0:
        decrText = ''.join(decrText)
        OurKeys.append((a, b))
    return OurKeys, decrText


keys = []
OurKeys = []
answers = []

OurPairs = Swaps(Xs, Ys)
all = []
for i in range(len(OurPairs)):
    for x, y in OurPairs[i].items():
        all.append((x, y))

all = list(set(permutations(all, 2)))

for i in range(len(all)):
    answers = (SearchOfKey(all[i]))
    if not answers in keys and answers != None:
        keys.append(answers)
for key in keys:
    OurKeys, decrText = decryption(key[0], key[1], len(alph)**2, txt)
    if len(decrText) > 0:
        file = open('result.txt', 'w', encoding='utf-8')
        file.write(decrText),('\n')
        print(decrText)
        file.close()

print(OurKeys)

