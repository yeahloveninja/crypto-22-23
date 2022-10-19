from collections import Counter
from math import log2
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
open('cp1/viernikova_fb-06_tovkach_fb-06_cp1/text/1_space.txt', 'w').write(text_file)
open('cp1/viernikova_fb-06_tovkach_fb-06_cp1/text/1_no_space.txt', 'w').write(ns_text_file)

mono_text = Counter(text_file)
#print(mono_text) 

def l_freq(dict):
    l_sum = sum(dict.values()) 
    for i in dict.keys():
        dict[i] = dict[i] / l_sum 
        
def l_ent(dict):
    for i in dict.keys():
        dict[i] = -(dict[i] * log2(dict[i])) 

def l_R(entropy):
        r = 1 - entropy / log2(32)
        return r

l_freq(mono_text)
#print(mono_text)
l_ent(mono_text)
#print(mono_text)

all_entropy = sum(mono_text.values())
#print(all_entropy)
#print(l_R(all_entropy))


