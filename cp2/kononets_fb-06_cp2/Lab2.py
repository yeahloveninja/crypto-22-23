from collections import Counter
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
path = 'D:\\Python\\PycharmProjects\\crypto-22-23\\cp2\\kononets_fb-06_cp2\\Crypto\\'
dict_letters = dict(zip(alphabet, [i for i in range(32)]))
revers_dict_letters = dict(zip([i for i in range(32)], alphabet))
keys = ["ты", "сок", "ромб", "песик", "тарабанить", "антропотолерантность"]
files = ["text_key1.txt", "text_key2.txt", "text_key3.txt", "text_key4.txt", "text_key5.txt", "text_key6.txt"]

with open(path+"text.txt", 'r', encoding='utf-8') as f:
    my_text = f.read()                          # файл з моїм текстом
with open(path+"cipher_text.txt", 'r', encoding='utf-8') as f1:
    cipher_text = f1.read()                     # ШТ варіант 7


def vigenere(str_word, str_key, operation):     # шифрування/дешифрування шифру Віженера (слово/ключ/операція)
    array_indexes = []
    key_indexes = []
    for i in str_word:      # шукаю індекси літер тексту
        if i in dict_letters.keys():
            array_indexes.append(dict_letters[i])
    for i in str_key:       # шукаю індекси літер ключа
        if i in dict_letters.keys():
            key_indexes.append(dict_letters[i])
    length_word = len(array_indexes)
    length_key = len(key_indexes)
    k = 0
    while length_key < length_word:     # для того щоб повторювати ключ до довжини тексту
        key_indexes.append(key_indexes[k])
        if k % length_key == k:         # так як довжина ключа фіксована, то повторюємо кожен раз коли ключ закінчується
            k += 1
        length_key += 1               # збільшую довжину ключа коли він повторюється
    if operation == "enc":            # шифрування
        sum1 = [x + y for x, y in zip(array_indexes, key_indexes)]  # дадаємо індекси
    else:                             # дешифрування
        sum1 = [x - y for x, y in zip(array_indexes, key_indexes)]  # індекси шт відняти індекси ключа
    for i in range(len(sum1)):
        sum1[i] = sum1[i] % 32  # за модулем 32, бо 32 літери алфавіту
    text = ""
    for i in sum1:          # формую шифрований/дешифрований текст
        if i in revers_dict_letters.keys():
            text += revers_dict_letters[i]  # щоб не робити циклу у циклі взяв реверс-словник літер
    return text


def theoretical_i_of_conformity(text):      # індекс відповідності
    index = 0
    frequency = Counter(text)
    for i in frequency:
        index += frequency[i] * (frequency[i] - 1)      # сума: частота букви * частота букви - 1
    index /= (len(text) * (len(text) - 1))              # відповідно ділимо на знаменник суму
    return index


def math_expectation(text):                 # математичне очікування
    expectation = 0
    frequency = Counter(text)
    for i in frequency:
        frequency[i] /= len(text)
        expectation += pow(frequency[i], 2)   # частота літери у тексті в степені 2
    return expectation


def text_into_blocks(text, r):               # ділимо текст на блоки Y1, Y2... Y(r) де r - довжина ключа
    text_blocks = []
    for i in range(r):
        text_blocks.append(text[i::r])
    return text_blocks


def len_key(text, expectation):              # пошук довжини ключа шляхом розбиття ШТ на блоки
    r_i = []         # сюди додаю індекс відповідності  для кожного ключа
    array_differences = []   # різниця між індексом відповідності та його теор. математичним очікуванням
    for r in range(2, 31):   # на проміжку від 2 до 30 включно за умовою
        index = 0
        blocks = text_into_blocks(text, r)
        for i in range(r):
            index += theoretical_i_of_conformity(blocks[i])
        index /= r
        r_i.append(index)
    for i in range(len(r_i)):
        difference = abs(r_i[i] - expectation)
        array_differences.append(difference)
    print(r_i)
    return array_differences.index(min(array_differences)) + 2   # додаю два бо починав рахувати індекси з довжини r = 2


# PART 1 ---------------------------------------------------------------------------------
# for i in range(len(keys)):
#     new_data = vigenere(my_text, keys[i], "enc")
#     with open("D:\\Python\\PycharmProjects\\crypto-22-23\\cp2\\kononets_fb-06_cp2\\Crypto\\"+files[i],
#     'w', encoding="utf-8") as f:
#         f.write(new_data)
#PART 2 -----------------------------------------------------------------------------------
for i in range(len(files)):
    with open("D:\\Python\\PycharmProjects\\crypto-22-23\\cp2\\kononets_fb-06_cp2\\Crypto\\"+files[i],
              'r', encoding="utf-8") as f:
        text_txt = f.read()
    print("Index for my encrypted text"+str(i+1)+": " + str(theoretical_i_of_conformity(text_txt)))
print("Index for my text: " + str(theoretical_i_of_conformity(my_text)))
# Index for my encrypted text1: 0.04508227392477867
# Index for my encrypted text2: 0.04172939542958518
# Index for my encrypted text3: 0.03722774007403989
# Index for my encrypted text4: 0.03465818759936407
# Index for my encrypted text5: 0.03670957484999231
# Index for my encrypted text6: 0.036412503585179105
# Index for my text: 0.05621256930554843
