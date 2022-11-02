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


def systems_of_equations(text):     # формування систем рівнянь
    the_most_frequent_ru = ['ст', 'но', 'ен', 'то', 'на']
    the_most_frequent_text = bigram_frequency(text)
    bigrams, systems_equations = [], []
    for i in the_most_frequent_ru:
        for j in the_most_frequent_text:
            bigrams.append((i, j))
    for i in bigrams:
        for j in bigrams:
            if i == j or (j, i) in systems_equations:
                continue
            systems_equations.append((i, j))
    return systems_equations


def decrypt_affine(my_text, key_array):     # дешифрування афінного шифру
    arr_plaintext = []
    a, b = key_array[0], key_array[1]
    for i in range(0, len(my_text) - 1, 2):
        x = (extended_euclid(a, 31 ** 2) * (convert(my_text[i:i + 2]) - b)) % (31 ** 2)  # рівняння дешифрування
        arr_plaintext.append(alphabet[x // 31] + alphabet[x % 31])  # щоб знайти літери біграми (літера 1 буде
        # результатом цілочисельного ділення на 31, а літера 2 результатом ділення за модулем 31)
    plaintext_str = ''.join(i for i in arr_plaintext)
    return plaintext_str


def solutions(system_of_equations):
    keys = []
    x1, x2, y1, y2 = convert(system_of_equations[0][0]), convert(system_of_equations[1][0]), \
                     convert(system_of_equations[0][1]), convert(system_of_equations[1][1])
    a = modulo_equation(x1 - x2, y1 - y2, 31 ** 2)
    for i in a:
        if gcd(i, 31) != 1:
            continue
        b = (y1 - i * x1) % 31 ** 2
        keys.append((i, b))
    return keys
