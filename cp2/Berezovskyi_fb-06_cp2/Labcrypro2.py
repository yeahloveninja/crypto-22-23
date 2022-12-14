from itertools import cycle


with open('initial_text.txt', 'r', encoding='utf-8') as file1:
    initial_text = file1.read()
with open('ciphertext.txt', 'r', encoding='utf-8') as file2:
    ciphertext = file2.read()

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


def encode(text, key1):
    indexkey1 = []
    for i in key1:
        indexkey1.append(alphabet.index(i))
    ecode = lambda argument: alphabet[(alphabet.index(argument[0]) + alphabet.index(argument[1]) % 32) % 32]
    return ''.join(map(ecode, zip(text, cycle(key1))))


def decode(deCodedText, key):
    indexkey2 = []
    for i in key:
        indexkey2.append(alphabet.index(i))
    dcode = lambda argument: alphabet[(alphabet.index(argument[0]) - alphabet.index(argument[1]) % 32) % 32]
    return ''.join(map(dcode, zip(deCodedText, cycle(key))))


keyList = ['да', 'нет', 'прив', 'оысив', 'орпвитсьвэ', 'ннвпосшайфздомн', 'зцюрйонпхбяжткщсюсцъ']
data = {}

for key in keyList:
    encodeText = encode(initial_text, key)
    data[len(key)] = [key + ' : ' + ''.join(encodeText)]


# Шукаємо індекси відповідності
def compliance_index(text):
    index = 0
    length = len(text)
    for i in range(len(alphabet)):
        countLetter = text.count(alphabet[i])
        index += countLetter * (countLetter - 1)
    index *= 1 / (length * (length - 1))
    return index


# 1)для кожного кандидата зробити свій шифротекст
def firstTask(text):
    print("\n Індекс відповідності відкритого тексту = ", compliance_index(text), "\n")

    for key in keyList:
        print("Key length ", len(key))
        enccodedText = encode(text, key)
        print("Сipher text: ", enccodedText)
        print("Decoded text: ", decode(enccodedText, key))
        print("Індекс відповідності: ", compliance_index(enccodedText), "\n")
firstTask(initial_text)


# Розбиваємо текст на блоки
def split(text, length):
    block = []
    for i in range(length):
        block.append(text[i::length])
    return block


# 2)рахуємо індекси для кожного блоку
def indexblock(text, size):
    block = split(text, size)  # Власний індекс відповідності
    index = 0
    for i in range(len(block)):
        index = index + compliance_index(block[i])
    index = index / len(block)
    return index


def print_index_blocks():
    for i in range(1, len(alphabet)):
        print('Key length=' + str(i))
        print('Індекс відповідності=' + str(indexblock(ciphertext, i)))
print_index_blocks()


def findkey(text, size, letter):
    block = split(text, size)
    key = ""
    for i in range(len(block)):
        freq = max(block[i], key=lambda count_: block[i].count(count_))
        key += alphabet[(alphabet.index(freq) - alphabet.index(letter)) % len(alphabet)]
    return key


for letter in 'оеаитнслвр':
    print(findkey(ciphertext, 14, letter))
print("\n")
decodedText = decode(ciphertext, 'экомаятникфуко')
print("Сipher text: ", ciphertext)
print("Decoded text: ", decodedText)
