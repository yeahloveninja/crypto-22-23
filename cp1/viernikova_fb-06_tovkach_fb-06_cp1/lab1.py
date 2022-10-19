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
