import itertools
import math
from collections import Counter
import re 
ru_alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
# in next functions 961 = len(alphabet**2) = 31**2
def monofrequency(text):
    answer = Counter(text)
    for i in answer:
        answer[i] = answer[i] / len(text)
    return answer

def h_count(text_with_frequencies): 
    h = 0
    all_frequencies = []
    for i in text_with_frequencies:
        all_frequencies.append(text_with_frequencies[i])
    for i in all_frequencies:
        h += round(-i * math.log2(i), 3)
    return h

def bifrequency(text):
    answer = {}
    bigram_list = []
    for i in range(0, len(text) - 1, 2):
        bigram = f'{text[i] + text[i + 1]}'
        bigram_list.append(bigram)
    for i in bigram_list:
        if i not in answer:
            answer[i] = answer.setdefault(i, 0)
    for i in bigram_list:
        temp = answer.get(i)
        temp += 1
        answer.update({i: temp})
    for i in answer:
        answer[i] = answer[i] / len(bigram_list)
    answer = dict(sorted(answer.items(), key=lambda item: item[1], reverse=True))
    answer = dict(itertools.islice(answer.items(), 5))
    return answer

def letter_to_number(letter):
    res = 0
    for i in ru_alphabet:
        if i == letter:
            res = ru_alphabet.index(i) #we find letter in alphabet -> we find index 
    return res

def bigram_to_number(bigram):
    letter1 = letter_to_number(bigram[0])
    letter2 = letter_to_number(bigram[1])
    number = letter1*31 + letter2
    return number

def number_to_bigram(n):
    second = n%31 #formula was given in materials
    first = (n-second)//31
    bigram = ru_alphabet[first]+ru_alphabet[second] # add two chars
    return bigram

#print(bigram_to_number('ио'))
#print(number_to_bigram(262))

