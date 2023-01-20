import re

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
file = open('text.txt', encoding='utf-8')
text = file.read()
file3 = open('3task.txt', encoding='utf-8').read()
keys = open('keys.txt', encoding='utf-8', mode='r').read().split(' ')


def fil_text(text):
    txt = re.sub(r'[^а-яА-Я ]', '', text)
    space = txt.lower().replace('  ', ' ').replace('   ', ' ')
    return space


task3 = fil_text(file3)
thirdTask = task3.replace(' ', '')
var6task3 = open('3taskvar6.txt', 'w', encoding='utf-8')
var6task3.write(thirdTask)
var6task3.close()

textWithSpace = fil_text(text)
textWithoutSpace = textWithSpace.replace(' ', '')

file_No_Space = open('filtText.txt', 'w', encoding='utf-8')
file_No_Space.write(textWithoutSpace)
file_No_Space.close()


def encrypt(textWithoutSpace):
    encrypted_texts = {i: ''.join([alphabet[(alphabet.find(textWithoutSpace[j]) + (alphabet.find(i[j % len(i)]))) % 32] for j in range(len(textWithoutSpace))]) for i in keys}
    return encrypted_texts


def decrypt(thirdTask):
    key = "возвращениеджинна"
    result = ''.join([alphabet[(alphabet.find(thirdTask[i]) - (alphabet.find(key[i % len(key)]))) % 32] for i in range(len(thirdTask))])
    return result


def index(thirdTask):
    res = sum([thirdTask.count(i) * (thirdTask.count(i) - 1) for i in alphabet]) / (len(thirdTask) * (len(thirdTask) - 1))
    return res


def keyLength(thirdTask):
    ind = {lengthKey: sum([index(thirdTask[group::lengthKey]) for group in range(lengthKey)])/lengthKey for lengthKey in range(2, len(alphabet))}
    return ind


def blocks(thirdTask):
    blocks = [thirdTask[block::17] for block in range(17)]
    return blocks


def frequencies(thirdTask):
    frequencies = [max({letter: block.count(letter) / len(block) for letter in set(block)}, key={letter: block.count(letter) / len(block) for letter in set(block)}.get) for block in blocks(thirdTask)]
    return frequencies


def findKey(thirdTask):
    key = ''.join([alphabet[(alphabet.index(letter) - 14) % len(alphabet)] for letter in frequencies(thirdTask)])
    return key


def main():
    encryptedtext = encrypt(textWithoutSpace)
    print('Зашифрований текст:\n', encryptedtext)
    print('Індекси:\n', keyLength(thirdTask))
    print('Ключ:\n', findKey(thirdTask))
    print('Розшифрований текст:\n', decrypt(thirdTask))


main()


