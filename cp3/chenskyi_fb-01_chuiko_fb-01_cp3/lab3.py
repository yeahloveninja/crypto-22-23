import io
from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
ru_bigrams = ['ст','но','то','на','ен']

with io.open("07.txt", encoding='utf-8') as file:
    text = file.read()
    text = text.replace("\n", "")

#----------------------------#
def bigrams(text): #Найчастіші біграми
    bigrams = []
    for j in range(0, len(text) - 2, 2):
        bigrams.append(text[j:j + 2])
    sorted_bigram_dict = sorted(Counter(bigrams).items(), key=lambda x: x[1], reverse=True)
    # сортуємо значення елементів словаря за спаданням, на виході отримуємо двовимірний список
    print("[+] 5 найчастіших біграм: ", sorted_bigram_dict[0:5])
    # створюємо список лише з біграмами
    top_bigrams = []
    for i in range(5):
        top_bigrams.append(sorted_bigram_dict[i][0])
    return top_bigrams

def possible_pairs(ru_list, top_list):
    pairs = []
    for x1 in ru_list:
        for y1 in top_list:
            for x2 in ru_list:
                if x2 != x1:
                    for y2 in top_list:
                        if y2 != y1:
                            pairs.append([[x1, y1], [x2, y2]]) # у1, х1, х2, у2,
    return pairs

def ExtendedEuclid(a, b): # b = mod
    # x — обернене щодо a за модулем b, y — обернене щодо b за модулем a. (ax+by=gcd(a,b))
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = ExtendedEuclid(b % a, a)
    x = y1 - (b//a) * x1
    y = x1
    return gcd, x, y

def Equation(a, b, mod = len(alphabet)):
    gcd, a0, y = ExtendedEuclid(a, mod) # a0 - обернене до а за модулем mod
    result = []
    if gcd == 1 and ((a * a0) % mod) == 1:
        result.append((a0 * b) % mod)
        return result
    elif b % gcd == 0:
        _, a1, _ = ExtendedEuclid(a/gcd, mod/gcd)
        x1 = (a1 * b / gcd) % (mod / gcd)
        for i in range(gcd):
            result.append(x1 + i * mod / gcd)
        return result
    else:
        return None

def find_keys(text):  # ймовірні ключі
    keys_list = []
    top_bigr = bigrams(text)
    pairs_of_bigrams = possible_pairs(ru_bigrams, top_bigr)
    for bigram in pairs_of_bigrams:
        keys = []
        x1 = getIndex(bigram[0][0])
        x2 = getIndex(bigram[1][0])
        y1 = getIndex(bigram[0][1])
        y2 = getIndex(bigram[1][1])
        res = Equation(x1 - x2, y1 - y2,  len(alphabet)**2)  # рівняння (2) з методички
        if res is not None:
            for a in res:
                gcd, a0, y = ExtendedEuclid(a,  len(alphabet))
                if gcd != 1:
                    continue
                b = (y1 - a * x1) % len(alphabet)**2  # відповідно знаючи a знаходимо відповідне b
                keys.append((int(a), int(b)))  # отримуємо пари а, b
        if len(keys) != 0:
            for j in range(len(keys)):
                if keys[j] not in keys_list:
                    keys_list.append(keys[j])
    return keys_list

def getIndex(bigram):
    index = alphabet.index(bigram[0])*31 + alphabet.index(bigram[1])
    return index

def getBigram(index):
    bigram = alphabet[(index - index % 31)//31] + alphabet[index % 31]
    return bigram

def decrypt(text, a, b ):
    dec_text = ""
    text_bigrams = []
    gcd, a1, y = ExtendedEuclid(a, len(alphabet)**2)
    for i in range(0, len(text) - 2, 2):
        text_bigrams.append(text[i] + text[i + 1])
    for bigram in text_bigrams:
        X = (a1 * (getIndex(bigram) - b)) % len(alphabet)**2
        dec_text = dec_text + getBigram(X)
    return dec_text

def check(text):
    exception_bigrams = ['аъ', 'аь', 'бй', 'бф', 'гщ', 'гъ', 'еъ', 'еь', 'жй', 'жц', 'жщ', 'жъ', 'жы', 'йъ', 'къ', 'лъ', 'мъ', 'оъ', 'пъ', 'ръ', 'уъ', 'уь', 'фщ', 'фъ', 'хы', 'хь', 'цщ', 'цъ', 'цю', 'чф', 'чц', 'чщ', 'чъ', 'чы', 'чю', 'шщ', 'шъ', 'шы', 'шю', 'щг', 'щж', 'щл', 'щх', 'щц', 'щч', 'щш', 'щъ', 'щы', 'щю', 'щя', 'ъа', 'ъб', 'ъг', 'ъд', 'ъз', 'ъй', 'ък', 'ъл', 'ън', 'ъо', 'ъп', 'ър', 'ъс', 'ът', 'ъу', 'ъф', 'ъх', 'ъц', 'ъч', 'ъш', 'ъщ', 'ъъ', 'ъы', 'ъь', 'ъэ', 'ыъ', 'ыь', 'ьъ', 'ьы', 'эа', 'эж', 'эи', 'эо', 'эу', 'эщ', 'эъ', 'эы', 'эь', 'эю', 'эя', 'юъ', 'юы', 'юь', 'яъ', 'яы', 'яь', 'ьь']
    bigrams = []
    for j in range(0, len(text) - 1, 1):
        bigrams.append(text[j] + text[j + 1])
    for bigram in exception_bigrams:
        if bigram in bigrams:
            return False
    return True
#-----------------------------#
keys = find_keys(text)
print("[+] можливі ключі:", keys)
for key in keys:
    dec_text = decrypt(text, key[0], key[1])
    if check(dec_text):
        print("[+] вірний ключ:",key)
        print("[+] шифртекст:", text)
        print("[+] відкритий текст:", decrypt(text, key[0], key[1]))
        f = open('dec_07.txt', 'w', encoding='utf-8')
        f.write(dec_text)
        f.close()
