import re

text = open("start_text.txt", 'r', encoding='utf-8').read()

alphabet = 'абвгдеэжзиыйклмнопрстуфхцчшщъьюя'

text_down = text.lower()
result_text = ''
for i in list(text_down):
    if i in alphabet:
        result_text += i
    elif i == ' ':
        result_text += ' '

result_text = re.sub(r' +', '_', result_text)
result_text = result_text.replace('_', '')
print(result_text)

with open("final_text.txt", 'w') as file:
    file.write(result_text)


