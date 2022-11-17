import pandas as pd
import warnings
import xlsxwriter

warnings.simplefilter(action='ignore', category=FutureWarning)


alphabet_1, alphabet_2 = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"), list("абвгдежзийклмнопрстуфхцчшщъыьэюя")
encrypted_text = ''

text = open('thetext.txt', encoding='utf-8', mode='r').read()
keys = open('keys.txt', encoding='utf-8', mode='r').read().split(' ')
key = keys[0]
len_text = len(text)



def convert_to_index(text, alphabet):
    index_list = []
    for i in range(len(text)):
        index_list.append(alphabet.index(text[i]))
    return index_list


def convert_to_letter(indexs, alphabet):
    letter_list = []
    for i in range(len(indexs)):
        letter_list.append(alphabet[indexs[i]])
    return letter_list


def encode(conv_txt, conv_key, alphabet):
    encoded_txt = []
    for i in range(len(conv_txt)):
        encoded_index = (conv_txt[i] + conv_key[i % len(conv_key)]) % len(alphabet)
        encoded_txt.append(encoded_index)
    return encoded_txt


def decode(conv_txt, conv_key, alphabet):
    decoded_txt = []
    for i in range(len(conv_txt)):
        decoded_index = (conv_txt[i] - conv_key[i % len(conv_key)]) % len(alphabet)
        decoded_txt.append(decoded_index)
    return decoded_txt


def get_blocks(r, text):
    blocks = []
    for j in range(r):
        a = []
        for i in range(0, len(text), r):
            i += j
            if i < len(text):
                a.append(text[i])
        blocks.append(a)
    return blocks


def calculate_index(text):
    n, total, frequency_list = len(text), 0, {}
    for i in text: frequency_list[i] = 1 if i not in frequency_list else frequency_list[i] + 1
    # ↑ записываем количества повторов букв
    frequency_list = sorted(frequency_list.items(), key=lambda item: item[1], reverse=True)
    for t in range(len(frequency_list)):  # длина словаря  # считаем индекс соответствия
        chance = frequency_list[t][1]
        total += chance * (chance - 1)
    return (1 / (n * (n - 1))) * total


converted_text = convert_to_index(text, alphabet_1)
converted_keys, encoded_text = [], []
for i in range(len(keys)):  # convert all keys to index
    converted_keys.append(convert_to_index(keys[i], alphabet_1))
for i in range(len(keys)):  # joining all the results into one piece and save
    encoded_text.append(convert_to_letter(encode(converted_text, converted_keys[i], alphabet_1), alphabet_1))

# --------------------task 1-------------------------------------------------------------------

for i in range(len(encoded_text)):
    a = 'w' if i == 0 else 'a'
    f, data_ = open("encrypted_text.txt", a), encoded_text[i]
    for line in list(''.join(data_) + '\n'): f.write(line)
    f.close()


# --------------------task 2-------------------------------------------------------------------
index_values = [('key_length', 'index'), ('PlainText', calculate_index(text))]
for key in keys:  # для каждого ключа
    blocks, blocks_sum = get_blocks(1, encoded_text[keys.index(key)]), 0
    index_values.append((len(key), calculate_index(blocks[0])))

# --------------------task 3-------------------------------------------------------------------

text_to_decrypt = open('task3.txt', encoding='utf-8', mode='r').read().lower().replace("\n", '')
conv_txt = convert_to_index(text_to_decrypt, alphabet_2)
index_values_2 = [('key_length', 'index')]
for r in range(1, 31):
    blocks, blocks_sum = get_blocks(r, text_to_decrypt), 0
    for i in range(len(blocks)): blocks_sum += calculate_index(blocks[i])  # для усереднення
    index_values_2.append((r, blocks_sum / len(blocks)))


def return_approximate_key(text, key_len, alphabet):
    lst, divided_text, right, output_list = list(text), [], key_len, {}
    for i in range(len(lst) // key_len + 1):  # dividing text into fragments with key_len
        temp, left = [], i*key_len
        for j in range(left, right):
            if j <= len(lst) - 1: temp.append(lst[j])
        right += key_len
        divided_text.append(temp)
    for i in range(len(alphabet)):  # generate alphabet list
        output_list[alphabet[i]] = [0]*key_len
    for i in range(len(divided_text)):  # result is output_list
        for j in range(key_len):
            if j < len(divided_text[i]): output_list[divided_text[i][j]][j] += 1
    abc, lstx = [], []
    for i in range(key_len):  # извлекаем столбики
        u = []
        for j in range(len(alphabet)): u.append(output_list[alphabet[j]][i])
        abc.append(u)
        lstx.append((abc[i].index(max(abc[i]))-14)%len(alphabet))  # точка "о" - опорна точка, тому віднімаємо 14
    return print(''.join(convert_to_letter(lstx, alphabet)))

return_approximate_key(text_to_decrypt, int(input('Enter key length: ')), alphabet_2)

# ----- запись в таблицу --------
df1 = pd.DataFrame(index_values)
df2 = pd.DataFrame(index_values_2)
writer = pd.ExcelWriter("index.xlsx", engine="xlsxwriter")
df1.to_excel(writer, startrow=-1, startcol=-1, sheet_name = 'Task_2')
worksheet = writer.sheets['Task_2']
df2.to_excel(writer, startrow=-1, startcol=-1, sheet_name = 'Task_3')
worksheet = writer.sheets['Task_3']
writer.save()
