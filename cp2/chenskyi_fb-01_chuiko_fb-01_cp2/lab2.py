import re
import io

def enc(text, key):
    encText = ""
    key_letter_index = 0
    for letter in text:
            if key_letter_index < len(key):
                cipher = (alphabet.index(letter) + alphabet.index(key[key_letter_index])) % len(alphabet)
                encText += alphabet[cipher]
                key_letter_index = key_letter_index + 1
            else:
                key_letter_index = 0
                cipher = (alphabet.index(letter) + alphabet.index(key[key_letter_index])) % len(alphabet)
                encText += alphabet[cipher]
                key_letter_index = key_letter_index + 1
    return encText

def dec(text, key):
        decText = ""
        key_letter_index = 0
        for letter in text:
                if key_letter_index < len(key):
                    cipher = (alphabet.index(letter) - alphabet.index(key[key_letter_index])) % len(alphabet)
                    decText += alphabet[cipher]
                    key_letter_index = key_letter_index + 1
                else:
                    key_letter_index = 0
                    cipher = (alphabet.index(letter) - alphabet.index(key[key_letter_index])) % len(alphabet)
                    decText += alphabet[cipher]
                    key_letter_index = key_letter_index + 1
        return decText

# рахуємо індекси відповідності
def indexVidp(text):
    index = 0
    length = len(text)
    for i in range(len(alphabet)):
        letterCount = text.count(alphabet[i])
        index += letterCount * (letterCount - 1)
    index = index/(length*(length-1))
    return index

def diffKeyLength(text):
    print("Довжина ключа: __ ", " Ключ: ", "____".ljust(20), " Індекс відповідності: ", indexVidp(text))
    for key in keyList:
        encText = enc(text, key)
        print("Довжина ключа: ", str(len(key)).ljust(2), " Ключ: ", key.ljust(20), " Індекс відповідності: ", round(indexVidp(encText), 17))

# Розбиття тексту на блоки
def blocks(text, length):
    block = []
    for i in range(length):
        block.append(text[i::length]) #i з кроком length
    return block

#Розрахунок та виведення індексів відповідності
def keyLengthIndex(text):
    for i in range(1, len(alphabet)):   # беремо різні довжини ключів
        ourBlock = blocks(text, i)
        index = 0
        for i in range(len(ourBlock)):
            index = index + indexVidp(ourBlock[i])
            # print(indexVidp(ourBlock[i])
        index = index / len(ourBlock)
        print('Довжина ключа:', str(i + 1).ljust(2), ' Індекс відповідності: ', round(index,17))

#Знаходження ключа
def possibleKeys(text, keylen, letter):
    blockList = blocks(text, keylen)
    key = ""
    for i in range(len(blockList)):
        symbol = max(blockList[i], key = lambda count_: blockList[i].count(count_)) #Найбільш зустрівана літера
        key += alphabet[(alphabet.index(symbol) - alphabet.index(letter)) % len(alphabet)]
    return key

# ---------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    with io.open("text_task1.txt", encoding='utf-8') as file:
        clearText = file.read()
    clearText = re.sub("[^А-Яа-я ]", "", clearText)   # видаляємо всі символи крім зазначених
    clearText = re.sub(" +", "", clearText)           # виадаляємо всі пробіли
    clearText = clearText.lower()                     # переводимо всі символи в нижній регістр

    f = open('text_task1_clear.txt', 'w', encoding='utf-8')
    f.write(clearText)
    f.close()

    with io.open("var7.txt", encoding='utf-8') as file:
        varText = file.read()

    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

    keyList = ['хм', 'эус', 'шщьо', 'биафе', 'сягшдтъщтм', 'ештцътсьакр', 'эицюжгюнукре', 'жцгъъибщаызео', 'чзехржезйышусг',
    'рфгэспмйийыъйшт', 'прызсбрргзсыэцму', 'рщюцвьэлзпхфияупя', 'шъьмвяяудъслъшуьсд', 'лгсчрдмтйцкьяфлбьыд', 'ечояеъщтиащъщчшнцнйб']

    print(diffKeyLength(clearText)) # Індекс відповідності для ключів різної довжини(Перше завдання)

    keyLengthIndex(varText) # Викликаємо функцію для індексів відповідності для блоків різної довжини шифрованого тексту

    print("\n[+]Можливі ключі:")
    for letter in 'оеаитнслвр':                     # найчастіші букви у рос. мові
        print(">>>",possibleKeys(varText, 15, letter))     # ключ має довжину 15
    print("\n")

    decText = dec(varText, 'арудазовархимаг')  # змінили ключ з "арудазевархимаг" на "арудазовархимаг" А.Рудазов "Архимаг" - книга
    f = open('decText.txt', 'w', encoding='utf-8')
    f.write(decText)
    f.close()