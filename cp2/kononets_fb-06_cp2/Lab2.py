alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
path = 'D:\\Python\\PycharmProjects\\crypto-22-23\\cp2\\kononets_fb-06_cp2\\Crypto\\text.txt'
dict_letters = dict(zip(alphabet, [i for i in range(32)]))
revers_dict_letters = dict(zip([i for i in range(32)], alphabet))


with open(path, 'r', encoding='utf-8') as f:
    my_text = f.read()


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
