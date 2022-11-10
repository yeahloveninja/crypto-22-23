from collections import Counter
from operator import itemgetter
from math import log

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
exception = ['аы', 'аь', 'йь', 'оы', 'уы', 'уь', 'чщ', 'чэ', 'ьы', 'яь', 'оь', 'ыь', 'еь', 'юь',
             'эь', 'ць', 'хь', 'кь', 'йь', 'иь', 'гь', 'еы', 'эы', 'иы', 'яы', 'юы', 'ыы', 'ьь']


def open_file(path_to_file):  # відкриваємо файл, читаємо текст
    with open(path_to_file, 'r', encoding='utf-8') as f:
        text_txt = f.read()
    my_text_enc = ''.join(i for i in text_txt if i in alphabet)
    return my_text_enc


def gcd(int_a, int_b):  # НСД рекурсивно
    if int_b == 0:
        return abs(int_a)
    else:
        return gcd(int_b, int_a % int_b)


def extended_euclid(a, n):  # пошук оберненого за розширеним алгоритмом Евкліда
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
    for i in range(2, len(result) - 1):
        result[i] = result[i - 2] + (-result[i]) * result[i - 1]
    return result[-2]


def modulo_equation(int_a, int_b, int_n):  # рівняння за модулем
    int_a, int_b = int_a % int_n, int_b % int_n
    d = gcd(int_a, int_n)  # НСД а та n
    array_x = []  # корені рівняння
    if d == 1:  # якщо НСД = 1, то 1 корінь
        array_x.append((extended_euclid(int_a, int_n) * int_b) % int_n)
        return array_x
    else:  # якщо НСД != 1, то 2 випадки
        if int_b % d != 0:  # немає коренів
            return array_x
        else:  # коренів буде рівно d
            int_a, int_b, int_n = int_a // d, int_b // d, int_n // d
            array_x.append((modulo_equation(int_a, int_b, int_n)[0]))
            for i in range(1, d):
                array_x.append(array_x[-1] + int_n)
            return array_x


def bigram_frequency(text):  # 5 найчастіших біграм тексту
    arr_bigrams = []
    for i in range(0, len(text) - 1, 2):
        arr_bigrams.append(text[i:i + 2])
    bigrams_count = Counter(arr_bigrams)
    sorted_tuples = sorted(bigrams_count.items(), key=itemgetter(1), reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}
    return list(sorted_dict.keys())[:5]


def convert(bigram):  # перевести біграму в її числове значення
    number = alphabet.index(bigram[0]) * 31 + alphabet.index(bigram[1])
    return number


def systems_of_equations(text):  # формування систем рівнянь на біграмах
    the_most_frequent_ru = ['ст', 'но', 'ен', 'то', 'на']
    the_most_frequent_text = bigram_frequency(text)
    bigrams, systems_equations = [], []
    for i in the_most_frequent_ru:
        for j in the_most_frequent_text:
            bigrams.append((i, j))  # пара найч. біграма мови - кожна найчастіша біграма тексту
    for i in bigrams:
        for j in bigrams:
            if i == j or (j, i) in systems_equations:
                continue
            elif i[0] == j[0] or i[1] == j[1]:  # бо одна й та сама біграма не може одночасно переходити у дві
                continue
            systems_equations.append((i, j))
    return systems_equations


def decrypt_affine(my_text, key_array):  # дешифрування афінного шифру
    arr_plaintext = []
    a, b = key_array[0], key_array[1]
    for i in range(0, len(my_text) - 1, 2):
        x = (extended_euclid(a, 31 ** 2) * (convert(my_text[i:i + 2]) - b)) % (31 ** 2)  # рівняння дешифрування
        arr_plaintext.append(alphabet[x // 31] + alphabet[x % 31])  # щоб знайти літери біграми (літера 1 буде
        # результатом цілочисельного ділення на 31, а літера 2 результатом ділення за модулем 31)
    plaintext_str = ''.join(i for i in arr_plaintext)
    return plaintext_str


def solutions(system_of_equations):  # знаходимо корені системи рівнянь
    keys = []
    x1, x2, y1, y2 = convert(system_of_equations[0][0]), convert(system_of_equations[1][0]), convert(
        system_of_equations[0][1]), convert(system_of_equations[1][1])
    # ((ст, цл),(но, ял)) ст -> цл, но -> ял
    a = modulo_equation(x1 - x2, y1 - y2, 31 ** 2)  # рівняння (2) з методички
    for i in a:
        if gcd(i, 31) != 1:
            continue
        b = (y1 - i * x1) % 31 ** 2  # відповідно знаючи a знаходимо відповідне b
        keys.append((i, b))  # отримуємо пари а, b
    return keys


def to_find_keys(text):  # ймовірні ключі
    arr_keys = []
    bigram_systems = systems_of_equations(text)  # системи біграм
    for i in bigram_systems:
        solutions_of_systems = solutions(i)  # ключі для і-ої системи біграм
        if len(solutions_of_systems) != 0:
            for j in range(len(solutions_of_systems)):
                # записую отримані пари ключів до arr_keys (якщо їх 1 або більше)
                arr_keys.append(solutions_of_systems[j])
    return arr_keys  # [(),(),()...]


def entropy(my_text):  # ентропія тексту
    count_letters = Counter(my_text)
    for i in count_letters:
        count_letters[i] /= len(my_text)
    result = -1 * sum(float(count_letters[i]) * log(count_letters[i], 2) for i in count_letters)
    return result


def except_values(my_text):     # перевірка чи є у тексті неможливі біграми
    x = 0
    for i in exception:
        if i in my_text:
            x = 1
            break
    return x


def keys_is_right(keys, enc_text):          # розпізнавач
    no_matches = "No matches :("
    for i in keys:
        dec = decrypt_affine(ciphertext, i)
        letters = list(dict(sorted(Counter(dec).items(),
                                   key=itemgetter(1), reverse=True)).keys())        # топ літер за спаданням зустрічі
        if letters[0] not in ['о', 'е']:            # якщо в тексті 1 літера топу не 'о' та не 'е', то skip
            continue
        elif except_values(dec) == 1:
            continue                  # якщо у тексті зустрілись неможливі біграми - skip
        e = entropy(decrypt_affine(enc_text, i))
        if (e > 4.2) and (e < 4.5):         # якщо ентропія тексту від 4.2 до 4.5 - то повернути ключ
            # взагалі ентропія мови ~4,35
            return i
    return no_matches


ciphertext = open_file('D:\\Python\\PycharmProjects\\crypto-22-23\\cp3\\kononets_fb-06_cp3\\07.txt')
a_b = keys_is_right(to_find_keys(ciphertext), ciphertext)
# print(a_b)
decrypt = decrypt_affine(ciphertext, a_b)
print(decrypt)
# with open("D:\\Python\\PycharmProjects\\crypto-22-23\\cp3\\kononets_fb-06_cp3\\07_dec.txt", 'w', encoding="utf-8") as f:
#     f.write(decrypt)
