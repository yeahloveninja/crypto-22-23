import collections
import itertools
import numpy


def inverse_input(a, b):
    d, x = eu_ext(a, b)
    return (d, x % b) if d == 1 else (d, None)


def bigram_to_number(bigram):
    return charlist.find(bigram[0]) * 31 + charlist.find(bigram[1])


def entropy(string, s_len, n=1):
    return - sum({i: string[i] / s_len * numpy.log2(string[i] / s_len) for i in string}.values()) / n


def get_second_key_element(x1, y1, a):
    x1, y1 = (charlist.index(x1[0]) * len(charlist) + charlist.index(x1[1]),
              charlist.index(y1[0]) * len(charlist) + charlist.index(y1[1]))
    return (y1 - a * x1) % pow(len(charlist), 2)


def bigram_frequency(string, sort=True):
    qnext = 1
    f_dict = {}
    for i in range(0, len(string) - 1, qnext):
        c_str = string[i] + string[i+1]
        if c_str in f_dict:
            f_dict[c_str] += 1
        else:
            f_dict[c_str] = 1
    if not sort:
        return f_dict
    else:
        return sorted(f_dict.items(), key=lambda x: (x[1], x[0]), reverse=True)


def calculation_linear_equation(a, b, m):
    d = inverse_input(a, m)[0]
    if inverse_input(a, m)[1]:
        return [(inverse_input(a, m)[1] * b) % m]
    if not b % d:
        a, b, m = a / d, b / d, m / d
        q = ([int((b * inverse_input(a, m)[1]) % m +
        (i - 1) * m) for i in range(1,d+1)])
        return q


def first_key(*args):
    q = [charlist.index(i[0]) * len(charlist) + charlist.index(i[1]) for i in args]
    qx = calculation_linear_equation(q[2] - q[3], q[0] - q[1], pow(len(charlist), 2))
    if qx is not None:
        return [x for x in [inverse_input(i, pow(len(charlist),2))[1] for i in qx] if x is not None]


def text_verification(f_list_s, f_list_big, t_len):
    return entropy(f_list_s, t_len) < 4.5 and entropy(f_list_big, t_len, n=2) < 4.2


def eu_ext(a, b):
    x0 = 1
    x1 = 0
    while b:
        comp = a % b
        x0, x1 = x1, x0 - a // b * x1
        a, b = b, comp
    return a, x0


def decryption(string, key):
    fstr = ''
    lenq = len(charlist)
    for i in range(0, len(string), 2):
        inverser = inverse_input(key[0], pow(len(charlist), 2))[1]
        indexer1 = charlist.index(string[i]) * lenq
        indexer2 = charlist.index(string[i + 1])
        fstr += (charlist[(inverser * (indexer1 + indexer2 - key[1]) % pow(lenq, 2)) // lenq] +
                 charlist[(inverser * (indexer1 + indexer2 - key[1]) % pow(lenq, 2)) % lenq])
    return fstr


def gen_key(string, f_size=5):
    f_list = bigram_frequency(string)[:f_size]
    for i in itertools.permutations(('ст', 'но', 'то', 'на', 'ен'), 2):
        for j in range(len(f_list) - 1):
            if first_key(i[0], i[1], f_list[j][0], f_list[j + 1][0]) is None:
                continue
            for solution in first_key(i[0], i[1], f_list[j][0], f_list[j + 1][0]):
                key = solution, get_second_key_element(i[0], f_list[j][0], solution)
                if corre := (
                    text_verification(
                        collections.Counter(decryption(string, key)),
                        bigram_frequency(
                            decryption(string, key), sort=False
                        ),
                        len(decryption(string, key)),
                    )
                ):
                    return decryption(string, key), key


c_text = open("cipher_text.txt", "r", encoding="utf-8").read().replace("\n", "")
charlist = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
ciphertext = c_text
print(bigram_frequency(ciphertext)[:5])
answer = gen_key(ciphertext)
print(answer[0][:40],answer[1])
with open("decrypt.txt", "w", encoding='utf-8') as f:
    f.write(answer[0])