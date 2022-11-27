import re
from collections import Counter
import matplotlib.pyplot as plt

alphabet = 'абвгдеэжзийклмнопрстуфхцчшщъыьэюя'  # без 'ё'
indexed_alphabet = {i: num for num, i in enumerate(alphabet)}
print(indexed_alphabet)
keys = ['но', 'кот', 'пьет', 'узвар', 'сверхоблагодетель']


def prettify_text(text_path):
    plain_text = open(text_path, encoding='utf-8')
    pt = plain_text.read()
    plain_text.close()
    pt = pt.replace("\n", "")
    pt = pt.lower()
    pt = pt.replace(" ", "").replace("  ", " ")
    pt = re.sub(r'[^а-яё]', '', pt)
    pt = pt.replace("ё", "е")  # без 'ё'
    return pt


def vignere_encrypt(plain_text, key, filename, alphabet):
    # повторити ключ стільки разів скільки треба для покриття всього тексту
    key_length = len(key)
    cipher_text = ''
    counter_key = 0
    for letter in plain_text:
        cipher_text += alphabet[(alphabet.index(letter) + alphabet.index(key[counter_key])) % 32]
        counter_key += 1
        if counter_key >= key_length:
            counter_key = 0
    ciphert_text_file = open(filename, 'w+', encoding='utf-8')
    ciphert_text_file.write(cipher_text)
    return cipher_text


def calculate_index_of_coincedence(text):
    # plain text
    text_length = len(text)
    letter_frequency = Counter(text)
    index_of_coincedence = 0
    for l in letter_frequency:
        index_of_coincedence += letter_frequency[l] * (letter_frequency[l] - 1)
    return round(index_of_coincedence / (text_length * (text_length - 1)), 6)


def determine_period(text, alphabet_len):
    ic_dict = {}
    for key_length in range(2, alphabet_len):
        index = 0
        for i in range(key_length):
            index += calculate_index_of_coincedence(text[i::key_length])
        index /= key_length
        ic_dict[key_length] = index
    return ic_dict


def caesar_encrypt(text_block, key, alphabet):
    shifted_block = ''
    for letter in text_block:
        index_in_alphabet = alphabet.index(letter)
        index_shifted = (index_in_alphabet + key) % (len(alphabet) - 1)
        shifted_block += alphabet[index_shifted]
    return shifted_block


def chi_squared_statistic(encrypted_text, key_length, letter_frequency, alphabet):
    expected_key = ''
    for i in range(key_length):
        block = encrypted_text[i::key_length]
        letter_of_key = find_min_chi_squared(block, letter_frequency, alphabet)
        expected_key += alphabet[letter_of_key]
    return expected_key


def find_min_chi_squared(block, letter_frequency, alphabet):
    chi_square = {}
    block_length = len(block)
    for key in range(len(alphabet)): # бо треба шукати значення узгодженості пірса для всієї кількості моєливих ключів
        caesar_block = caesar_encrypt(block, key, alphabet) # зміщуємо блок
        given_letter_frequency = Counter(caesar_block)
        c_s_total = 0
        for letter in alphabet:
            expected_quantity = letter_frequency[letter] * block_length
            if letter in caesar_block:
                given_quantity = given_letter_frequency[letter]
            else:
                given_quantity = 0
                # print('hahaha ==> ', ((abs(given_quantity - expected_quantity))**2) / expected_quantity)
            c_s = ((abs(given_quantity - expected_quantity))**2) / expected_quantity
            c_s_total += c_s
        chi_square[key] = c_s_total
    # plt.bar(range(len(chi_square)), list(chi_square.values()), align='center')
    # plt.xticks(range(len(chi_square)), list(chi_square.keys()))
    # plt.show()
    # print(chi_square)
    return min(chi_square, key=chi_square.get)


#
# def vigener_decrypt()

plain_text = prettify_text('pt_task1.txt')
encrypted_text = prettify_text('ct_var2.txt')
# TASK 1
# vignere_encrypt(plain_text, keys[0], 'task1_keys[0].txt', alphabet)
# vignere_encrypt(plain_text, keys[1], 'task1_keys[1].txt', alphabet)
# vignere_encrypt(plain_text, keys[2], 'task1_keys[2].txt', alphabet)
# vignere_encrypt(plain_text, keys[3], 'task1_keys[3].txt', alphabet)
# vignere_encrypt(plain_text, keys[4], 'task1_keys[4].txt', alphabet)

# TASK 2
# ic_plain_text = calculate_index_of_coincedence(plain_text)

# ic_key0 = calculate_index_of_coincedence(open('task1_keys[0].txt', encoding='utf-8').read())
# ic_key1 = calculate_index_of_coincedence(open('task1_keys[1].txt', encoding='utf-8').read())
# ic_key2 = calculate_index_of_coincedence(open('task1_keys[2].txt', encoding='utf-8').read())
# ic_key3 = calculate_index_of_coincedence(open('task1_keys[3].txt', encoding='utf-8').read())
# ic_key4 = calculate_index_of_coincedence(open('task1_keys[4].txt', encoding='utf-8').read())
# print(ic_plain_text,ic_key0, ic_key1, ic_key2, ic_key3, ic_key4)

# TASK 3
ic_for_different_periods = determine_period(open('ct_var2.txt', encoding='utf-8').read(), len(alphabet))
# print(ic_for_different_periods)
print(max(ic_for_different_periods, key=ic_for_different_periods.get))
# plt.bar(range(len(ic_for_different_periods)), list(ic_for_different_periods.values()), align='center')
# plt.xticks(range(len(ic_for_different_periods)), list(ic_for_different_periods.keys()))
# plt.show()
letter_frequency_from_lab1 = {'а': 0.0812955355, 'б': 0.0167278024, 'в': 0.0465636711, 'г': 0.0189788603,
                              'д': 0.0311363331, 'е': 0.0879716934, 'э': 0.0035537228, 'ж': 0.0115677529,
                              'з': 0.0173087206, 'и': 0.0637843737, 'ы': 0.0174165425, 'й': 0.0103707094,
                              'к': 0.0327998715, 'л': 0.0464954572, 'м': 0.0307600566, 'н': 0.0670190317,
                              'о': 0.111932367, 'п': 0.0272239373, 'р': 0.0394870317, 'с': 0.0532926397,
                              'т': 0.0630362216, 'у': 0.0262029297, 'ф': 0.0022114498, 'х': 0.0070788398,
                              'ц': 0.0032610633, 'ч': 0.018446352, 'ш': 0.0083418967, 'щ': 0.0029552011,
                              'ъ': 0.0002200448, 'ь': 0.0226382046, 'ю': 0.0059544111, 'я': 0.0239672749}

#print(chi_squared_statistic(encrypted_text, 14, letter_frequency_from_lab1, alphabet))

# print(chi_squared_statistic(open('task1_keys[0].txt', encoding='utf8').read(), 2, letter_frequency_from_lab1, alphabet))

encrypted = caesar_encrypt(open('for_testing.txt', encoding='utf8').read(), -3, alphabet) # wtf
print(chi_squared_statistic(encrypted, 1, letter_frequency_from_lab1, alphabet))
# # print(caesar_encrypt('абвг', 4, alphabet))

# print(len("жосвеыдиадозор"))
