from collections import Counter
from operator import itemgetter
from math import log

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
def nsd(a, b): # нсд
    while a*b != 0:
        if a >= b:
            a = a % b
        else:
            b = b % a
    return a + b


def bezout(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return x


def uravnenie(a, b, n):
    a, b = a % n, b % n
    d = nsd(a, n)
    x = []
    if d == 1:
        x.append((bezout(a, n) * b) % n)
        return x
    else:
        if b % d != 0:
            return x
        else:
            a, b, n = a // d, b // d, n // d
            x.append((uravnenie(a, b, n)[0]))
            for i in range(1, d):
                x.append(x[-1] + n)
            return x


def negr(text):
    tabor = []
    for i in range(0, len(text) - 1, 2):
        tabor.append(text[i:i + 2])
    negr_count = Counter(tabor)
    sorted_cortezhes = sorted(negr_count.items(), key=itemgetter(1), reverse=True)
    sorted_slovar = {key: value for key, value in sorted_cortezhes}
    return list(sorted_slovar.keys())[:5]


def transform(bigram):
    nomer = alphabet.index(bigram[0]) * 31 + alphabet.index(bigram[1])
    return nomer


def systems_uravneniya(text):
    mostpopularRUletter = ['ст', 'но', 'ен', 'то', 'на']
    mostpopularRUtext = negr(text)
    print(mostpopularRUtext)
    bigrams, systems_uravneniyas = [], []
    for i in mostpopularRUletter:
        for j in mostpopularRUtext:
            bigrams.append((i, j))
    for i in bigrams:
        for j in bigrams:
            if i == j or (j, i) in systems_uravneniyas:
                continue
            elif i[0] == j[0] or i[1] == j[1]:
                continue
            systems_uravneniyas.append((i, j))
    return systems_uravneniyas


def superdupersecretAfinne(secrettext, secretkey):
    notsecretletters = []
    a, b = secretkey[0], secretkey[1]
    for i in range(0, len(secrettext) - 1, 2):
        x = (bezout(a, 31 ** 2) * (transform(secrettext[i:i + 2]) - b)) % (31 ** 2)
        notsecretletters.append(alphabet[x // 31] + alphabet[x % 31])
    notsecrettext = ''.join(i for i in notsecretletters)
    return notsecrettext


def result(systems_uravneniya):
    kluch = []
    x1, x2, y1, y2 = transform(systems_uravneniya[0][0]), transform(systems_uravneniya[1][0]), transform(
        systems_uravneniya[0][1]), transform(systems_uravneniya[1][1])
    a = uravnenie(x1 - x2, y1 - y2, 31 ** 2)
    for i in a:
        if nsd(i, 31) != 1:
            continue
        b = (y1 - i * x1) % 31 ** 2
        kluch.append((i, b))
    return kluch


def findingkeys(text):
    keys_box = []
    bigr_syst = systems_uravneniya(text)
    for i in bigr_syst:
        sys_solutions = result(i)
        if len(sys_solutions) != 0:
            for j in range(len(sys_solutions)):
                keys_box.append(sys_solutions[j])
    return keys_box


def entropy(opentxt):
    amountofletters = Counter(opentxt)
    for i in amountofletters:
        amountofletters[i] /= len(opentxt)
    answer = -1 * sum(float(amountofletters[i]) * log(amountofletters[i], 2) for i in amountofletters)
    return answer


def correctkey(keys, cyphertext):
    no_matches = "net sovpadeni"
    for i in keys:
        e = entropy(superdupersecretAfinne(cyphertext, i))
        if (e > 4.0) and (e < 4.5):
            return i
    return no_matches


with open("1.txt", 'r', encoding='utf-8') as f:
        txt = f.read()
mineenctext = ''.join(i for i in txt if i in alphabet)
ciphertext = mineenctext
a_b = correctkey(findingkeys(ciphertext), ciphertext)
print(a_b)
antisecret = superdupersecretAfinne(ciphertext, a_b)
print(antisecret)
with open("1decrypted.txt", 'w', encoding="utf-8") as f:
    f.write(antisecret)