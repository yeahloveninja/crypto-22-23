import re
from collections import Counter
import math
import pandas as pd

with open("text.txt", encoding='utf8') as file:
    text = file.read()

alphabet_without_spaces = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'
al = []
for i in alphabet_without_spaces:
    al.append(i)
alsp = []
alphabet_with_spaces = ' абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'
for i in alphabet_with_spaces:
    alsp.append(i)

splited = re.compile('[^а-яёА-ЯЁ ]').sub('', text).rstrip('.,').lower().split(' ')
cleansp = ' '.join(splited)
clean = ''.join(splited)
clean_textsp = open('clean_textsp.txt', 'w')
clean_textsp.write(cleansp)  # текст з пробілами
clean_text = open('clean_text.txt', 'w')
clean_text.write(clean)  # текст без пробілів


def letters_frequency(txt):  # функція для підрахунку частоти букв
    c = Counter()
    frequency = {}
    total = 0
    for line in txt:
        c += Counter(line)  # рахуємо скільки разів зустрічається кожна літера в тексті
    for letter in alphabet_without_spaces:
        frequency[letter] = c[letter]/len(txt)
        #print(letter, frequency[letter])
    # h1 обчислюємо ентропію
    for i in frequency.values():
        total += i*math.log2(i)
    h1 = -total
    print('H1:', h1)
    
    # обчислюємо надлишок
    R = 1 - (h1 / math.log2(len(alphabet_without_spaces)))
    print('R:', R)

    letters_data = pd.DataFrame(data=frequency, index=['частота'])
    #print(letters_data)
    letters_data.to_excel('frequency_of_letters.xlsx')


def bigrams_frequency(txt, intersection=True):  #частота біграм
    c = Counter()
    frequency = {}
    index = 0
    if txt == clean:
        alph = alphabet_without_spaces
    else:
        alph = alphabet_with_spaces
    for letter1 in alph:
        for letter2 in alph:
            bigram = letter1 + letter2
            c[bigram] = 0

    if intersection is True:  # біграми з перетином
        for i in range(len(txt) - 1):  # до останньої літери
            bigram = txt[i] + txt[i + 1]
            c[bigram] += 1  # рахуємо скільки разів зустрічається біграма
        for bigram in c.keys():
            frequency[bigram] = c[bigram] / sum(c.values())  # частота кожної біграми
            #print(bigram, frequency[bigram])

    else:  # біграми без перетину
        for i in range(0, len(txt) - 1, 2):  # крок 2
            bigram = txt[i] + txt[i + 1]
            c[bigram] += 1  # рахуємо скільки разів зустрічається біграма

        for bigram in c.keys():
            frequency[bigram] = c[bigram] / sum(c.values())  # частота кожної біграми
            #print(bigram, frequency[bigram])
    
    # h2 обчислюємо ентропію
    total = 0
    for i in frequency.values():
        if i > 0:
            total += i*math.log2(i)
    h2 = -total / 2
    print('H2:', h2)

    # обчислюємо надлишок
    R = 1 - (h2 / math.log2(len(alph)))
    print('R:', R)
    big_fr = list(frequency.values())
    bigrams_data = pd.DataFrame(data=frequency, index=al, columns=al)

    for i in range(0, len(al)):
        bigrams_data[al[i]] = big_fr[index:len(al) + index]
        index = len(al) + index
    #print(bigrams_data)

    bigrams_data.to_excel('frequency_of_bigrams.xlsx')


letters_frequency(clean)
bigrams_frequency(clean, intersection=False)

info = pd.DataFrame(index=alphabet_without_spaces.split(), columns=alphabet_without_spaces.split())