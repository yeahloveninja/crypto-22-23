import re
from collections import Counter

with open("text.txt", encoding='utf8') as file:
    text = file.read()

alphabet_without_spaces = 'абвгдеэжзиыйклмнопрстуфхцчшщъьюя'
splited = re.compile('[^а-яА-Я ]').sub('', text).rstrip('.,').lower().split(' ')
clean = ''.join(splited)
clean_text = open('clean_text.txt', 'w')
clean_text.write(clean)
al = []
for i in alphabet_without_spaces:
    al.append(i)

key_2 = 'он'
key_3 = 'нет'
key_4 = 'кино'
key_5 = 'земля'
key_20 = 'методполиалфавитного'


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
        name = open('key_2_text.txt', 'w')
        name.write(encrypted_data)
    if key == key_3:
        name = open('key_3_text.txt', 'w')
        name.write(encrypted_data)
    if key == key_4:
        name = open('key_4_text.txt', 'w')
        name.write(encrypted_data)
    if key == key_5:
        name = open('key_5_text.txt', 'w')
        name.write(encrypted_data)
    if key == key_20:
        name = open('key_20_text.txt', 'w')
        name.write(encrypted_data)


def find_i(txt):
    c = Counter()
    i = 0
    for line in txt:
        c += Counter(line)  # рахуємо скільки разів зустрічається кожна літера в тексті
    for letter in al:
        i = i + c[letter] * (c[letter] - 1)
    i = i / (len(txt) * (len(txt) - 1))
    print(i)


to_encrypt(clean, key_2)
to_encrypt(clean, key_3)
to_encrypt(clean, key_4)
to_encrypt(clean, key_5)
to_encrypt(clean, key_20)

find_i(clean)

with open("key_2_text.txt") as file1:
    key2 = file1.read()
find_i(key2)
with open("key_3_text.txt") as file1:
    key3 = file1.read()
find_i(key3)
with open("key_4_text.txt") as file1:
    key4 = file1.read()
find_i(key4)
with open("key_5_text.txt") as file1:
    key5 = file1.read()
find_i(key5)
with open("key_20_text.txt") as file1:
    key20 = file1.read()
find_i(key20)





