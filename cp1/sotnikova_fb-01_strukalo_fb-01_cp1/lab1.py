from pprint import pprint
import math

ourFile = open("book_with_spaces.txt", mode="r", encoding="utf-8")
textWithSpaces = ourFile.read()
ourFile.close()

ourFile = open("book_without_spaces.txt", mode="r", encoding="utf-8")
textWithOutSpaces = ourFile.read()
ourFile.close()


def ourLetterFrequency(ourText):  # Підрахунок частоти наших букв у документі
    objectLetterAmount = {}  # Об'єкт {буква: кількість}
    for i in ourText:
        if i in objectLetterAmount: 
            objectLetterAmount[i] += 1
        else:
            objectLetterAmount[i] = 1
    generalSum = sum(objectLetterAmount.values())
    for symbol in objectLetterAmount:
        # Обчислюємо частоту букв (ділимо к-сть входжень символа на загальну к-сть)
        objectLetterAmount[symbol] = objectLetterAmount[symbol]/generalSum
    return objectLetterAmount

print("\nLetters Frequency in text with spaces")
pprint(ourLetterFrequency(textWithSpaces))
print("\nLetters Frequency in text without spaces")
pprint(ourLetterFrequency(textWithOutSpaces))


def bigGramCouple(ourText, crossing):  # Підрахунок частоти біграм
    objectCoupleAmount = {}  # Об'єкт {біграма: кількість}
    if crossing:  # Перехресна ентропія
        for i in range(0, len(ourText)):
            if ourText[i:i+2] in objectCoupleAmount:
                objectCoupleAmount[ourText[i:i+2]] += 1
            else:
                objectCoupleAmount[ourText[i:i+2]] = 1
    else:  # Пари букв, що не перетинаються
        for i in range(0, len(ourText), 2):  # з кроком два
            if ourText[i:i+2] in objectCoupleAmount:
                objectCoupleAmount[ourText[i:i+2]] += 1
            else:
                objectCoupleAmount[ourText[i:i+2]] = 1
                
    generalSum = sum(objectCoupleAmount.values())
    for couple in objectCoupleAmount:
    # Обчислюємо частоту біграм
        objectCoupleAmount[couple] = objectCoupleAmount[couple]/generalSum
    return objectCoupleAmount

print("\nBigrams frequency with intersection")
pprint(bigGramCouple(textWithSpaces, True))
print("\nBigrams frequency without intersection")
pprint(bigGramCouple(textWithSpaces, False))

######################################################################################################

print("\nBigrams frequency with intersection")
pprint(bigGramCouple(textWithOutSpaces, True))
print("\nBigrams frequency without intersection")
pprint(bigGramCouple(textWithOutSpaces, False))


def entropia(ourText, n=1, crossing=True):
    if n == 1:
        letterFrequency = ourLetterFrequency(ourText)  # Отримуємо об'єкт {буква: частота}
    elif n == 2:
        letterFrequency = bigGramCouple(ourText, crossing)  # Отримуємо об'єкт {біграма: частота}
    arrFrequency = letterFrequency.values()
    entropia = map(lambda probability: -probability * math.log2(probability), arrFrequency)
    entropia = sum(list(entropia)) / n
    return entropia

def surplus(h, amountAlphabet):  # Пошук надлишку
    R = 1 - (h/math.log2(amountAlphabet))
    return R

print("\nEntropy: ", entropia(textWithSpaces, 1))

h1Spaces = entropia(textWithSpaces)
h1NotSpaces = entropia(textWithOutSpaces)
h2Spaces = entropia(textWithSpaces, 2, False)
h2NotSpaces = entropia(textWithOutSpaces, 2, False)
h2SpacesCrossing = entropia(textWithSpaces, 2, True)
h2NotSpacesCrossing = entropia(textWithOutSpaces, 2, True)

######################################################################################################

print("\nH1 w/ spaces: ", h1Spaces, "surplus: ", surplus(h1Spaces, 34))
print("H1 w/o spaces: ", h1NotSpaces, "surplus: ", surplus(h1NotSpaces, 33))
print("H2 w/ spaces: ", h2Spaces, "surplus: ", surplus(h2Spaces, 34))
print("H2 w/o spaces: ", h2NotSpaces, "surplus: ", surplus(h2NotSpaces, 33))
print("H2 w/ spaces crossing: ", h2SpacesCrossing, "surplus: ", surplus(h2SpacesCrossing, 34))
print("H2 w/o spaces crossing: ", h2NotSpacesCrossing, "surplus: ", surplus(h2NotSpacesCrossing, 33))
