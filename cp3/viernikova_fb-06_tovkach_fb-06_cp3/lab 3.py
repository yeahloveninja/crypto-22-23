from collections import Counter

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
non_existent = ['аы', 'аь', 'йь', 'оы', 'фь', 'йй', 'уы', 'уь', 'чщ', 'чэ', 'ьы', 'яь', 'оь', 'ыь', 'еь', 'юь',
             'эь', 'ць', 'хь', 'кь', 'йь', 'ээ', 'иь', 'гь', 'еы', 'эы', 'иы', 'яы', 'юы', 'ыы', 'ьь']
with open('C:\\Users\\katri\\Desktop\\KPI\\Crypto\\lab3\\10.txt', 'r', encoding='utf-8') as file:
    txt = file.read()
m = len(alphabet)


def gcd(a, b):
    if b == 0:
        return abs(a)
    else:
        return gcd(b, a % b)


def euclid(a, n):
    scheme = [0, 1]
    while a != 0 and n != 0:
        if n > a:
            scheme.append(n // a)
            n = n % a
        elif n < a:
            scheme.append(a // n)
            a = a % n
    for i in range(2, len(scheme)-1):
        scheme[i] = scheme[i - 2] + (-scheme[i]) * scheme[i - 1]
    return scheme[-2]


def equations(a, b, mod):
    a, b = a % mod, b % mod
    d = gcd(a, mod)
    k = []
    if d == 1:
        k.append((euclid(a, mod) * b) % mod)
        return k
    else:
        if b % d == 0:
            a = a // d
            b = b // d
            mod = mod // d
            k.append((equations(a, b, mod)[0]))
            for i in range(1, d):
                k.append(k[-1] + mod)
            return k
        else:
            return k


def decr(file_txt, keys):
    decr_text = []
    a, b = keys[0], keys[1]
    for i in range(0, len(file_txt) - 1, 2):
        x = (euclid(a, 31 ** 2) * (str_to_num(file_txt[i:i + 2]) - b)) % (31 ** 2)
        decr_text.append(alphabet[x // 31] + alphabet[x % 31])
    text = ''.join(i for i in decr_text)
    return text


def top5_bigr(text):
    bigrams = []
    for i in range(0, len(text) - 1, 2):
        bigrams.append(text[i:i + 2])
    return list(dict(sorted(Counter(bigrams).items(), key=lambda item: item[1], reverse=True)).keys())[:5]


def eq_systems(text):
    bigrams = []
    equation_sys = []
    top_text = top5_bigr(text)
    top_lang = ['ст', 'но', 'ен', 'то', 'на']
    for b in top_lang:
        for b2 in top_text:
            bigrams.append((b, b2))
    for b in bigrams:
        for b2 in bigrams:
            if b[0] == b2[0] or b[1] == b2[1]:
                continue
            elif b == b2 or (b2, b) in equation_sys:
                continue
            equation_sys.append((b, b2))
    return equation_sys


def create_keys(text):
    keys = []
    systems = eq_systems(text)
    for i in systems:
        result = results(i)
        if len(result) != 0:
            for j in range(len(result)):
                keys.append(result[j])
    return keys


def str_to_num(bigram):
    number = alphabet.index(bigram[0]) * 31 + alphabet.index(bigram[1])
    return number


def results(system):
    keys = []
    x1, y1, x2, y2 = str_to_num(system[0][0]), str_to_num(system[0][1]), \
                     str_to_num(system[1][0]), str_to_num(system[1][1])
    a = equations(x1 - x2, y1 - y2, m ** 2)
    for i in a:
        if gcd(i, m) != 1:
            continue
        b = (y1 - i * x1) % m ** 2
        keys.append((i, b))
    return keys


def except_letters(text):
    x = 0
    for i in non_existent:
        if i in text:
            x = 1
            break
    return x


def my_key_is(keys):
    for i in keys:
        letters = list(dict(sorted(Counter(decr(encrypted, i)).items(),
                                   key=lambda item: item[1], reverse=True)).keys())
        if letters[0] not in ['о', 'е']:
            continue
        except_l = except_letters(decr(encrypted, i))
        if except_l == 0:
            return i


encrypted = ''.join(l for l in txt if l in alphabet)
print(top5_bigr(encrypted))
print(my_key_is(create_keys(encrypted)))
ab = my_key_is(create_keys(encrypted))
print(decr(encrypted, ab))

