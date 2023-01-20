import collections
import re
import itertools


def frequency(text):
    count = char_counter(text)
    count_frequency = {}
    all_chars = sum(count[letter] for letter in count)
    for char in count:
        count_frequency[char] = count_frequency.get(char, 0)
        count_frequency[char] = count[char] / all_chars
    return count_frequency


def block_compl(text):
    final_compblock_value = {}
    for key in range(2, 31):
        final_bs_value = 0
        for value in range(key):
            text_blocks = text[value::key]
            final_bs_value = final_bs_value + comp_ind_calculation(text_blocks)
        final_bs_value = final_bs_value / key
        final_compblock_value[key] = final_bs_value
    return final_compblock_value


def key(text):
    result_keys = []
    max_frequencies_charlist = chars_to_numbers("оеаинт")
    text_fragment = [text[j::14] for j in range(14)]
    result_keys.extend("".join([charlist[(charlist.index(collections.Counter(iter(block)).most_common(1)[0][0]) - max_frequencies_charlist[i]) % len(charlist)] for i in range(len(max_frequencies_charlist))]) for block in text_fragment)
    return result_keys


def vigenere(text, key):
    mod, numbers, key = len(charlist), chars_to_numbers(text), chars_to_numbers(key)
    encrypt_text = [(numbers[i] + key[i % len(key)]) % mod for i in range(len(numbers))]
    return numbers_to_chars(encrypt_text)


def decrypt(text, key):
    mod, numbers, key = len(charlist), chars_to_numbers(text), chars_to_numbers(key)
    dencrypt_text = [(numbers[i] - key[i % len(key)] + mod) % mod for i in range(len(numbers))]
    return numbers_to_chars(dencrypt_text)


def comp_ind_calculation(text):
    frequency = char_counter(text)
    compliance = sum(frequency[i] * (frequency[i] - 1) for i in frequency)
    compliance = compliance / (len(text) * (len(text) - 1))
    return compliance


def open_file(file):
    text = open(file, "r", encoding="utf-8").read()
    return re.sub(r'[1-9.,"\'-?:–!;a-z»A-Z„n{}#°—’’%` +\f\r\v\0^\ufeff@№&…*\\\n\t“«]', '', text).replace(" ", "").replace("ё", "е").replace("\n", "").lower()


def chars_to_numbers(text):
    mod = len(charlist)
    char_table = {i: charlist[i] for i in range(mod)}
    return [j for i, j in itertools.product(range(len(text)), range(len(char_table))) if text[i] == char_table[j]]


def numbers_to_chars(number):
    mod = len(charlist)
    char_table = {i: charlist[i] for i in range(mod)}
    return "".join(char_table[j] for i, j in itertools.product(range(len(number)), range(len(char_table))) if number[i] == j)


def char_counter(text):
    counter = {}
    for letter in text:
        counter[letter] = counter.get(letter, 0)
        counter[letter] += 1
    return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))


o_text = open_file("open_text.txt")
c_text = open_file("cipher_text.txt")
charlist = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
name = block_compl(c_text)
print(name)
print(comp_ind_calculation(o_text))

#ax = usrplot.subplots()
#usrplot.bar(name.keys(), name.values())
#ax.xaxis.set_major_locator(tick_usr.MultipleLocator(1))
#ax.xaxis.set_minor_locator(tick_usr.MultipleLocator(1))
#usrplot.title("Індекси відповідності для ключів")
# usrplot.show()

arr_k = key(c_text)
print(len(arr_k))
for j in range(len(arr_k[0])):
    word = [arr_k[i][j] for i in range(len(arr_k))]
    print(word)
a_iprint = []
for nchars in ['вы', 'кот', 'крот', 'танец', 'ортопедический']:
    with open(f"Key of {len(nchars)} chars lenght.txt", 'w', encoding="utf-8") as ph:
        a_iprint.append(comp_ind_calculation(vigenere(o_text, nchars)))
        ph.write(vigenere(o_text, nchars))
    ph.close()
#usrplot.bar(['вы', 'кот', 'крот', 'танец', 'ортопедический'], a)
#usrplot.title("Індекси відповідності для ключів")
# usrplot.show()
with open("decode_text.txt", 'w', encoding="utf-8") as ph:
    ph.write(decrypt(c_text, "чугунныенебеса"))
print(a_iprint)