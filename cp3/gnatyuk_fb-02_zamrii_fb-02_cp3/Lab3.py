import re
import itertools
import collections


Encr_text = open('V7.txt', 'r', encoding='utf-8')
text_with_spaces = Encr_text.read()
text_with_spaces = text_with_spaces.lower()
text_with_spaces = re.sub(r"[\W\d]", " ", text_with_spaces)
text_with_spaces = re.sub(r"[A-Za-z]", " ", text_with_spaces)
text_no_space = text_with_spaces.replace(" ", "")

def LetterToNumber(letter):
    num = ord(letter) - 1072
    if (letter >= 'ъ'):
        num -= 1
    return num

def NumberToLetter(num):
    if (num >= 26): 
        num += 1
    letter = chr(num + 1072)
    return letter

def GCD(num, mod):
    if num == 0:
        MOD = (mod, 0, 1)
        return MOD
    else:
        x, y, z = GCD(mod % num, num)
        XYZ = (x, z - (mod // num) * y, y)
        return XYZ

def Converse(num, mod):
    x, y, z = GCD(num, mod)
    reverse = (y % mod + mod) % mod
    return reverse

def BigramToNumber(bigram):
    num_bigram = LetterToNumber(bigram[0]) * 31 + LetterToNumber(bigram[1])
    return num_bigram

def NumberToBigram(num):
    num_to_bigram = NumberToLetter(num // 31) + NumberToLetter(num % 31)
    return num_to_bigram

def FindTextBigram(text):
    x = re.findall('..', text)
    return x

def Frequence(text):
    c = collections.Counter(text)
    return dict(c.most_common())
print('_'*300)
print('Freq:', (Frequence(text_no_space)))
print('_'*300)

def Decr_text(encr_text, a, b):
    decr = ""
    for i in FindTextBigram(encr_text):
        x = (Converse(a, pow(31, 2)) * (BigramToNumber(i) - b)) % (pow(31, 2))
        decr += NumberToBigram(x)
    return decr

def Prime_5(bigrams):
    lst = list(Frequence(bigrams))
    list_prime_5 = lst[0:5:1]
    print('The most frequent bigrams:', list_prime_5 )
    return list_prime_5

def Meaningfulness(encr_text):
    LEN = len(encr_text)
    fr_o = (encr_text.count('о') / LEN)
    fr_a = (encr_text.count('а') / LEN)
    if fr_o < 0.10 or fr_a < 0.07:
        return False
    else:
        return True

def Decision(x, y, mod):
    a = (Converse(x, mod) * y) % mod
    return a

def Afine_cipher(text):
    list1 = [545, 417, 572, 403, 168]  #---> ['ст', 'но', 'то', 'на', 'ен']
    prime5_encr_text = []
    for i in Prime_5(FindTextBigram(text)):
        prime5_encr_text.append(BigramToNumber(i))
    for y in list(itertools.combinations(prime5_encr_text, 2)):
        y1 = (y[0] - y[1]) % (pow(31, 2))
        for x in list(itertools.combinations(list1, 2)):
            x1 = (x[0] - x[1]) % (pow(31, 2))
            a = Decision(x1, y1, pow(31, 2))
            if a != -1:
                b = (y[0] - a * x[0]) % (pow(31, 2))
                if (Meaningfulness(Decr_text(text, a, b)) == True):
                    return [a, b]

Key = Afine_cipher(text_no_space)
print('Encrypt text:', text_no_space)
print('_'*300)
print('Key: а = ', str(Key[0]))
print('Key: b = ', str(Key[1]))
print('_' * 300)
print('Decrypt text:', Decr_text(text_no_space, Key[0], Key[1]))
print('_' * 300)

