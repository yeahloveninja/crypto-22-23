import math
import re
import pandas as pd
import numpy as np

f = open("text.txt", encoding='utf-8')
text = f.read()
text = re.sub( r'[^а-яё ]', ' ', text.lower())
text = " ".join(text.split())
text_off = text.replace(' ', '')

letters_off = []
for i in range(ord('а'), ord('я')+1):
    letters_off.append(chr(i))
letters_off.append('ё')
letters = []
for i in letters_off:
    letters.append(i)
letters.append(" ")

letters_off_bi = [] #список усіх біграм із алфавіту без пробілу
for i in letters_off:
    for j in letters_off:
        letters_off_bi.append(i+j)
letters_bi = [] #список усіх біграм із алфавіту з пробілом
for i in letters:
    for j in letters:
        letters_bi.append(i+j)

all_off_bi_cross = []     #без пробілів + перетин
for i in range(0, len(text_off)-1):
    all_off_bi_cross.append(text_off[i] + text_off[i + 1])

all_off_bi_not_cross = []   #без пробілів без перетину
for i in range(0, len(text_off) - 2, 2):
    all_off_bi_not_cross.append(text_off[i] + text_off[i + 1])

all_bi_cross = []   #з пробілами + перетину
for i in range(0, len(text) - 1):
    all_bi_cross.append(text[i] + text[i + 1])

all_bi_not_cross = []   #з пробілами без перетину
for i in range(0, len(text)-2, 2):
    all_bi_not_cross.append(text[i] + text[i + 1])

                                    #РОБОТА З ТЕКСТОМ БЕЗ ПРОБІЛІВ (частота)

frequency1_l_off = {} #частота букв без пробілів
for i in letters_off:
    frequency1_l_off[i] = text_off.count(i)/len(text_off)

frequency2_bi_off_cross = {} #частота біграм в тексті без пробілів + перетин
for i in letters_off_bi:
    frequency2_bi_off_cross[i] = all_off_bi_cross.count(i)/(len(text_off)-1)

frequency2_bi_off_not_cross = {} #частота біграм із тексту без проблів + не перетин
for i in letters_off_bi:
    frequency2_bi_off_not_cross[i] = all_off_bi_not_cross.count(i)/(len(text_off)/2)


                                    #РОБОТА З ТЕКСТОМ З ПРОБІЛАМИ (частота)

frequency1_l = {}#частота букв із пробілами
for i in letters:
    frequency1_l[i] = text.count(i) / len(text)

frequency2_bi_cross = {} #частота біграм із тексту з проблів + перетин
for i in letters_bi:
    frequency2_bi_cross[i] = all_bi_cross.count(i) / (len(text)-1)

frequency2_bi_not_cross = {} #частота біграм із тексту з пробілами + не перетин
for i in letters_bi:
    frequency2_bi_not_cross[i] = all_bi_not_cross.count(i) / (len(text)/2)

                                            #ОБЧИСЛЕННЯ ЕНТРОПІЇ
sum1 = 0
for i in frequency1_l_off.values():
    sum1 = sum1 + (i * math.log2(i))
h1off = -sum1   #для букв + текс без пробілів

sum2 = 0
for i in frequency1_l.values():
    sum2 = sum2 + (i * math.log2(i))
h1 = -sum2   #для букв + текст з пробілами

def entropy(dictionary):
    entr = 0
    for i in dictionary.values():
        if i != 0:
            entr += i * math.log2(i)/2
    return -entr

h2cross = entropy(frequency2_bi_cross)
h2crossoff = entropy(frequency2_bi_off_cross)
h2notcross = entropy(frequency2_bi_not_cross)
h2notcrossoff = entropy(frequency2_bi_off_not_cross)
print('       Значення етропії:\n')
print('H1 (з пробілами)', h1)
print('H1 (без пробілів)',h1off)
print('H2 ( перетин., з пробілами)',h2cross)
print('H2 ( перетин., без пробілів)',h2crossoff)
print('H2 ( не перетин., з пробілами)',h2notcross)
print('H2 ( не перетин., без пробілів)',h2notcrossoff)
                                            #НАДЛИШКОВІСТЬ