#The idea is to use Extended Euclidean algorithms that take two integers ‘a’ and ‘b’, 
#then find their gcd, and also find ‘x’ and ‘y’ such that  ax + by = gcd(a, b)
def gcdExtended(a, b):
    if a == 0:
        x = 0
        y = 1
        return (abs(b), 0, 1)
    gcd, y, x = gcdExtended(b % a, a) #recursion
    x = x - (b // a) * y
    return (gcd, x, y)
    
def modInverse(a, m):
    gcd, x, y = gcdExtended(a, m)
    if gcd != 1:
        answer = 0 #Inverse doesn't exist
    else:
        answer = ((x % m + m) % m)
    return answer

#solutions of ax = b (mod n)
def linearCongruence(a, b, n):
    a = a % n
    b = b % n
    u = 0
    v = 0
    d, u, v = gcdExtended(a, n)
    #below we have base solution cases
    if (b % d != 0):
        return [(modInverse(a, n) * b) % n] #No solution exists
    x0 = (u * (b // d)) % n #x0 
    if (x0 < 0):
        x0 += n
    results = []
    for i in range(d): # d = amount of solutions
        res = (x0 + i * (n // d)) % n #all results
        results.append(res)
    return results

def find_all_couples(top_bigrams):
    native_bigrams = ['ст', 'но', 'то', 'на', 'ен'] #top 5 bigrams from ru texts
    bigram_from_text = [x for x in top_bigrams] #our top 5 from ciphertext
    couples_1 = [] 
    couples_2 = []
    for i in native_bigrams:
        for j in bigram_from_text:
            couples_1.append([i, j]) #couples like [x*,y*],[x*,y**],[x*,y***]...[x**,y*]...
    #print(couples_1)
    for i in couples_1:
        for j in couples_1:
            if (i[0] == j[0] or i[1] == j[1]) or i == j or [j,i] in couples_2: #exclude repeated bigrams and others like them
                continue
            couples_2.append([i, j]) #get couples we need
    return couples_2

def txteditor(file_name):
    with open(file_name, 'r', encoding='utf-8') as file: #open your file -> read text -> close
        txt = file.read().lower()
        file.close()
    txt = " ".join(txt.split())
    txt = re.sub( r'[^а-яё]', '', txt)
    return txt

text = txteditor('11.txt')
top_bigrams = bifrequency(text)
#print(top_bigrams)
all_couples = find_all_couples(top_bigrams)
#print(all_couples)

def find_keys(all_couples):
    keys = []
    for i in all_couples:
        x1 = bigram_to_number(i[0][0]) #get x1,y1,x2,y2
        x2 = bigram_to_number(i[1][0])
        y1 = bigram_to_number(i[0][1])
        y2 = bigram_to_number(i[1][1])
        x = x1 - x2 
        y = y1 - y2 
        answers = linearCongruence(x, y, 961) #calculate a like in formula
        for a in answers:
            if gcdExtended(a, 31)[0] == 1:
                b = (y1 - a * x1) % 961 # calculate b like in formula
                keys.append([a, b]) #get all possible keys
    return keys

xkeys = find_keys(all_couples)
#print(xkeys)

#функція для дешифрування
def AffineDecrypt(text, keys):
    a = keys[0]
    b = keys[1]
    decrypted_text_num = []#розшифрований текст, представлений числами
    decrypted_text_t = []#розшифрований текст, преставлений вже літерами
    bigram_t = [] #список біграм витягнутих з зашифрованого тексту
    for i in range(0, len(text) - 1, 2):
        bigram = f'{text[i] + text[i + 1]}'
        bigram_t.append(bigram)
    #print(bigram_t)
    bigram_num = []#список біграм витягнутих з зашифрованого тексту, тепер представлених у вигляді чисел
    for i in range(len(bigram_t)):
        bigram_num.append(bigram_to_number(bigram_t[i]) )
    #print(bigram_num)
    for i in bigram_num: #розшифровуємо
        x = (modInverse(a, 961) * (i - b))%(961)#формула - найважливіша частина
        decrypted_text_num.append(x)
    #print(decrypted_text_num)
    #print(decrypted_text_num[0])
    for i in range(0, len(decrypted_text_num)-1): #перетворюємо числа у текст
        get_bi = number_to_bigram(decrypted_text_num[i])
        decrypted_text_t.append(get_bi)
    clear_text = ''.join(decrypted_text_t)
    return clear_text #розшифрований текст



#функція для автоматичного розпізнання змістовного тексту
def recognize(keys,text):
    for k in keys:
        txt = AffineDecrypt(text, k)
        bigram_list = [] #список усіх біграм у тексті
        for i in range(0, len(txt) - 1, 2):
            bigram = f'{txt[i] + txt[i + 1]}'
            bigram_list.append(bigram)
        #перелік заборонених біграм
        banned_bigram = ['аъ', 'аь', 'бй', 'бф', 'гщ', 'гъ', 'еъ', 'еь', 'жй', 'жц', 'жщ', 'жъ', 'жы', 'йъ', 'къ', 'лъ', 'мъ', 'оъ', 'пъ', 'ръ', 'уъ','уь', 'фщ', 'фъ', 'хы', 'хь', 'цщ', 'цъ', 'цю', 'чф', 'чц', 'чщ', 'чъ', 'чы', 'чю', 'шщ', 'шъ', 'шы', 'шю', 'щг', 'щж','щл', 'щх', 'щц', 'щч', 'щш', 'щъ', 'щы', 'щю', 'щя', 'ъа', 'ъб', 'ъг', 'ъд', 'ъз', 'ъй', 'ък', 'ъл', 'ън', 'ъо', 'ъп', 'ър','ъс', 'ът', 'ъу', 'ъф', 'ъх', 'ъц', 'ъч', 'ъш', 'ъщ', 'ъъ', 'ъы', 'ъь', 'ъэ', 'ыъ', 'ыь', 'ьъ', 'ьы', 'эа', 'эж', 'эи', 'эо','эу', 'эщ', 'эъ', 'эы', 'эь', 'эю', 'эя', 'юъ', 'юы', 'юь', 'яъ', 'яы', 'яь', 'ьь', 'гг']
        get_freq = monofrequency(txt)
        get_bifreq = list(bifrequency(txt)) #most frequent bigrams in ouput text
        h = h_count(get_freq) #ентропія
        #print(bigram_list)
        for bigram in bigram_list:
            if bigram not in banned_bigram: #if not in ban list
                if get_bifreq[0] in ['ст', 'но', 'то'] and (h >= 4.3 and h < 4.5): # <=4.45 doesn't feet
                    return k #if the most frequent bigram is among top 3 common bigrams and entropy between 4.3 and 4.5(the standart value 4.35)
    return "Not found (ㆆ_ㆆ)"


true_keys = recognize(xkeys, text)
print('----Your key (ɔ◔‿◔)ɔ', true_keys)
print('----Your text ⇩')
final = AffineDecrypt(text, true_keys)
print(final)