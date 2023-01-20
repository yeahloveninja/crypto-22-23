from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns


alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
keys = ["ля", "топ", "круг", "кринж", "пармеджано", "воздухоохладительный"]


with open('C:\\Users\\katri\\Desktop\\KPI\\Crypto\\lab2\\lab2.txt', 'r', encoding='utf-8') as file1:
    some_text = file1.read()                          # файл з текстом
with open('C:\\Users\\katri\\Desktop\\KPI\\Crypto\\lab2\\var10.txt', 'r', encoding='utf-8') as file2:
    cipher = file2.read()                     # ШТ варіант 10


def dec_enc_vigenere(text, key_word, enc_or_dec):     # encrypt/decrypt
    text_indexes = []
    key_word_indexes = []
    for letter in text:
        if letter in alphabet:
            text_indexes.append(alphabet.index(letter))
    for letter in key_word:
        if letter in alphabet:
            key_word_indexes.append(alphabet.index(letter))
    len_str_text = len(text_indexes)
    length_indexes = len(key_word_indexes)
    if len_str_text % length_indexes == 0:
        key_word_indexes = key_word_indexes * (len_str_text // length_indexes)
    else:
        key_indexes = key_word_indexes * (len_str_text // length_indexes)
        diff_len = len_str_text - len(key_indexes)
        key_word_indexes = key_indexes + key_indexes[0:diff_len]
    if enc_or_dec == "encrypt":
        sum_indexes = [a + b for a, b in zip(text_indexes, key_word_indexes)]
    else:
        sum_indexes = [a - b for a, b in zip(text_indexes, key_word_indexes)]
    for index in range(len(sum_indexes)):
        sum_indexes[index] = sum_indexes[index] % 32
    result_text = ""
    for index in sum_indexes:
        result_text += alphabet[index]
    return result_text


def blocks_of_text(txt, r):
    blocks = []
    for i in range(r):
        blocks.append(txt[i::r])
    return blocks


def conform_index(txt):
    frequency = Counter(txt)
    conf_index = 0
    for freq in frequency:
        conf_index += frequency[freq] * (frequency[freq] - 1)
    conf_index /= ((len(txt) - 1)*len(txt))
    return conf_index


def length(text):
    indexes = []
    for r in range(2, 31):
        index = 0
        blocks = blocks_of_text(text, r)
        for i in range(r):
            index += conform_index(blocks[i])
        index /= r
        indexes.append(index)
    return indexes, indexes.index(max(indexes)) + 2


def letters_top(text):
    frequency = Counter(text)
    max_freq = max(Counter(text).values())
    for k, v in frequency.items():
        if v == max_freq:
            return k


def find_key(blocks):
    expected_keys = []
    text_top_letters = ["о", "е", "а"]
    for i in range(len(blocks)):
        for_block = []
        cipher_top_number = alphabet.index(letters_top(blocks[i]))
        for j in text_top_letters:
            text_top_number = alphabet.index(j)
            move = (cipher_top_number - text_top_number) % 32
            for_block.append(alphabet[move])
        expected_keys.append(for_block)
    return expected_keys
#1
files = ["key2.txt", "key3.txt", "key4.txt", "key5.txt", "key10.txt", "key20.txt"]
for i in range(len(keys)):
    data = dec_enc_vigenere(some_text, keys[i], "encrypt")
    with open("C:\\Users\\katri\\Desktop\\KPI\\Crypto\\lab2\\"+files[i],
    'w', encoding="utf-8") as file:
        file.write(data)

# 2
for i in range(len(files)):
    with open("C:\\Users\\katri\\Desktop\\KPI\\Crypto\\lab2\\"+files[i],
              'r', encoding="utf-8") as file:
        txt_file = file.read()
    print("Індекс для шифр тексту"+str(i+1)+": " + str(conform_index(txt_file)))
print("Індекс відкритого тексту: " + str(conform_index(some_text)))
data_x = [0.05664286889320178,	0.040480824102661656,	0.04449478617254916,	0.03684642033510209,
        0.03740422914857003,	0.034044960809275056,	0.032670392191031336]
data_y = ['ВТ', 'key_2', 'key_3', 'key_4', 'key_5', 'key_10', 'key_20']
plt.figure(figsize=(10, 6))
plt.yticks([i for i in range(2,31)])
plt.xticks(rotation=25)
sns.set_style("dark")


plt.title("Part 2")


sns.barplot(x=data_x, y=data_y)


plt.xlabel("Значення індексу відповідності")
plt.ylabel("Тексти зашифровані різними ключами")
plt.show()

# 3
length_key = length(cipher)
print(f'Довжина ключа: {length_key}')

data_x = length_key[0]
data_y = [str(i) for i in range(2, 31)]
plt.figure(figsize=(10, 6))
plt.yticks([i for i in range(2,31)])
plt.xticks(rotation=25)
sns.set_style("dark")


plt.title("Part 3")


sns.barplot(x=data_x, y=data_y)


plt.xlabel("Значення індексу відповідності")
plt.ylabel("r - довжина ключа")
plt.show()
text_blocks = blocks_of_text(cipher, 15)
key_word = find_key(text_blocks)
print('Ключ: ', end='')
for i in range(len(key_word)):
    print(key_word[i][0], end='')
print("")
decrypted_text = dec_enc_vigenere(cipher, "крадущийсявтени", "decrypt")
print(decrypted_text)
with open('C:\\Users\\katri\\Desktop\\KPI\\Crypto\\lab2\\' + 'decrypted_text.txt', 'w', encoding='utf-8') as f:
    f.write(decrypted_text)
