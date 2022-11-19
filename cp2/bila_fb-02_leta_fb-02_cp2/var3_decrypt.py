import re
import math
import pandas as pd
from collections import Counter
from lab2_encrypt import find_i
from itertools import cycle

with open("var3_text copy.txt", encoding='utf8') as file:
    file_to_decrypt = file.read()

alphabet_without_spaces = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
al = []
for a in alphabet_without_spaces:
    al.append(a)

def letters_frequency(txt):  # функція для підрахунку частоти букв
    c = Counter()
    frequency = {}
    total = 0
    for line in txt:
        c += Counter(line)  # рахуємо скільки разів зустрічається кожна літера в тексті
    for letter in alphabet_without_spaces:
        frequency[letter] = c[letter]/len(txt)
    return frequency


def to_separate_blocks(txt, period):
    separated_txt = []
    for i in range(0, period):  # записуємо літери тексту у блок
        separated_txt.append(txt[i])
        i += 1
    for j in range(period, len(txt)):  # записуємо літери по їх відповідності до періоду
        separated_txt[j % period] += txt[j]
        j += 1
    return separated_txt


def blocks_index(txt, length):
    period = to_separate_blocks(txt, length)
    for i in range(0, len(period)):
        i += find_i(period[i], al)
    i /= len(period)
    return i


def total_index(arr):
    total = 0
    for element in arr:
        total += find_i(element, al)
    total /= len(arr)
    return total


def key_out(val, dictionary):
    for key, value in dictionary.items():
        if val == value:
            return key


def to_count_key_size(txt):
    theoretical_i = 0.05  # з частот першого комп. практикуму (0.05751442686466821)
    all_i = {}
    for k in range(2, 32):
        all_i[k] = total_index(to_separate_blocks(txt, k))
    print(all_i)
    all_i_data = pd.DataFrame(all_i, index=["index"])
    all_i_data.to_excel("indexes.xlsx")
    all_keys = []
    for exp_i in all_i.values():
        if exp_i > theoretical_i:
            all_keys.append(exp_i)
    key_size = key_out(min(all_keys), all_i)
    return key_size


def fr(text):
    freq = {}
    for i in text:
        freq[i] = text.count(i)/len(text)
    k = 0
    k = dict(sorted(freq.items()))
    return k



def to_reveal_key(periods):
    mode_letters = []  # список найчастіших літер у кожному блоці шифрованого тексту
    for period in periods:
        frequency = letters_frequency(period)
        r = key_out(max(frequency.values()), frequency)
        mode_letters.append(r)
    all_keys = []  # значення ключа
    for l in mode_letters:
        key = (al.index(l) - al.index(mode_letters[0])) % len(al)
        all_keys.append(key)
    print(all_keys)
    letters = []
    for letter in all_keys:
        letters.append(al[letter])
    result_key = ''.join(letters)
    return result_key


def test(txt, key):
    cipher = ''  # зашифрований текст
    first_letter = ord(al[0])  # отримуємо аскіі першої літери
    j = 0
    while j < len(txt):  # перебираємо кожну літеру тексту
        letter = txt[j]
        key_letter = key[j % len(key)]  # літера ключа
        encrypted_letter = (ord(letter) - first_letter - ord(key_letter) + first_letter) % len(al)  # зашифрована літера
        cipher += al[encrypted_letter]  # зашифрований текст
        j += 1
    encrypted_data = ''.join([letter for letter in cipher])
    name = open('decrypted_text.txt', 'w', encoding='utf8')
    name.write(encrypted_data)
    return encrypted_data


#print(find_i(file_to_decrypt))

print(to_count_key_size(file_to_decrypt))
print(to_reveal_key(to_separate_blocks(file_to_decrypt, 14)))
print(test(file_to_decrypt, 'экомаятникфуко'))
#print(test(alphabet_without_spaces, 'б'))
to_reveal_key(file_to_decrypt)
letters_frequency(file_to_decrypt)
