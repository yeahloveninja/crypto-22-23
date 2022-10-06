import re
import math
import pandas as pd
import numpy as np

alfavit = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя' # алфавіт
alfavit_sp = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя ' # алфавіт + пробіл

def filter_txt( file_name, spaces = True ):
    # зчитуємо текст
    file = open( file_name, encoding="utf8" )
    t = file.read()
    file.close()
    # переводимо всі літери в нижній регістр і оброблюємо
    lower_text = t.lower()
    if (spaces == True):     # якщо залишити пробіли
        new_txt = re.sub( r'[^а-яё ]', '', lower_text )
    else:
        new_txt = re.sub( r'[^а-яё]', '', lower_text )
    # записуємо оброблений текст у файл
    new_file = open('filtered.txt', 'w')
    new_file.write(new_txt)
    new_file.close()

def frequency_of_letters(txt, alfavit):
    dictionary = {} # словник зі значеннями літера:кількість зустріваності
    for l in alfavit:
        dictionary[l] = 0
    for l in txt: # якщо літера є в тексті, збільшуємо її частоту зустріваності
        dictionary[l] += 1

    freq = {} # рахуємо частоту для кожної літери і заносимо в словник
    for l in alfavit:
        freq[l] = (dictionary[l])/len(txt)
        freq[l] = round(freq[l], 6)
    return freq

def frequency_of_bigrams(txt, alfavit, cross = True):
    dictionary = {} # словник зі значеннями біграма:кількість зустріваності
    freq = {}
    for l1 in alfavit:
        for l2 in alfavit:
            key = l1 + l2
            dictionary[key] = 0

    #H1 - беремо перехресні пари абвгде - аб бв вг гд ге
    if (cross == True): 
        for i in range(len(txt)-1):  # до передостанньої літери 
            key = txt[i] + txt[i+1]  # беремо 2 літери, які стоять поруч в тексті
            dictionary[key] += 1     # збільш частоту зустріваності їх пари

        for key in dictionary.keys():   # для кожної біграми (пари літер) рахуємо частоту 
            freq[key] = dictionary[key]/(len(txt)-1)   
            freq[key] = round(freq[key], 6)

    #H2 - беремо кожні 2 елемента абвгде - аб вг де
    else: 
        if len(txt) % 2 == 1:
            txt += "а"   # щоб кожній літері була пара
        i = 0
        for i in range(len(txt) - 1):
            if i % 2 == 1:
                continue
            key = txt[i] + txt[i+1]
            dictionary[key] += 1     # рахуємо частоту в тексті

        for key in dictionary.keys():
            freq[key] = dictionary[key]/(len(txt)/2)
            freq[key] = round(freq[key], 6)
    return freq

def entropy(dictionary, n):
    entropies = []
    for k in dictionary.keys():
        if dictionary[k] != 0:
            e = abs(float(dictionary[k]) * math.log2(dictionary[k])/n)
            entropies.append(e)
    entropy = sum(entropies)
    return entropy

filter_txt('text.txt', True)
file = open('filtered.txt')
text = file.read()
file.close()

print('----------------------Обрахунки для тексту з пробілами-----------------------\n\n')
f_1 = frequency_of_letters(text, alfavit_sp)
print('Частота букв: ', f_1)
e = entropy(f_1, 1)
print('\nH1: ', e)
print('\nНадлишковість: ', (1 - (e/math.log2(len(alfavit_sp)))))

f1_1 = frequency_of_bigrams(text, alfavit_sp, True)
print('\nЧастота біграм: ', f1_1)
e = entropy(f1_1, 2)
print('\nH2: ', e)
print('\nНадлишковість: ', (1 - (e/math.log2(len(alfavit_sp)))))

f2_1 = frequency_of_bigrams(text, alfavit_sp, False)
print('\nЧастота перехресних біграм: ', f2_1)
e = entropy(f2_1, 2)
print('\nH2 (перехресна): ', e)
print('\nНадлишковість: ', (1 - (e/math.log2(len(alfavit_sp)))))

