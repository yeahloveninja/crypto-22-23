from itertools import cycle

alpha = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

keys = ['вам', 'топор', 'программа', 'пакетирование', 'деревообрабатывающий']


def vigenere(target_text: str, code: str, type_operation: bool) -> str:
    # True - encode
    # False - decode
    result_text = ''
    if type_operation:
        for symbol, symbol_key in zip(target_text, cycle(code)):
            result_text += alpha[(alpha.index(symbol) + alpha.index(symbol_key) % 32) % 32]
    else:
        for symbol, symbol_key in zip(target_text, cycle(code)):
            result_text += alpha[(alpha.index(symbol) - alpha.index(symbol_key) % 32) % 32]
    return result_text


def coincidence_index(target_text):
    length = len(target_text)
    index = 0
    for i in range(len(alpha)):
        count_letter = target_text.count(alpha[i])
        index += count_letter * (count_letter - 1)
    index *= 1 / (length * (length - 1))
    return index


data = {}

with open('final_text.txt', 'r') as file1:
    our_text = file1.read()


for key in keys:
    encodeText = vigenere(our_text, key, True)
    data[len(key)] = [key + ' : ' + ''.join(encodeText)]


print("\nCoincidence index start = ", coincidence_index(our_text), "\n")

for key in keys:
    print("Key length = ", len(key))
    final_text = vigenere(our_text, key, True)
    print("Encoded text: ", final_text)
    print("Decoded text: ", vigenere(final_text, key, False))
    print("Coincidence index: ", coincidence_index(final_text), "\n")
