import re
import pandas as pd
from collections import Counter

with open("var3_text copy.txt", encoding='utf8') as file:
    file_to_decrypt = file.read()

with open("text.txt", encoding='utf8') as file:
    text = file.read()

alphabet_without_spaces = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
al = []
for a in alphabet_without_spaces:
    al.append(a)

splited = re.compile('[^а-яА-Я ]').sub('', text).rstrip('.,').lower().split(' ')
clean = ''.join(splited)
clean_text = open('clean_text.txt', 'w')
clean_text.write(clean)

key_2 = 'он'
key_3 = 'нет'
key_4 = 'кино'
key_5 = 'земля'
key_20 = 'методполиалфавитного'

al_indexes = [i for i in range(len(al))]
thesaurus = {key: value for key, value in zip(al, al_indexes)}  # літера: індекс
returned_thesaurus = {key: value for key, value in zip(al_indexes, al)}  # індекс: літера

mode_letters = ['о', 'е', 'а', 'и', 'н', 'т']  # найпопулярніші літери в рос. алфавіті


def to_encrypt(txt, key):  # зашифровуємо текст ключами
    cipher = ''  # зашифрований текст
    first_letter = ord(al[0])  # отримуємо аскіі першої літери
    j = 0
    while j < len(txt):  # перебираємо кожну літеру тексту
        letter = txt[j]
        key_letter = key[j % len(key)]  # літера ключа
        encrypted_letter = (ord(letter) - first_letter + ord(key_letter) - first_letter) % len(al)  # зашифрована літера
        cipher += al[encrypted_letter]  # зашифрований текст
        j += 1
    encrypted_data = ''.join([letter for letter in cipher])
    if key == key_2:
        name = open('key_2_text.txt', 'w', encoding='utf8')
        name.write(encrypted_data)
    if key == key_3:
        name = open('key_3_text.txt', 'w', encoding='utf8')
        name.write(encrypted_data)
    if key == key_4:
        name = open('key_4_text.txt', 'w', encoding='utf8')
        name.write(encrypted_data)
    if key == key_5:
        name = open('key_5_text.txt', 'w', encoding='utf8')
        name.write(encrypted_data)
    if key == key_20:
        name = open('key_20_text.txt', 'w', encoding='utf8')
        name.write(encrypted_data)


def find_i(txt, alphabet):
    c = Counter()
    I = 0
    for line in txt:
        c += Counter(line)  # рахуємо скільки разів зустрічається кожна літера в тексті
    for letter in alphabet:
        I = I + c[letter] * (c[letter] - 1)
    I = I / (len(txt) * (len(txt) - 1))
    return I


def to_separate_blocks(txt, period):  # розділити текст на блоки
    separated_txt = []
    for i in range(0, period):  # записуємо літери тексту у блок
        separated_txt.append(txt[i])
        i += 1
    for j in range(period, len(txt)):  # записуємо літери по їх відповідності до періоду
        separated_txt[j % period] += txt[j]
        j += 1
    return separated_txt


def blocks_index(txt, length):  # індекс відповідності блоків
    period = to_separate_blocks(txt, length)
    for i in range(0, len(period)):
        i += find_i(period[i], al)
    i /= len(period)
    return i


def total_index(arr):  # загальний індекс
    total = 0
    for element in arr:
        total += find_i(element, al)
    total /= len(arr)
    return total


def key_out(x, thesaurus):  # повернути ключ
    for key, value in thesaurus.items():
        if x == value:
            return key


def to_count_key_size(txt):  # рахуємо довжину ключа
    theoretical_i = 0.05751442686466821  # з частот першого комп. практикуму (0.05751442686466821)
    all_i = {}  # всі індекси
    for k in range(2, 32):  # індекси відповідності для всіх можливих довжин блоку  
        all_i[k] = total_index(to_separate_blocks(txt, k))
    all_keys = []
    for exp_i in all_i.values():  # обираємо індекси найбільш близькі до теоритичного
        if (exp_i > theoretical_i - 0.001) and (exp_i < theoretical_i + 0.001):  
            all_keys.append(exp_i)
    key_size = key_out(min(all_keys), all_i)
    all_i_data = pd.DataFrame(all_i, index=["index"])
    all_i_data.to_excel("indexes.xlsx")
    return key_size


def mode_letter(txt):  # найпопулярніша літера  
    frequency = Counter()
    for line in txt:
        frequency += Counter(line)
    mode_frequency = max(frequency.values())
    return key_out(mode_frequency, frequency)


def letters_frequency(txt):  # функція для підрахунку частоти букв
    c = Counter()
    frequency = {}
    for line in txt:
        c += Counter(line)  # рахуємо скільки разів зустрічається кожна літера в тексті
    for letter in alphabet_without_spaces:
        frequency[letter] = c[letter]/len(txt)
    return frequency


def to_reveal_key(periods):  # отримуєм ключ
    calculated_keys = []
    for i in range(len(periods)):
        period = []
        mode_cipher = thesaurus[mode_letter(periods[i])]  # найпопулярніша літера в шифротексті
        for j in mode_letters:
            mode_txt = thesaurus[j]
            sub = (mode_cipher - mode_txt) % 32  
            period.append(returned_thesaurus[sub])
        calculated_keys.append(period)
    return calculated_keys


def to_decrypt(txt, key):
    decipher = ''  # розшифрований текст
    first_letter = ord(al[0])  # отримуємо аскіі першої літери
    j = 0
    while j < len(txt):  # перебираємо кожну літеру тексту
        letter = txt[j]
        key_letter = key[j % len(key)]  # літера ключа
        decrypted_letter = (ord(letter) - first_letter - ord(key_letter) + first_letter) % len(al)  # розшифрована літера
        decipher += al[decrypted_letter]  # розшифрований текст
        j += 1
    decrypted_data = ''.join([letter for letter in decipher])
    name = open('decrypted_text.txt', 'w', encoding='utf8')
    name.write(decrypted_data)
    return decrypted_data


to_encrypt(clean, key_2)
to_encrypt(clean, key_3)
to_encrypt(clean, key_4)
to_encrypt(clean, key_5)
to_encrypt(clean, key_20)

print(find_i(clean, al))

with open("key_2_text.txt", encoding='utf8') as file1:
    key2 = file1.read()
print(find_i(key2, al))
with open("key_3_text.txt", encoding='utf8') as file1:
    key3 = file1.read()
print(find_i(key3, al))
with open("key_4_text.txt", encoding='utf8') as file1:
    key4 = file1.read()
print(find_i(key4, al))
with open("key_5_text.txt", encoding='utf8') as file1:
    key5 = file1.read()
print(find_i(key5, al))
with open("key_20_text.txt", encoding='utf8') as file1:
    key20 = file1.read()
print(find_i(key20, al))


size_of_key = to_count_key_size(file_to_decrypt)
exp = to_reveal_key(to_separate_blocks(file_to_decrypt, size_of_key))
print('Hacked key: ', end='')
for i in range(len(exp)):
    print(exp[i][0], end='')
print('\nReal key: экомаятникфуко')

print(to_decrypt(file_to_decrypt, 'экомаятникфуко'))
