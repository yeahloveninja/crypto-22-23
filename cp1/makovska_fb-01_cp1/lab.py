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

