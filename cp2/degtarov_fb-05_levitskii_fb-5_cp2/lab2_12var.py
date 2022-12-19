import re
import collections

def text_check(textfile):
    file = open(textfile, encoding = 'utf=8')
    text = file.read()
    file.close()
    cleartext = re.sub(r'[^а-яА-Я]', '', text).replace("ё", "е").lower()
    return cleartext


alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
keyList = ['иб', 'бир', 'мало', 'ламар', 'нйсшафгфюр', 'дбйвьфпсшат', 'югэжулщэбтйа', 'ццбкьуяаккялн',
           'фърсмнлшиэхйфы', 'ьщбкэьзньфбгспн', 'ывыбувхпцечгулбь', 'дечдаифсюфгоьочьь', 'жйжвфтвндтззвяздба',
           'офыюпачжржзупуажяки', 'гйпзявэаязщлпдямонсх']

textEx1 = text_check("textEx1.txt")
textEx2 = text_check("text_to_decrypt.txt")

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def encrypt(text, key):
    encrypted = ""
    split_message = [text[i : i + len(key)] for i in range(0, len(text), len(key))]
    for each_split in split_message:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1

    return encrypted


def decrypt(cipher, key):
    decrypted = ""
    split_encrypted = [cipher[i : i + len(key)] for i in range(0, len(cipher), len(key))]

    for each_split in split_encrypted:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1
    return decrypted

def coincidenceIndex(text):
    IndexResult = 0
    length = len(text)
    for i in range(len(alphabet)):
        letterFreq = text.count(alphabet[i])
        IndexResult += letterFreq * (letterFreq - 1)
    IndexResult *= 1/(length*(length-1))
    return IndexResult

def frequencies(text):
    c = collections.Counter(text)
    freq = {i:c[i]/len(text)  for i in c}
    return freq

def most_frequent(text):
    freq=frequencies(text)
    for key, value in freq.items():
        if value == max(freq.values()):
            return key

def generate_key(txt, key_len):
    rus_frequent=['о', 'а', 'е', 'и', 'н', 'т', 'р', 'с']
    rflen = len(rus_frequent)
    key=''
    for n in range(rflen):
        for i in range(key_len):
            blockMostFr = most_frequent([txt[k] for k in range(i, len(txt), key_len)])
            key+=alphabet[(alphabet.index(blockMostFr)-alphabet.index(rus_frequent[n])+len(alphabet))%len(alphabet)] # формула k=(y* +x* )modm
            if len(key) == key_len:
                print(key)
                answer = input("Ключ підходить? ")
                if answer == "Yes":
                    return key
                else:
                    key = ""
                    continue

def blocksSplit(text, length):
    blocks = []
    for i in range(length):
        blocks.append(text[i::length])
    return blocks

def blocksIndex(text, size):
    blocks = blocksSplit(text, size)
    index = 0
    for i in range(len(blocks)):
        index = index + coincidenceIndex(blocks[i])
    index = index/len(blocks)
    return index

def main():
    print("Індекс збігу ВТ = ", coincidenceIndex(textEx1))
    for key in keyList:
        print("Довжина ключа = ", len(key))
        encryptedText = encrypt(textEx1, key)
        print("Закодований текст: ", encryptedText)
        print("Розшифрований текст: ", decrypt(encryptedText, key))
        print("Індекс збігу: ", coincidenceIndex(encryptedText), "\n")
    for i in range(1, len(alphabet)):
        print('Довжина ключа=' + str(i) + ' Індекс збігу=' + str(blocksIndex(textEx2, i)))
    print("Згенерований ключ: ", generate_key(textEx2, 14))
    decrypted_text = decrypt(textEx2, "чугунныенебеса")
    f=open(f'decrypted_text.txt','w',encoding='UTF-8')
    f.write(decrypted_text)
    f.close()

main()
