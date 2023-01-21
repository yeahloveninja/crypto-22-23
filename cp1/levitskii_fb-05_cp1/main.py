import math
import re
from collections import Counter
import csv

AlphabetWithoutSpaces = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф','х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']
AlphabetWithSpaces = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф','х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я','_']

def text_check(textfile, space):
    file = open(textfile, encoding = 'utf-8')
    labtext = file.read()
    file.close()
    labtext = labtext.lower()
    if space == False:
        labtext = re.sub(" ","", labtext)
    text = re.sub(r'[^а-яё ]', "", labtext)
    text = re.sub(' {2,}', "",text).replace(" ", "_") #замінюємо пробіли на _, адже в csv пробіли не чітко видно
    return text

textWithSpaces = text_check("text.txt", True)
textWithoutSpaces = text_check("text.txt", False)

def CountEntropy(counter, n_gram):
    len = sum(counter.values())
    entropy = 0
    for i in counter:
        p = counter[i] / (len)
        entropy -= p*math.log(p,2)
    return entropy / n_gram

def Letter_frequency(text):
    letterfreq = Counter(text)
    for i in letterfreq:
        letterfreq[i] = letterfreq[i] / len(text)
    return letterfreq

letter_freq2 = Letter_frequency(textWithSpaces)
letter_freq = Letter_frequency(textWithoutSpaces)
print(f"Letter frequency without spaces: {letter_freq}")
print("--------------------------------")
print(f"Letter frequency with spaces: {letter_freq2}")

def BigramCounter(text, step):
   length = len(text)
   i = 0
   array = []
   while i < (length-1):
     array.append(text[i] + text[i+1])
     i += step
   return Counter(array)



CrossedWithSpace = BigramCounter(textWithSpaces, 1)
CrossedWithoutSpace = BigramCounter(textWithoutSpaces, 1)
NotCrossedWithSpace = BigramCounter(textWithSpaces, 2)
NotCrossedWithoutSpace = BigramCounter(textWithoutSpaces, 2)

def FilledBigramFreqency(bigrama, alphabet, outputfile):
    len = sum(bigrama.values())
    with open(outputfile, 'w', newline='', encoding='cp1251') as f:
        writer = csv.writer(f)
        for i in alphabet:
            info = []
            for j in alphabet:
                index = (i + j)
                p = bigrama[index] / len
                info.append(index + ": " + str(round(p, 7)) + " ")
            writer.writerow(info)


#FilledBigramFreqency(BigramCounter(textWithSpaces, 1), AlphabetWithSpaces, 'CrossedWithSpace.csv')
#FilledBigramFreqency(CrossedWithoutSpace, AlphabetWithoutSpaces, 'CrossedWithoutSpace.csv')
#FilledBigramFreqency(NotCrossedWithSpace, AlphabetWithSpaces, 'NotCrossedWithSpace.csv')
#FilledBigramFreqency(NotCrossedWithoutSpace, AlphabetWithoutSpaces, 'NotCrossedWithoutSpace.csv')


def nadl(e): # розрахунок надлишковості
    length = len(AlphabetWithoutSpaces)
    ans = 1 - (e/math.log2(length))
    return ans

letterCounter = Counter(textWithSpaces)
letterCounterwithoutspaces = Counter(textWithoutSpaces)




print('Letters entropy with spaces: ',CountEntropy(letterCounter, 1))
print(nadl(CountEntropy(letterCounter, 1)))
print('Letters entropy without spaces: ',CountEntropy(letterCounterwithoutspaces, 1))
print(nadl(CountEntropy(letterCounterwithoutspaces, 1)))
print('Crossed bigram with spaces entropy: ', CountEntropy(BigramCounter(textWithSpaces, 1),2))
print(nadl(CountEntropy(BigramCounter(textWithSpaces, 1),2)))
print('Crossed bigram without spaces entropy: ', CountEntropy(BigramCounter(textWithoutSpaces, 1),2))
print(nadl(CountEntropy(BigramCounter(textWithoutSpaces, 1),2)))
print('Not crossed bigram with spaces entropy: ', CountEntropy(BigramCounter(textWithSpaces, 2),2))
print(nadl(CountEntropy(BigramCounter(textWithSpaces, 2),2)))
print('Not crossed bigram without spaces entropy: ', CountEntropy(BigramCounter(textWithoutSpaces, 2),2))
print(nadl(CountEntropy(BigramCounter(textWithoutSpaces, 2),2)))
