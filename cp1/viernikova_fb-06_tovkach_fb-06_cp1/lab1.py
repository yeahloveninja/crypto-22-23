from collections import Counter
from math import log2
import pandas as pd
# Спочатку відкриємо наш текст
# text_file = open('cp1/viernikova_fb-06_tovkach_fb-06_cp1/text/test.txt', 'r').read()
text_file = open('cp1/viernikova_fb-06_tovkach_fb-06_cp1/text/1.txt', 'r').read()
text_file = text_file.lower().replace('ъ', 'ь').replace('ё', "е").replace('\n',' ')

alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя '

# Використовуючи метод filter викидаємо з тексту все що не відповідає нашому алфавіту
text_file = filter(lambda x: (x in alphabet), text_file) 
text_file = ''.join(list(text_file))

# Тут допоки у тексті є 2 пробіли ми заміняємо їх на 1 пробіл, на виході отримаємо текст з пробілами
while "  " in text_file:
    text_file = text_file.replace("  ", " ")

# Тут методом replace замінюємо всі пробіли і отримаємо текст без пробілів
ns_text_file = text_file.replace(' ', '')

# запишемо очищенні тести у файли
# open('cp1/viernikova_fb-06_tovkach_fb-06_cp1/text/1_space.txt', 'w').write(text_file)
# open('cp1/viernikova_fb-06_tovkach_fb-06_cp1/text/1_no_space.txt', 'w').write(ns_text_file)

bigram = Counter([text_file[i:i + 2] for i in range(0, len(text_file) - 1)])
# print(bigram) 
bg_df = pd.DataFrame(list(bigram.items()), columns=['Біграма', 'к-сть.'])

def l_freq(dict):
    l_sum = sum(dict.values()) 
    for i in dict.keys():
        dict[i] = dict[i] / l_sum 
        
def l_ent(dict):
    for i in dict.keys():
        dict[i] = -(dict[i] * log2(dict[i])) 

def l_R(entropy, space = False):
    if space == True:
        r = 1 - entropy / log2(32)
        return r
    else:
        r = 1 - entropy / log2(31)
        return r

l_freq(bigram)
bg_df['Частота'] = bigram.values()
l_ent(bigram)
bg_df['Ентропія'] = bigram.values()

bg_df.to_csv('cp1/viernikova_fb-06_tovkach_fb-06_cp1/test.csv', index=False)
all_entropy = sum(bigram.values())/2
print(f'Загальна ентропія: {all_entropy}')
print(f'Надлишковість: {l_R(all_entropy)}')



