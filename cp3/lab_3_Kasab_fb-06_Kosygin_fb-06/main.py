from nltk import FreqDist
from collections import Counter
from nltk.util import ngrams
from math import log2

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

with open("text.txt", "r", encoding="utf-8") as f:
    x = f.read()
    text_c = x.replace("\n", "")
    f.close()
print(text_c)

def entropy(text):  # ентропія тексту
    all_let = [Counter(text)[i] / len(text) for i in Counter(text)]
    return sum(all_t / sum(all_let) * log2(sum(all_let) / all_t) for all_t in all_let)

def revers(a, b):  # обернене з розширеним алгоритмом евкліда
    if ext_euc(a, b)[0] != 1:
        return None
    else:
        _, _, y = ext_euc(b, a % b)
        return y

def ext_euc(a, b):  # розширений алгоритм евкліда
    if a == 0:
        return b, 0, 1
    gcd, _, __ = ext_euc(b % a, a)
    x = __ - (b // a) * _
    y = _
    return gcd, x, y

def best_bi(text):  # пошук 5 найчастіших біграм
    bigramfdist = FreqDist()
    bigrams = ngrams(text, 2)
    bigramfdist.update(bigrams)
    return [i[0][0] + i[0][1] for i in bigramfdist.most_common()[:5]]

def bi_to_num(bi):  # перетворення біграм в число
    return alphabet.index(bi[0]) * 31 + alphabet.index(bi[1])

def mix_bi(text):  # знаходження всіх можливих варіантів біграм
    top_5_bi = ['ст', 'но', 'то', 'на', 'ен']
    top_5_bi_text, all_bi = best_bi(text), []
    return [[[pair1_bi1, pair1_bi2], [pair2_bi1, pair2_bi2]] for pair1_bi2 in top_5_bi_text for pair1_bi1 in top_5_bi
            for pair2_bi2 in top_5_bi_text if pair2_bi2 != pair1_bi2 for pair2_bi1 in top_5_bi
            if pair2_bi1 != pair1_bi1]

def pass_text(text): # перевірка тексту
    unreal_bi = ['аы', 'аь', 'йь', 'оы', 'уы', 'уь', 'чщ', 'чэ', 'ьы', 'яь', 'оь', 'ыь', 'еь', 'юь',
                 'эь', 'ць', 'хь', 'кь', 'йь', 'иь', 'гь', 'еы', 'эы', 'иы', 'яы', 'юы', 'ыы', 'ьь']
    return 4.2 < entropy(text) < 4.5 and sorted(Counter(text).items(), key=lambda let:
    (let[1], let[0]), reverse=True)[0][0] in ["о", "е"] and not any(ext in text for ext in unreal_bi)

def find_solv(a, b, n):
    x, result = ext_euc(a, n)[0], []
    if x == 1:
        rev = revers(a, n)
        if isinstance(rev, int):
            result.append((rev * b) % n)
    elif b % x == 0:
        if revers(a / x, n / x) is not None:
            return [((revers(a / x, n / x) * b / x) % (n / x) + i * n / x) for i in range(int(x))]

    return result

def pass_keys(text):
    all_keys, all_bi = [], mix_bi(text)
    for bi_sy in all_bi:
        x1 = bi_to_num(bi_sy[0][0])
        x2 = bi_to_num(bi_sy[1][0])
        y1 = bi_to_num(bi_sy[0][1])
        y2 = bi_to_num(bi_sy[1][1])
        a = find_solv(x1 - x2, y1 - y2, pow(31, 2))
        for i in a:
            if ext_euc(i, 31)[0] != 1:
                continue
            b = (y1 - i * x1) % pow(31, 2)
            all_keys.append([int(i), int(b)])
    return all_keys

def affine_decoder(text, keys):
    decode = ""
    key1, key2 = keys
    for i in range(0, len(text), 2):
        part1 = (ext_euc(key1, pow(31, 2))[1] * (bi_to_num(text[i:i + 2]) - key2))
        decode += alphabet[part1 % pow(31, 2) // 31] + alphabet[part1 % 31]
    return decode


all_keys = pass_keys(text_c)
print(all_keys)
keys = []
for i in all_keys:
    if pass_text(affine_decoder(text_c, i)):
        keys = i
        break
print(keys)
print(affine_decoder(text_c, keys))