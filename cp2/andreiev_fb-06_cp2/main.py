import re


alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
alphabet_with_nums = {i: num for num, i in enumerate(alphabet)}
reverse_alphabet_with_nums = {num: i for num, i in enumerate(alphabet)}


#модифікація фільтрації тексту з попереднього практикуму
def filter_text(text):
    text = re.sub(r'[^а-яА-Я ]', '', text).lower().replace(" ", "").replace("ё", "е")
    return text

with open("text.txt", 'r') as f:
    text = f.read()

text = 'дыханиельдастильпятыйнифльхейм'
# text = filter_text(text)
key = 'самба'

def vigenere_encrypt(open_text, key):
    res = ''
    for i in range(len(open_text)):
        open_char = open_text[i]
        key_char = key[i % len(key)]

        open_num = alphabet_with_nums[open_char]
        key_num = alphabet_with_nums[key_char]

        encrypted_char = reverse_alphabet_with_nums[(open_num + key_num) % len(alphabet)]
        res += encrypted_char
    return res


print(vigenere_encrypt(text, key))
    
