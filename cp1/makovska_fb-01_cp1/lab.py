import re

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
f = frequency_of_letters(text, alfavit_sp)
print('Частота букв:\n', f)
e = entropy(f, 1)
print('\nЕнтропія:\n', e)

f1 = frequency_of_bigrams(text, alfavit_sp, True)
print('\nЧастота біграм H1:\n', f1)
e = entropy(f1, 2)
print('\nЕнтропія:\n', e)

f2 = frequency_of_bigrams(text, alfavit_sp, False)
print('\nЧастота біграм H2:\n', f2)
e = entropy(f2, 2)
print('\nЕнтропія:\n', e)

print('\n\n----------------------Обрахунки для тексту без пробілів-----------------------\n\n')

filter_txt('text.txt', False)
file = open('filtered.txt')
text_no_spaces = file.read()
file.close()

f = frequency_of_letters(text_no_spaces, alfavit)
print('Частота букв:\n', f)
e = entropy(f, 1)
print('\nЕнтропія:\n', e)

f1 = frequency_of_bigrams(text_no_spaces, alfavit, True)
print('\nЧастота біграм H1:\n', f1)
e = entropy(f1, 2)
print('\nЕнтропія:\n', e)

f2 = frequency_of_bigrams(text_no_spaces, alfavit, False)
print('\nЧастота біграм H2:\n', f2)
e = entropy(f2, 2)
print('\nЕнтропія:\n', e)

