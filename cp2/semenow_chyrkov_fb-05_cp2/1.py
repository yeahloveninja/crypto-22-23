import re
import itertools
from collections import Counter

txt = open('dirty_text_task1.txt', 'r', encoding='utf=8').read()


def create_txt(text):
    text_one = text.lower().replace(' ', '_').replace('\n', '_').strip()
    text_write = ''
    for i in text_one:
        if i == 'ё' or i == 'Ё':
            pass
        if i.isalpha():
            text_write += i
        elif i == '_':
            text_write += ''
    text_write = re.sub(r'_+', '', text_write)
    with open("clear_text_task1.txt", 'w') as file:
        file.write(text_write)
    return text_write
# create_txt(txt)


alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
num_of_letters = 32
keys = ['ад', 'ирп', 'граф', 'сабля', 'абсолютный', 'раскомплектовываться']


def sifr_viginere(text, key, operation: str):
    answer = ''
    if operation == 'decode':
        for text_elelement, key_element in zip(text, itertools.cycle(key)):
            answer += alphabet[(alphabet.index(text_elelement) - alphabet.index(key_element) % num_of_letters) % num_of_letters]
    if operation == 'encode':
        for text_elelement, key_element in zip(text, itertools.cycle(key)):
            answer += alphabet[(alphabet.index(text_elelement) + alphabet.index(key_element) % num_of_letters) % num_of_letters]
    return answer


def coincidence(text):
    length = len(text)
    index = 0
    i = 0
    while i < num_of_letters:
        letters = text.count(alphabet[i])
        index += (letters - 1) * letters
        i += 1
    index *= 1/((length-1) * length)

    return index


def find_blocks(text, letters):
    blocks = []
    for k in range(letters):
        blocks.append(text[k::letters])
    return blocks


def blocks_indexes(text):
    for letters in range(2, num_of_letters):
        index = 0
        for group in range(letters):
            block = text[group::letters]
            index += coincidence(block)
        index = index / letters
        if index > 0.05:
            print(f'{letters} --- {index}')


def maybe_key(text, len_of_key, letter):
    blocks = find_blocks(text, len_of_key)
    key = ''
    for element in blocks:
        count = Counter(element).most_common(1)[0]
        key += alphabet[(alphabet.index(count[0]) - alphabet.index(letter)) % num_of_letters]
    return key


print('TASK 1-2')
print(f'Відкритий текст')
clear_txt = open('clear_text_task1.txt', 'r').read()
print(clear_txt)
print(f'Індекс відповідності: {coincidence(clear_txt)}')

for k in keys:
    print('\n-----------------')
    print(f'Зашифрований текст ключем з {len(k)} символів. Ключ: {k}')
    sifr_txt = sifr_viginere(clear_txt, k, "encode")
    print(f'{sifr_txt}')
    print(f'Індекс відповідності: {coincidence(sifr_txt)}')


print('\n-----------------')
print('TASK 3')
txt_var = open('text_var10.txt', 'r', encoding='utf=8').read()
blocks_indexes(txt_var)
print(maybe_key(txt_var, 15, 'о'))
print(sifr_viginere(txt_var, 'крадущийсявтени', 'decode'))
