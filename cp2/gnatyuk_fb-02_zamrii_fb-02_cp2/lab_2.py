import re
import math
text_with_spaces1 = open("with_space.txt", "r", encoding='utf-8')
text_with_spaces = text_with_spaces1.read()
text_with_spaces = text_with_spaces.lower()
text_with_spaces = re.sub(r"[\W\d]", " ", text_with_spaces)
text_with_spaces = re.sub(r"[A-Za-z]", " ", text_with_spaces)
no_spaces_text = text_with_spaces.replace(" ", "")

file = open("no_space.txt", "w")
file.write(no_spaces_text)
file.close()
text_with_spaces1.close()

alphabet = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ы','ь','є','ю','я']
ind_alphabet = []
for i in range(0, len(alphabet)+1):
    ind_alphabet.append(i)

alphabet_dict = dict(zip(ind_alphabet, alphabet))

open_text = []
for i in no_spaces_text:
    open_text.append(i)
print('Відкритий текст:', open_text)

index_text = []
for i in range(len(open_text)):
    for j in alphabet_dict:
        if open_text[i] == alphabet_dict[j]:
            index_text.append(j)
print('Індекси відкритого тексту:', index_text, '\n')

def Vigenere(key):
    print('Ключ довжиною:', len(key))
    len_key_list = key*math.ceil(len(open_text)/len(key))
    key_list = []
    for i in len_key_list:
       while len(key_list) < len(open_text):
            key_list.append(i)
            break
    print('Ключ:', key_list)

    index_key = []
    for l in range(len(key_list)):
        for k in alphabet_dict:
            if key_list[l] == alphabet_dict[k]:
                index_key.append(k)
    print('Індекси ключа:', index_key)

    index_close_text = []
    for n in range(len(index_text)):
            index_close_text.append((index_text[n] + index_key[n])%32)
    print('Індекси шифрованого тексту:', index_close_text)

    close_text = []
    for i in range(len(index_close_text)):
        for j in alphabet_dict:
            if index_close_text[i] == j:
                close_text.append(alphabet_dict[j])
    print('Зашифрований текст: ', *close_text, sep='')

    counter = 0
    for i in alphabet:
        counter = counter + no_spaces_text.count(i) * (no_spaces_text.count(i) - 1)
    compliance_index = counter * (1 / (len(no_spaces_text) * (len(no_spaces_text) - 1)))
    print('Індекс відповідності ВТ:', round(compliance_index, 5))

    counter1 = 0
    for i in alphabet:
        counter1 = counter1 + close_text.count(i) * (close_text.count(i) - 1)
    compliance_index1 = counter1 * (1 / (len(close_text) * (len(close_text) - 1)))
    print('Індекс відповідності ШТ:', round(compliance_index1, 5))
    return ''

print(Vigenere('да'))
print(Vigenere('ркп'))
print(Vigenere('лраи'))
print(Vigenere('суолв'))
print(Vigenere('фвапролджб'))
print(Vigenere('хзщнекуцйфывапсмрувл'))