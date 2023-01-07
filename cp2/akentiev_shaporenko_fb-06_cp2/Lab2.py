import re

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
file = open('text.txt', encoding='utf-8')
text = file.read()


def fil_text(text):
    txt = re.sub(r'[^а-яА-Я ]', '', text)
    space = txt.lower().replace('  ', ' ').replace('   ', ' ')
    return space


textWithSpace = fil_text(text)
textWithoutSpace = textWithSpace.replace(' ', '')

file_No_Space = open('filtText.txt', 'w', encoding='utf-8')
file_No_Space.write(textWithoutSpace)
file_No_Space.close()

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def encrypt(message, key):
    encrypted = ""
    split_message = [message[i : i + len(key)] for i in range(0, len(message), len(key))]
    for each_split in split_message:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1

    return encrypted


def decrypt(cipher, key):
    decrypted = ""
    split_encrypted = [cipher[i: i + len(key)] for i in range(0, len(cipher), len(key))]
    for each_split in split_encrypted:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted


def main():
    message = input()
    key = input()
    encrypted_message = encrypt(message, key)
    decrypted_message = decrypt(encrypted_message, key)

    print("Текст: " + message)
    print("Зашифрований текст: " + encrypted_message)
    print("Розшифрований текст: " + decrypted_message)


main()

