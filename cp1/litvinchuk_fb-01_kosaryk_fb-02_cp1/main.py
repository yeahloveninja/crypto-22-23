import math
import re
import pandas as pd
import numpy as np

f = open("text.txt", encoding='utf-8')
text = f.read()
text = text.lower()
text = re.sub(r"[\W\d]", " ", text)
text = re.sub(r"[A-Za-z]", "", text)

text = " ".join(text.split()) #текст з пробілами
text_off = text.replace(" ", "") #текст без пробілів

letters_off = [] #список букв рос. алф. без пробілу
for i in range(ord('а'), ord('я')+1):
    letters_off.append(chr(i))

letters = [] #список букв рос. алф. із пробілом
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

all_bi_cross = []   #з пробілами + перетину
for i in range(0, len(text) - 1):
    all_bi_cross.append(text[i] + text[i + 1])


all_bi_not_cross = []   #з пробілами без перетину
for i in range(0, len(text) - 2, 2):
    all_bi_not_cross.append(text[i] + text[i + 1])

all_off_bi_not_cross = []   #без пробілами без перетину
for i in range(0, len(text_off) - 2, 2):
    all_off_bi_not_cross.append(text_off[i] + text_off[i + 1])


                                    #РОБОТА З ТЕКСТОМ БЕЗ ПРОБІЛІВ

frequency1_l_off = {} #частота букв без пробілів
for i in letters_off:
    frequency1_l_off[i] = text_off.count(i)/len(text_off)

frequency2_bi_off_cross = {} #частота біграм в тексті без пробілів + перетин
for i in letters_off_bi:
    frequency2_bi_off_cross[i] = all_off_bi_cross.count(i)/(2*len(all_off_bi_cross))

frequency2_bi_off_not_cross = {} #частота біграм із тексту без проблів + не перетин
for i in letters_off_bi:
    frequency2_bi_off_not_cross[i] = all_off_bi_not_cross.count(i) / (2*len(all_off_bi_not_cross))



                                    #РОБОТА З ТЕКСТОМ З ПРОБІЛАМИ

frequency1_l = {}#частота букв із пробілами
for i in letters:
    frequency1_l[i] = text.count(i) / len(text)

frequency2_bi_cross = {} #частота біграм із тексту з проблів + перетин
for i in letters_bi:
    frequency2_bi_cross[i] = all_bi_cross.count(i) / (2 * len(all_bi_cross))

frequency2_bi_not_cross = {} #частота біграм із тексту з пробілами + не перетин
for i in letters_off_bi:
    frequency2_bi_not_cross[i] = all_bi_not_cross.count(i) / (2 * len(all_bi_not_cross))

                                            #ОБЧИСЛЕННЯ ЕНТРОПІЇ

    #ДЛЯ БУКВ
sum1 = 0
for i in frequency1_l_off.values():
    sum1 = sum1 + (i*math.log(i, 2))
h1_off = -sum1   #для букв + текс без пробілів
print("H1 (без проб.): ", h1_off)

#h1 з пробілами
sum2 = 0
for i in frequency1_l.values():
    sum2 = sum2 + (i*math.log(i, 2))
h1 = -sum2   #для букв + текст з пробілами
print("H1 (з проб.) : ", h1)


    #ДЛЯ БІГРАМ
sum3 = 0
for i in frequency2_bi_off_not_cross.values():
    if i != 0:
        sum3 = sum3 + (i * math.log(i, 2))
h2_off_not_cross = -sum3   #біграми з тексту без пробілів + не перетин.
print("H2 (без проб., не перетин.): ", h2_off_not_cross)

sum4 = 0
for i in frequency2_bi_not_cross.values():
    if i != 0:
        sum4 = sum4 + (i * math.log(i, 2))
h2_not_cross = -sum4   #біграми з тексту з пробілами + не перетин.
print("H2 ( з проб., не перетин.) : ", h2_not_cross)

sum5 = 0
for i in frequency2_bi_cross.values():
    if i != 0:
        sum5 = sum5 + (i * math.log(i, 2))
h2_cross = -sum5    #біграми з тексту з пробілами + перетин.
print("H2 (з проб., перетин.) : ", h2_cross)

sum6 = 0
for i in frequency2_bi_off_cross.values():
    if i != 0:
        sum6 = sum6 + (i * math.log(i, 2))
h2_off_cross = -sum6  #біграми з тексту без пробілів + перетин.
print("H2 (без проб., перетин.) : ", h2_off_cross)

                                            #НАДЛИШКОВІСТЬ

R_h1 = 1 - (h1/(math.log(33, 2)))
R_h1_off =1 - (h1_off/(math.log(33, 2)))
R_h2_cross =1 - (h2_cross/(math.log(33, 2)))
R_h2_cross_off =1 - (h2_off_cross/(math.log(33, 2)))
R_h2_notcross =1 - (h2_not_cross/(math.log(33, 2)))
R_h2_notcross_off = 1 - (h2_off_not_cross/(math.log(33, 2)))

print('R1 - ', R_h1)
print('R2 - ', R_h1_off)
print('R3 - ', R_h2_cross)
print('R4 - ', R_h2_cross_off)
print('R5 - ', R_h2_notcross)
print('R6 - ', R_h2_notcross_off)

                                        #ПЕРЕНЕСЕННЯ ДАНИХ В ТАБЛИЦЮ
    #частота букв у тексті без пробілів
sorted_fr = dict(sorted(frequency1_l_off.items(), key=lambda item:item[1], reverse=True))
f1 = pd.DataFrame(sorted_fr, index=["frequency"])
f1.to_excel("fr.letters.off.xlsx")
it = iter(sorted_fr.items())
for i in range(10):
    print(next(it))
print("\n")
    #частота букв у тексті з пробілів
sorted_fr = dict(sorted(frequency1_l.items(), key=lambda item:item[1], reverse=True))
f1 = pd.DataFrame(sorted_fr, index=["frequency"])
f1.to_excel("fr.letters.xlsx")
it1 = iter(sorted_fr.items())
for i in range(10):
    print(next(it1))

 #частоти біграм(що перетинаються) у тексті без пробілів
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

    #частоти біграм(що перетинаються) у тексті з пробілами
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

    #частоти біграм(що не перетинаються) у тексті без пробілів
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

    #частоти біграм(що не перетинаються) у тексті з пробілів
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

