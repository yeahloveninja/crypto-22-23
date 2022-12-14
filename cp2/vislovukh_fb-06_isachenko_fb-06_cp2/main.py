import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import Counter

fig, ax = plt.subplots()
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
sort_rules = r'[1-9.,"\'-?:–!;a-z»A-Z„n{}#°—’’%` +\f\r\v\0^\ufeff@№&…*\\\n\t“«]'
#          r2     r3     r4       r5          r13
r_keys = ['от', 'рот', 'шире', 'бомба', 'макромолекула']


def open_file(file):
    text = open(file, "r", encoding="utf-8").read()
    return re.sub(sort_rules, '', text).replace(" ", "").replace("ё", "е").replace("\n", "").lower()


o_text = open_file("open_text.txt")
c_text = open_file("cipher_text.txt")


def chars_to_numbers(text):
    char_table = {}
    mod = len(alphabet)
    for i in range(0, mod):
        char_table[i] = alphabet[i]
    text_char_number = []
    for i in range(0, len(text)):
        for j in range(0, len(char_table)):
            if text[i] == char_table[j]:
                text_char_number.append(j)
    return text_char_number


def numbers_to_chars(number):
    char_table = {}
    mod = len(alphabet)
    for i in range(0, mod):
        char_table[i] = alphabet[i]
    cipher_text = ""
    for i in range(0, len(number)):
        for j in range(0, len(char_table)):
            if number[i] == j:
                cipher_text += char_table[j]
    return cipher_text


def char_counter(text):
    counter = {}
    for letter in text:
        counter.setdefault(letter, 0)
        counter[letter] += 1
    res = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))
    return res


def char_frequency(text):
    char_count = char_counter(text)
    all_chars = 0
    count_frequency = {}
    for letter in char_count:
        all_chars += char_count[letter]
    for char in char_count:
        count_frequency.setdefault(char, 0)
        count_frequency[char] = char_count[char] / all_chars
    return count_frequency


def vigenere(text, key):
    mod = len(alphabet)
    numbers = chars_to_numbers(text)
    key = chars_to_numbers(key)
    encrypt_text = []
    for i in range(0, len(numbers)):
        encrypt_text.append(((numbers[i] + key[i % len(key)]) % mod))
    return numbers_to_chars(encrypt_text)


def compliance_index(text):
    compliance = 0
    frequency = char_counter(text)
    for i in frequency:
        compliance += frequency[i] * (frequency[i] - 1)
    compliance = compliance / (len(text) * (len(text) - 1))
    return compliance


def get_block_compliance(text):
    compliance_block = {}
    for key in range(2, 31):
        result_blocks = 0
        for j in range(key):
            text_blocks = text[j::key]
            result_blocks += compliance_index(text_blocks)
        result_blocks = result_blocks / key
        compliance_block[key] = result_blocks
    return compliance_block


def find_key(text):
    text_fragment, result_keys, max_frequencies_alphabet = [text[j::17] for j in range(17)], [], chars_to_numbers(
        "оеаинт")
    for block in text_fragment:
        result_keys.append("".join([alphabet[
                                        (alphabet.index(Counter(line for line in block).most_common(1)[0][0]) -
                                         max_frequencies_alphabet[i]) % len(alphabet)] for i in
                                    range(len(max_frequencies_alphabet))]))
    return result_keys


def vigenere_decrypt(text, key):
    mod = len(alphabet)
    numbers = chars_to_numbers(text)
    key = chars_to_numbers(key)
    dencrypt_text = []
    for i in range(0, len(numbers)):
        dencrypt_text.append(((numbers[i] - key[i % len(key)] + mod) % mod))
    return numbers_to_chars(dencrypt_text)


name = get_block_compliance(c_text)

plt.bar(name.keys(), name.values())
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
plt.title("Індекси відповідності для ключів")
# plt.show()

arr_keys = find_key(c_text)
print(arr_keys)
for j in range(len(arr_keys[0])):
    word = []
    for i in range(len(arr_keys)):
        word.append(arr_keys[i][j])
    print(word)
i_for_r2_and_other = []
for i in r_keys:
    with open(f"lab_file/Ключ довжиною {len(i)}.txt", 'w', encoding="utf-8") as file:
        some_text = vigenere(o_text, i)
        i_for_r2_and_other.append(compliance_index(some_text))
        file.write(some_text)
        file.close()
plt.bar(r_keys, i_for_r2_and_other)
plt.title("Індекси відповідності для ключів")
# plt.show()
with open(f"lab_file/decode_text.txt", 'w', encoding="utf-8") as file:
    file.write(vigenere_decrypt(c_text, "войнамагаэндшпиль"))
