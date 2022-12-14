from collections import Counter
from itertools import permutations
from math import log2

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
most_frequent_bigrams = 'ст', 'но', 'то', 'на', 'ен'
exception = ['аы', 'аь', 'йь', 'оы', 'уы', 'уь', 'чщ', 'чэ', 'ьы', 'яь', 'оь', 'ыь', 'еь', 'юь',
             'эь', 'ць', 'хь', 'кь', 'йь', 'иь', 'гь', 'еы', 'эы', 'иы', 'яы', 'юы', 'ыы', 'ьь']

c_text = open("cipher_text.txt", "r", encoding="utf-8").read().replace("\n", "")


def extended_euclid(a: float, b: float) -> [float]:
    x0, x1 = 1, 0

    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
    return a, x0


def get_inverse(a: int or float, b: int or float) -> [float, None or float]:
    d, x = extended_euclid(a, b)
    if d == 1:
        return d, x % b
    return d, None


def bigram_to_number(bigram: list) -> float:
    return alphabet.find(bigram[0]) * 31 + alphabet.find(bigram[1])


def entropy(string: dict, s_len: int, n=1) -> float:
    return -sum({i: string[i] / s_len * log2(string[i] / s_len) for i in string}.values()) / n


def bigram_frequency(string: str, step=1, sort=True) -> dict:
    f_dict = {}

    for i in range(0, len(string) - 1, step):
        if string[i] + string[i + 1] in f_dict:
            f_dict[string[i] + string[i + 1]] += 1
        else:
            f_dict[string[i] + string[i + 1]] = 1

    return sorted(f_dict.items(), key=lambda x: (x[1], x[0]), reverse=True) if sort else f_dict


def solve_linear_comparison(a: float, b: float, m: float) -> list:
    d, a_inv = get_inverse(a, m)
    if a_inv:
        return [(a_inv * b) % m]
    if not b % d:
        a, b, m = a / d, b / d, m / d
        x0 = (b * get_inverse(a, m)[1]) % m
        return [int(x0 + (i - 1) * m) for i in range(1, d + 1)]


def get_first_key_element(x1: str, x2: str, y1: str, y2: str) -> [list[int], None]:
    x1 = alphabet.index(x1[0]) * len(alphabet) + alphabet.index(x1[1])
    x2 = alphabet.index(x2[0]) * len(alphabet) + alphabet.index(x2[1])

    y1 = alphabet.index(y1[0]) * len(alphabet) + alphabet.index(y1[1])
    y2 = alphabet.index(y2[0]) * len(alphabet) + alphabet.index(y2[1])

    results = solve_linear_comparison(y1 - y2, x1 - x2, len(alphabet) ** 2)
    if results is not None:
        return [x for x in [get_inverse(i, len(alphabet) ** 2)[1] for i in results] if x is not None]


def get_second_key_element(x1: str, y1: str, a: [list]) -> int:
    x1 = alphabet.index(x1[0]) * len(alphabet) + alphabet.index(x1[1])
    y1 = alphabet.index(y1[0]) * len(alphabet) + alphabet.index(y1[1])

    return (y1 - a * x1) % len(alphabet) ** 2


def check_text_correctness(f_list_s: dict, f_list_big: dict, t_len: int) -> bool:
    """
    :param f_list_s: словник частоти букв в тексті
    :param f_list_big: словник частоти біграм в тексті
    :param t_len: text length
    :return: bool
    """
    return entropy(f_list_s, t_len) < 4.5 and entropy(f_list_big, t_len, n=2) < 4.2


def decrypt_affine(string: str, key: tuple[int, int]) -> str:
    new_str = ''
    for i in range(0, len(string), 2):
        x = (get_inverse(key[0], len(alphabet) ** 2)[1] * (alphabet.index(string[i]) * len(alphabet) +
                                                           alphabet.index(string[i + 1]) - key[1])) % len(alphabet) ** 2
        new_str += alphabet[x // len(alphabet)] + alphabet[x % len(alphabet)]
    return new_str


def gnc_keys(string: str, f_size=5) -> str:
    """
    Генерація та перевірка ключів
    :param string: CT (str)
    :param f_size: кількість часто використовуваних біграм, які будуть генерувати ключі
    """
    f_list = bigram_frequency(string)[:f_size]
    print(f_list)
    for i in permutations(most_frequent_bigrams, 2):
        for j in range(len(f_list) - 1):
            key_1 = get_first_key_element(i[0], i[1], f_list[j][0], f_list[j + 1][0])
            if key_1 is None:
                continue

            for solution in key_1:
                key = solution, get_second_key_element(i[0], f_list[j][0], solution)
                d_text = decrypt_affine(string, key)
                if check_text_correctness(Counter(d_text), bigram_frequency(d_text, sort=False), len(d_text)):
                    print(key)
                    return d_text


answer = gnc_keys(c_text)
print(answer[:40])
with open("decrypt.txt", "w", encoding='utf-8') as f:
    f.write(answer)