R_h1 = 1 - (h1/(math.log2(len(letters))))
R_h1_off = 1 - (h1off/(math.log2(len(letters_off))))
R_h2_cross = 1 - (h2cross/(math.log2(len(letters))))
R_h2_cross_off = 1 - (h2crossoff/(math.log2(len(letters_off))))
R_h2_notcross = 1 - (h2notcross/(math.log2(len(letters))))
R_h2_notcross_off = 1 - (h2notcrossoff/(math.log2(len(letters_off))))
print('\n       Значення надлишковості:')
print('R1 (букви з пробілами) - ', R_h1)
print('R2 (букви без пробілів) - ', R_h1_off)
print('R3 (біграми перетин. з пробілами)- ', R_h2_cross)
print('R4 (біграми перетин. без пробілів) -', R_h2_cross_off)
print('R5 (біграми не перетин. з пробілами) - ', R_h2_notcross)
print('R6 (біграми не перетин. без пробілів) - ', R_h2_notcross_off)
                                        #ПЕРЕНЕСЕННЯ ДАНИХ В ТАБЛИЦЮ
sorted_fr = dict(sorted(frequency1_l_off.items(), key = lambda item:item[1], reverse=True))
f1 = pd.DataFrame(sorted_fr, index=["frequency"])
f1.to_excel("fr.letters.off.xlsx")

sorted_fr = dict(sorted(frequency1_l.items(), key=lambda item:item[1], reverse=True))
f1 = pd.DataFrame(sorted_fr, index=["frequency"])
f1.to_excel("fr.letters.xlsx")

f = pd.DataFrame(index=letters_off, columns=letters_off)
letter = 0
for i in range(0, len(letters_off)):
    f[letters_off[i]] = letters_off_bi[letter:len(letters_off) + letter]
    letter = len(letters_off) + letter
f = f.T
for i in list(frequency2_bi_off_not_cross.keys()):
    k, v = np.where(f == i)
    f.iloc[k, v] = frequency2_bi_off_not_cross[i]
for i in letters_off_bi:
    k, v = np.where(f == i)
    f.iloc[k, v] = 0
f.to_excel('fr.bi.cross.off.xlsx')

f = pd.DataFrame(index=letters, columns=letters)
letter = 0
for i in range(0, len(letters)):
    f[letters[i]] = letters_bi[letter:len(letters) + letter]
    letter = len(letters) + letter
f = f.T
for i in list(frequency2_bi_cross.keys()):
    k, v = np.where(f == i)
    f.iloc[k, v] = frequency2_bi_cross[i]
for i in letters_bi:
    k, v = np.where(f == i)
    f.iloc[k, v] = 0
f.to_excel('fr.bi.cross.xlsx')

f = pd.DataFrame(index=letters_off, columns=letters_off)
letter = 0
for i in range(0, len(letters_off)):
    f[letters_off[i]] = letters_off_bi[letter:len(letters_off) + letter]
    letter = len(letters_off) + letter
f = f.T
for i in list(frequency2_bi_off_not_cross.keys()):
    k, v = np.where(f == i)
    f.iloc[k, v] = frequency2_bi_off_not_cross[i]
for i in letters_off_bi:
    k, v = np.where(f == i)
    f.iloc[k, v] = 0
f.to_excel('fr.bi.notcross.off.xlsx')

f = pd.DataFrame(index=letters, columns=letters)
letter = 0
for i in range(0, len(letters)):
    f[letters[i]] = letters_bi[letter:len(letters) + letter]
    letter = len(letters) + letter
f = f.T
for i in list(frequency2_bi_not_cross.keys()):
    k, v = np.where(f == i)
    f.iloc[k, v] = frequency2_bi_not_cross[i]
for i in letters_bi:
    k, v = np.where(f == i)
    f.iloc[k, v] = 0
f.to_excel('fr.bi.notcross.xlsx')

results = open('results.txt','a',encoding='utf8')
results.write('Table of frequencies:\n')
temp = dict(sorted(frequency1_l_off.items(), key = lambda item:item[1], reverse=True))
for key in temp:
    results.write("{:^4}<{:^.5f}>\n".format(key, frequency1_l_off[key]))