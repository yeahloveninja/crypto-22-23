from itertools import cycle
import re


alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

#keys from 1,2,3,4,5 and 10-20
keys = ['яд', 'аут', 'беда', 'вагон',  'далматинец', 'живодерство', 'заботливость', 'камнедробилка', 'надувательство', 'техобслуживание', 'патриархальность', 'самовоспламенение', 'недобросовестность', 'многозначительность', 'сверхъестественность']

data = {}
def coincidenceIndex(targetText):
    index = 0
    length = len(targetText)
    for element in range(len(alphabet)):
        letterCounter = targetText.count(alphabet[element])
        index += letterCounter * (letterCounter - 1)
    index *= 1 / (length * (length - 1))
    return index

#read file master and margarit (without spaces, special symbols and all to lower case, was performed on Java)
with open('textMaster.txt', 'r') as file1:
    ourText = file1.read()
#read given file of 4th variant
with open('texe.txt', 'r', encoding='utf-8') as file1:
    newText = file1.read()


#loop over keys array, and for every key ouput value with using methods
for key in keys:
    print("Key len = ", len(key), f'and key is: "{key}"')
    finalText = ''
    for symbol, symbolKey in zip(ourText, cycle(key)):
        finalText += alphabet[(alphabet.find(symbol) + alphabet.find(symbolKey)) % 32]
    print("Encoded text: ", finalText)
    vigenereDecrypt = ''
    for symbol, symbolKey in zip(finalText, cycle(key)):
        vigenereDecrypt += alphabet[(alphabet.find(symbol) - alphabet.find(symbolKey)) % 32]
    print("Decoded text: ", vigenereDecrypt)
    print("Coincidence index: ", coincidenceIndex(finalText), "\n")

#encoding master text with our keys
for key in keys:
    masterText = ''
    for symbol, symbolKey in zip(ourText, cycle(key)):
        masterText += alphabet[(alphabet.find(symbol) + alphabet.find(symbolKey)) % 32]  # 32 lenght of alpha
    data[len(key)] = [key + ' : ' + ''.join(masterText)]

#coinci index start master text
print("\nCoinc, index starts with = ", coincidenceIndex(ourText), "\n")

#loop over alphabet with i itteration, for finding index of our fiven text 4 variant
for i in range(1, len(alphabet) + 1):
    blockList = []
    for element in range(i):
        blockList.append(newText[element::i])
    beginingIndex = 0

    for element in range(len(blockList)):
        beginingIndex = beginingIndex + coincidenceIndex(blockList[element])
    beginingIndex = beginingIndex / len(blockList)
    print(str(i), str(beginingIndex))

#so our closest index in alphabet was 13(0.0540) and 26(0.0538), so chosen was 13 - looping over most using russian letters
for letter in 'оае':
    blockList = []
    for element in range(13):
        blockList.append(newText[element::13])
    finalKey = ""
    for element in range(len(blockList)):
        frequent = ''
        frequentCount = 0
        for blockE in blockList[element]:
            el = blockList[element]
            if frequentCount < el.count(blockE):
                frequentCount = el.count(blockE)
                frequent = blockE
            else:
                continue
        finalKey += alphabet[(alphabet.index(frequent) - alphabet.index(letter)) % len(alphabet)]
    print(finalKey)

#combining 3 our string and answer for algorithm is 'громыковедьма' and decode
finalDecrypt = ''
for symbol, symbolKey in zip(newText, cycle('громыковедьма')):
    finalDecrypt += alphabet[(alphabet.find(symbol) - alphabet.find(symbolKey)) % 32]
print(finalDecrypt)
