import random
from itertools import cycle

with open('text1.txt', 'r', encoding='utf-8') as file1:
    text1 = file1.read()
with open('text2.txt', 'r', encoding='utf-8') as file2:
    text2 = file2.read()


ABC = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


# функція кодування
def encode(ourText, key):

    indexKey = []
    for i in key:
        indexKey.append(ABC.index(i))

    # Закодовуємо додаванням
    result = lambda argument: ABC[(ABC.index(argument[0]) + ABC.index(argument[1]) % 32) % 32]
    return ''.join(map(result, zip(ourText, cycle(key))))


# функція декодування
def decode(deCodedText, key):

    indexKey = []
    for i in key:
        indexKey.append(ABC.index(i))

    # Розкодовуємо відніманням
    result = lambda argument: ABC[(ABC.index(argument[0]) - ABC.index(argument[1]) % 32) % 32]
    return ''.join(map(result, zip(deCodedText, cycle(key))))


keyList = ['фщ', 'бсв', 'юхшм', 'осмвг', 'йикъбмуящш', 'хюхзгррахеш', 'саэсдпейдзтф', 'вдзхьзужбъгяш', 'квххсьпириуктж', 'ннвпосшайфздомн', 'жшпеиезэщфчбщнзй', 'здукящуаубцыхыгхж', 'юпйсимяяшяшзломмзш', 'щыййгскфвэслнуьрсхщ', 'зцюрйонпхбяжткщсюсцъ']
data = {}

for key in keyList:
    encodeText = encode(text1, key)
    data[len(key)] = [key + ' : ' + ''.join(encodeText)]


# Шукаємо індекси відповідності
def coincidenceIndex(ourText):

    index = 0
    length = len(ourText)
    for i in range(len(ABC)):
        countLetter = ourText.count(ABC[i])
        index += countLetter * (countLetter - 1)
    index *= 1/(length*(length-1))

    return index


# функція для першого завдання
def firstTask(ourText):

    print("\nCoincidence index start = ", coincidenceIndex(ourText), "\n")

    for key in keyList:
        print("Key length = ", len(key))
        enccodedText = encode(ourText, key)
        print("--- Encoded text: ", enccodedText)
        print("--- Decoded text: ", decode(enccodedText, key))
        print("Coincidence index: ", coincidenceIndex(enccodedText), "\n")

firstTask(text1)


# Розбиваємо текст на блоки
def splitBlocks(ourText, length):

    ourBlock = []

    for i in range(length):
        ourBlock.append(ourText[i::length])

    return ourBlock


# Рахуємо індекси для кожного блоку
def eachIndexBlock(ourText, size):

    ourBlock = splitBlocks(ourText, size)  # Власний індекс відповідності
    index = 0

    for i in range(len(ourBlock)):
        index = index + coincidenceIndex(ourBlock[i])
    index = index/len(ourBlock)

    return index


# Функція для виведення індексів відповідності
def printBlocksIndex():

    for i in range(1, len(ABC)):   # для ключів різних довжин
        print('Key length=' + str(i) + ' => ioc=' + str(eachIndexBlock(text2, i)))

# Викликаємо функцію для індексів відповідності для блоків різної довжини шифрованого тексту
printBlocksIndex()


# функція для знаходження ключа
def creationKey(ourText, size, letter):

    ourBlock = splitBlocks(ourText, size)
    key = ""  # k - це літера, яка э серед найчастыших
    for i in range(len(ourBlock)):
        frequent = max(ourBlock[i], key=lambda count_: ourBlock[i].count(count_))  # Найчастіший
        key += ABC[(ABC.index(frequent) - ABC.index(letter)) % len(ABC)]

    return key


for letter in 'оеаитнслвр':
    print(creationKey(text2, 14, letter))  # ключ має довжину 14 або 28
print("\n")

decodedText = decode(text2, 'экомаятникфуко')  # трішки підкоригувавши отриманий ключ, розшифрували текст

print("--- Encoded text: ", text2)
print("--- Decoded text: ", decodedText)
