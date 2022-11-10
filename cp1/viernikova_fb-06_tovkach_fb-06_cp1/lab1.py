# Імпортуємо потрібні бібліотеки
from collections import Counter
import pandas as pd
from math import log2

# Спочатку відкриємо наш текст
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

# робимо функцію де робимо все що необхідно в лабі
def lab(text):
    # тут використавши метод Counter отримаємо словник де ключі - наші букви, а значення - їх кількість
    mono_text = Counter(text)
    # невеличка перевірка наявності пробілів у наданому тексті
    space = False
    if mono_text[' '] > 0:
        space = True

    # тут рахуємо частоту з якою зустрічаються наші моно- або біграми
    def l_freq(dict):
        l_sum = sum(dict.values()) # для цього рахуємо суму всіх значень
        for i in dict.keys():
            dict[i] = dict[i] / l_sum # а після перебираємо за кожним ключем значення і записуємо туди його ділення на суму всіх значень 
        
    # тут рахуємо ентропію за формулою з методички
    def l_ent(dict):
        for i in dict.keys():
            dict[i] = -(dict[i] * log2(dict[i])) # знову перезаписуємо за ключами їх ентропію

    # тут рахуємо надлишок за формулою, тут нам і потрібна перевірка чи є пробіл у тексті, щоб дізнатись скільки букв в нашому алфавіті
    def l_R(entropy):
        if space == True:
            r = 1 - entropy / log2(32)
            return r
        else:
            r = 1 - entropy / log2(31)
            return r
    
    # тут викликаємо функції і додаємо отримані дані у датафрейм
    def add_df(dict, df):
        l_freq(dict)
        df['Частота'] = dict.values()
        l_ent(dict)
        df['Ентропія'] = dict.values()
        if dict['а'] > 0: # невеличка перевірка на те монограма у нас чи ні
            all_entropy = sum(dict.values())
        else:
            all_entropy = sum(dict.values())/2
        df.at[0,'Загальна Ентропія'] = all_entropy
        df.at[0,'Надлишковість'] = l_R(all_entropy)

    # тут записуємо у csv наші дані
    def write_df(df, name):
        if space == True:
            df.to_csv(f'cp1/viernikova_fb-06_tovkach_fb-06_cp1/{name}_space.csv', index=False)
        else:
            df.to_csv(f'cp1/viernikova_fb-06_tovkach_fb-06_cp1/{name}_no_space.csv', index=False)
    
    #створюємо датафрейми та словники з нашими значеннями буквами *значення для монограми отримуємо на початку функції 
    mono_df = pd.DataFrame(list(mono_text.items()), columns=["Буква","к-сть"])
    add_df(mono_text, mono_df)
    write_df(mono_df, "monogram")

    bigram = Counter([text[i:i + 2] for i in range(0, len(text) - 1)])
    bi_df = pd.DataFrame(list(bigram.items()), columns=["Буква","к-сть"])
    add_df(bigram, bi_df)
    write_df(bi_df, "bigram")

    bigram_c = Counter([text[i:i + 2] for i in range(0, len(text) - 1, 2)])
    bi_c_df = pd.DataFrame(list(bigram_c.items()), columns=["Буква","к-сть"])
    add_df(bigram_c, bi_c_df)
    write_df(bi_c_df, "crossed_bigram")

# робимо виклик наших функцій
lab(text_file)
lab(ns_text_file)