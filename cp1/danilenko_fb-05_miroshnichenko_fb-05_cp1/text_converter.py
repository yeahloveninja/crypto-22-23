import re

text = open("1.txt", 'r', encoding='utf-8').read()

alphabet = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'

text_down = text.lower()
result_text = ''
for i in list(text_down):
    if i in alphabet:
        result_text += i
    elif i == ' ':
        result_text += ' '

result_text = re.sub(r' +', '_', result_text)

print(result_text)

with open("2.txt", 'w') as file:
    file.write(result_text)

result_text = result_text.replace('_', '')
with open("3.txt", 'w') as file:
    file.write(result_text)
