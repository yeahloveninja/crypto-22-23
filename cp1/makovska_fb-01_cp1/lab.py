import re

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
    dictionary = {} # створ словник, куди заносимо значення у відношенні літера:кількість зустріваності
    for l in alfavit:
        dictionary[l] = 0
    for l in txt: # якщо літера є в тексті, збільшуємо її частоту зустріваності на 1
        dictionary[l] += 1

    freq = {} # рахуємо частоту для кожної літери і заносимо в словник
    for l in alfavit:
        freq[l] = (dictionary[l])/len(txt)
        freq[l] = round(freq[l], 6)
    return freq

# готуємо текст до подальших обчислень
filter_txt('text.txt', True)
file = open('filtered.txt')
text = file.read()
file.close()

alfavit_sp = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя ' # алфавіт + пробіл
print('Частота букв в тексті (з пробілами): \n\n', frequency_of_letters(text, alfavit_sp))
