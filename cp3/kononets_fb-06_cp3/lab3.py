from collections import Counter
from operator import itemgetter
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'


def open_file(path_to_file):        # відкриваємо файл, читаємо текст
    with open(path_to_file, 'r', encoding='utf-8') as f:
        text_txt = f.read()
    my_text_enc = ''.join(i for i in text_txt if i in alphabet)
    return my_text_enc


def gcd(int_a, int_b):           # НСД рекурсивно
    if int_b == 0:
        return abs(int_a)
    else:
        return gcd(int_b, int_a % int_b)


def extended_euclid(a, n):      # пошук оберненого за розширеним алгоритмом Евкліда
    result = [0, 1]
    while a != 0 and n != 0:
        if a > n:
            result.append(a // n)
            a = a % n
        elif n > a:
            result.append(n // a)
            n = n % a
        else:
            print("Оберненого не існує :(")
    for i in range(2, len(result)-1):
        result[i] = result[i - 2] + (-result[i]) * result[i - 1]
    return result[-2]


def modulo_equation(int_a, int_b, int_n):           # рівняння за модулем
    int_a, int_b = int_a % int_n, int_b % int_n
    d = gcd(int_a, int_n)   # НСД а та n
    array_x = []            # корені рівняння
    if d == 1:              # якщо НСД = 1, то 1 корінь
        array_x.append((extended_euclid(int_a, int_n) * int_b) % int_n)
        return array_x
    else:        # якщо НСД != 1, то 2 випадки
        if int_b % d != 0:   # немає коренів
            return array_x
        else:    # коренів буде рівно d
            int_a, int_b, int_n = int_a // d, int_b // d, int_n // d
            array_x.append((modulo_equation(int_a, int_b, int_n)[0]))
            for i in range(1, d):
                array_x.append(array_x[-1] + int_n)
            return array_x


def bigram_frequency(text):         # 5 найчастіших біграм тексту
    arr_bigrams = []
    for i in range(0, len(text) - 1, 2):
        arr_bigrams.append(text[i:i + 2])
    bigrams_count = Counter(arr_bigrams)
    sorted_tuples = sorted(bigrams_count.items(), key=itemgetter(1), reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}
    return list(sorted_dict.keys())[:5]


def convert(bigram):                # перевести біграму в її числове значення
    number = alphabet.index(bigram[0]) * 31 + alphabet.index(bigram[1])
    return number