print('\n\n----------------------Обрахунки для тексту без пробілів-----------------------\n\n')

filter_txt('text.txt', False)
file = open('filtered.txt')
text_no_spaces = file.read()
file.close()

f_2 = frequency_of_letters(text_no_spaces, alfavit)
print('Частота букв: ', f_2)
e = entropy(f_2, 1)
print('\nH1: ', e)
print('\nНадлишковість: ', (1 - (e/math.log2(len(alfavit_sp)))))

f1_2 = frequency_of_bigrams(text_no_spaces, alfavit, True)
print('\nЧастота біграм: ', f1_2)
e = entropy(f1_2, 2)
print('\nH2: ', e)
print('\nНадлишковість: ', (1 - (e/math.log2(len(alfavit_sp)))))

f2_2 = frequency_of_bigrams(text_no_spaces, alfavit, False)
print('\nЧастота перехресних біграм: ', f2_2)
e = entropy(f2_2, 2)
print('\nH2 (перехресна): ', e)
print('\nНадлишковість: ', (1 - (e/math.log2(len(alfavit_sp)))))



alfavit_sp = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'э', 'ж', 'з', 'и', 'ы', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я', ' ']
alfavit = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'э', 'ж', 'з', 'и', 'ы', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я']
data = pd.DataFrame(index = alfavit_sp, columns = alfavit_sp)

bigr = []

for l1 in alfavit_sp: # створили біграми
    for l2 in alfavit_sp: 
        bigr.append(l1+l2)
 
n = 0
for i in range(len(alfavit_sp)): # занесли біграми в таблицю 
    data[alfavit_sp[i]] = bigr[n:len(alfavit_sp)+n]
    n = len(alfavit_sp) + n
data = data.T # транспонували


for bigr_name in list(f1_1.keys()): 
    i1,i2 = np.where(data == bigr_name) 
    data.iloc[i1,i2] = f1_1[bigr_name] # на місце, де були написані біграми, вставляємо їх частоту
    
data.to_excel('bigr_fr_H1.xlsx') 


data = pd.DataFrame(index = alfavit_sp, columns = alfavit_sp)

bigr = []

for l1 in alfavit_sp: 
    for l2 in alfavit_sp: 
        bigr.append(l1+l2)
 
n = 0
for i in range(len(alfavit_sp)): 
    data[alfavit_sp[i]] = bigr[n:len(alfavit_sp)+n]
    n = len(alfavit_sp) + n
data = data.T 


for bigr_name in list(f2_1.keys()): 
    i1,i2 = np.where(data == bigr_name) 
    data.iloc[i1,i2] = f2_1[bigr_name] 
    
data.to_excel('bigr_fr_H2.xlsx') 


data = pd.DataFrame(index = alfavit, columns = alfavit)

bigr = []

for l1 in alfavit: 
    for l2 in alfavit: 
        bigr.append(l1+l2)
 
n = 0
for i in range(len(alfavit)): 
    data[alfavit[i]] = bigr[n:len(alfavit)+n]
    n = len(alfavit) + n
data = data.T 


for bigr_name in list(f1_2.keys()): 
    i1,i2 = np.where(data == bigr_name) 
    data.iloc[i1,i2] = f1_2[bigr_name] 
    
data.to_excel('bigr_fr_H1_nosp.xlsx') 


data = pd.DataFrame(index = alfavit, columns = alfavit)

bigr = []

for l1 in alfavit: 
    for l2 in alfavit: 
        bigr.append(l1+l2)
 
n = 0
for i in range(len(alfavit)): 
    data[alfavit[i]] = bigr[n:len(alfavit)+n]
    n = len(alfavit) + n
data = data.T 


for bigr_name in list(f2_2.keys()): 
    i1,i2 = np.where(data == bigr_name) 
    data.iloc[i1,i2] = f2_2[bigr_name] 
    
data.to_excel('bigr_fr_H2_nosp.xlsx') 
