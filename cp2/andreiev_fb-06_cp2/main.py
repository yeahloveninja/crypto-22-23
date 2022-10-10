import csv
import re


alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
alphabet_with_nums = {i: num for num, i in enumerate(alphabet)}
reverse_alphabet_with_nums = {num: i for num, i in enumerate(alphabet)}


#модифікація фільтрації тексту з попереднього практикуму
def filter_text(text):
    text = re.sub(r'[^а-яА-Я ]', '', text).lower().replace(" ", "").replace("ё", "е")
    return text

with open("text.txt", 'r') as f:
    text = f.read()


text = filter_text(text)

def vigenere_encrypt(open_text, key):
    res = ''
    for i in range(len(open_text)):
        open_char = open_text[i]
        key_char = key[i % len(key)]

        open_num = alphabet_with_nums[open_char]
        key_num = alphabet_with_nums[key_char]

        encrypted_char = reverse_alphabet_with_nums[(open_num + key_num) % len(alphabet)]
        res += encrypted_char
    return res


keys = ['ро', 'кси', 'бета', 'сигма', 'танецклинковмеркурия']

r2 = vigenere_encrypt(text, keys[0])
r3 = vigenere_encrypt(text, keys[1])
r4 = vigenere_encrypt(text, keys[2])
r5 = vigenere_encrypt(text, keys[3])
r20 = vigenere_encrypt(text, keys[4])


def calc_index(text):
    result = 0
    for i in alphabet:
        counted = text.count(i)
        result += counted * (counted - 1)

    result = result / (len(text) * (len(text) - 1))
    return round(result, 5)

with open("given_ct_var_5.txt", 'r') as f:
    given_ct = f.read()

given_ct = filter_text(given_ct).replace('\n', "")


def spot_key_length(text):
    indexes = {}
    for key_length in range(2, len(alphabet)):
        total = 0
        for group in range(key_length):
            block = text[group::key_length]
            total += calc_index(block)
        total = total / key_length
        indexes[key_length] = total
    return indexes

indexes = spot_key_length(given_ct)

blocks = []
for block in range(16):
    blocks.append(given_ct[block::16])

max_frequencies = []
key = ''
for block in blocks:
    frequencies = {}
    for letter in set(block):
        frequencies[letter] = block.count(letter) / len(block)
    max_frequencies.append(max(frequencies, key=frequencies.get))

for letter in max_frequencies:
    key += alphabet[(alphabet.index(letter) - 14) % len(alphabet)]
print(key)

def vigenere_decrypt(ciphertext, key):
    res = ''
    for i in range(len(ciphertext)):
        cipher_char = ciphertext[i]
        key_char = key[i % len(key)]
        cipher_num = alphabet_with_nums[cipher_char]
        key_num = alphabet_with_nums[key_char]

        open_char = reverse_alphabet_with_nums[(cipher_num - key_num) % len(alphabet)]
        res += open_char
    return res

decrypted = vigenere_decrypt(given_ct, 'делолисоборотней')



