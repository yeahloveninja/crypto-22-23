from collections import Counter
from itertools import combinations
import re
import operator


# Ф-ція розширеного алгоритму Евкліда
def evklidExtended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x0, y0 = evklidExtended(b % a, a)
    x = y0 - (b // a) * x0
    y = x0
    return gcd, x, y  # gcd - НСД(a, b), x - коефіцієнт перед a, y - коефіцієнт перед b


# Ф-ція для знаходження оберненого елементу
def reverseElement(number, mod):
    gcd, x, y = evklidExtended(number, mod)
    if gcd == 1:
        return (x % mod + mod) % mod
    else:
        return -1


# Ф-ція для розв'язання лінійних рівнянь
def linearEquation(a, b, mod):
    gcd, _, _ = evklidExtended(a, mod)
    if gcd == 1:
        x = ((reverseElement(a, mod)) * b) % mod
        return x
    elif b % gcd != 0:
        return -1
    else:
        a = a / gcd
        b = b / gcd
        n1 = mod / gcd
        x0 = linearEquation(a, b, n1)
        return x0


# Ф-ція для отримання частоти
# def Get_freq(text):
#     return dict(Counter(text).most_common())

# Ф-ція для отримання символу з числа
def charToInt(char):
    inter = ord(char) - 1072
    if (char >= 'ъ'):
        inter = inter - 1
    return inter


# Ф-ція для отримання числа з символу
def intToChar(inter):
    if (inter >= 26):
        inter = inter + 1
    char = chr(inter + 1072)
    return char


# Ф-цiя для отримання Біграм
def makeBigrams(someText):
    if len(someText) % 2 != 0:
        someText = someText + 'ф'
    return re.findall('..', someText)


# Ф-ція для підрахунку Біграм
def coupleBigram(someText):  # Підрахунок частоти біграм
    objectBigramAmount = {}  # Об'єкт {біграма: кількість}

    for i in range(0, len(someText), 2):
        if someText[i:i+2] in objectBigramAmount:
            objectBigramAmount[someText[i:i+2]] += 1
        else:
            objectBigramAmount[someText[i:i+2]] = 1

    finallSum = sum(objectBigramAmount.values())

    for couple in objectBigramAmount:
    # Обчислюємо частоту біграм
        objectBigramAmount[couple] = objectBigramAmount[couple]/finallSum

    sortObject = dict(sorted(objectBigramAmount.items(), key=operator.itemgetter(1), reverse=True))
    sortTuple = list(sortObject.items())[:5]
    return list(list(zip(*sortTuple))[0])


# Ф-ція для перевірки мови
def checkLanguage(someText):
    if (someText.count('о') / len(someText)) < 0.1 or (someText.count('а') / len(someText)) < 0.07:
        return -1
    else:
        return 1


# Ф-ція для розшифрування
def decryption(text, a, b):
    bigrams = makeBigrams(text)
    decrypt = ''
    for bigram in bigrams:
        Y = charToInt(bigram[0]) * 31 + charToInt(bigram[1])
        X = (reverseElement(a, 31 * 31) * (Y - b)) % (31 * 31)
        decrypt = decrypt + (intToChar(X // 31) + intToChar(X % 31))
    return decrypt


def attackFun(someText):
    # bigrams = makeBigrams(text)

    popularRus = []
    for bigram in ['ст', 'но', 'то', 'на', 'ен']:
        popularRus.append(charToInt(bigram[0]) * 31 + charToInt(bigram[1]))

    popularRusEncrypt = []
    for bigram in coupleBigram(someText):
        popularRusEncrypt.append(charToInt(bigram[0]) * 31 + charToInt(bigram[1]))

    xCombin = list(combinations(popularRus, 2))  # кортежі len = 2, у відсортованому порядку, без повторюваних елементів
    yCombin = list(combinations(popularRusEncrypt, 2))

    for yCouple in yCombin:
        y1 = yCouple[0]
        y2 = yCouple[1]
        y3 = (y1 - y2) % (31 * 31)
        for xCouple in xCombin:
            x1 = xCouple[0]
            x2 = xCouple[1]
            x3 = (x1 - x2) % (31 * 31)

            a = linearEquation(x3, y3, 31 * 31)
            if a != -1:
                b = (y1 - a * x1) % (31 * 31)
                if checkLanguage(decryption(someText, a, b)) == 1:
                    return [a, b]


file = open(r"D:\5 semestr\crypto\labs\crypto-22-23\cp3\sotnikova_fb-01_strukalo_fb-01_cp3\variant3.txt", mode="r", encoding="utf-8")
# file = open(r"E:\_svv_92\KPI\V - Семестер\Крипта\Lab_3\variant3.txt", mode="r", encoding="utf-8")

variant3 = file.read()
file.close()

print('-------------------Зашифрований текст-------------------\n' + variant3)

key = attackFun(variant3)
if len(key) == 2:
    print('\nКлюч: a = ' + str(key[0]) + ', b = ' + str(key[1]))

    decrypt = decryption(variant3, key[0], key[1])

    print('\n-------------------Дешифрований текст-------------------\n' + decrypt)
else:
    print('\nТак вийшло, що ключ ми не змогли знайти.')


decrypt = decryption(variant3, 199, 700)
print('\n-------------------Дешифрований текст-------------------\n' + decrypt)
