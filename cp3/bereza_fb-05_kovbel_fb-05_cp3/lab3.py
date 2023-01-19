import re
import collections
import itertools

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
popularBigrams = ['ст', 'но', 'то', 'на', 'ен']

#find top 5 bigrams
def bigrams(text):
    bigrams = []
    for j in range(len(text) - 1):
        bigrams.append(text[j:j + 2])
    counter = collections.Counter(bigrams)
    sorted_bigrams = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    print(f"Top 5 bigrams in this text: {sorted_bigrams[:5]}\n---\n")
    return [bigram[0] for bigram in sorted_bigrams[:5]]


def possible_pairs(ru_list, top_list):
    # Using python's built-in itertools.product function to generate all possible pairs
    pairs = list(itertools.product(ru_list, top_list))
    # Using python's built-in combinations function to generate all possible pair combinations
    pairs = list(itertools.combinations(pairs, 2))
    return pairs

def ExtendedEuclid(a, b):
    """
    Calculates the inverse element modulo using the extended Euclid algorithm.
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def Equation(a, b, mod = len(alphabet)):
    gcd, a0, y = ExtendedEuclid(a, mod)
    if gcd == 1 and ((a * a0) % mod) == 1:
        return [int((a0 * b) % mod)]
    elif b % gcd == 0:
        _, a1, _ = ExtendedEuclid(a/gcd, mod/gcd)
        x1 = (a1 * b / gcd) % (mod / gcd)
        result = []
        for i in range(gcd):
            result.append(x1 + i * mod / gcd)
        return result
    else:
        return None


def find_keys(text):
    keys_list = []
    top_bigrams = bigrams(text)
    pairs_of_bigrams = possible_pairs(popularBigrams, top_bigrams)
    for bigram in pairs_of_bigrams:
        keys = []
        x1, y1 = get_index(bigram[0][0]), get_index(bigram[0][1])
        x2, y2 = get_index(bigram[1][0]), get_index(bigram[1][1])
        res = Equation(x1 - x2, y1 - y2,  len(alphabet)**2)
        if res is not None:
            for a in res:
                b = (y1 - a * x1) % len(alphabet)**2
                keys.append((int(a), int(b)))
        keys_list.extend(keys)
    keys_list = list(set(keys_list))
    return keys_list

def get_index(bigram):
    index = alphabet.index(bigram[0])*len(alphabet) + alphabet.index(bigram[1])
    return index

def get_bigram(index):
    first_letter_index = (index - index % len(alphabet))//len(alphabet)
    second_letter_index = index % len(alphabet)
    bigram = alphabet[first_letter_index] + alphabet[second_letter_index]
    return bigram

def decrypt(text, a, b ):
    dec_text = ""
    text_bigrams = [text[i:i+2] for i in range(0, len(text) - 2, 2)]
    a1 = ExtendedEuclid(a, len(alphabet)**2)[1]
    for bigram in text_bigrams:
        X = (a1 * (get_index(bigram) - b)) % len(alphabet)**2
        dec_text += get_bigram(X)
    return dec_text

def check_text(text):
    exception_bigrams = ['аъ', 'аь', 'бй', 'бф', 'гщ', 'гъ', 'еъ', 'еь', 'жй', 'жц', 'жщ', 'жъ', 'жы', 'йъ', 'къ', 'лъ', 'мъ', 'оъ', 'пъ', 'ръ', 'уъ', 'уь', 'фщ', 'фъ', 'хы', 'хь', 'цщ', 'цъ', 'цю', 'чф', 'чц', 'чщ', 'чъ', 'чы', 'чю', 'шщ', 'шъ', 'шы', 'шю', 'щг', 'щж', 'щл', 'щх', 'щц', 'щч', 'щш', 'щъ', 'щы', 'щю', 'щя', 'ъа', 'ъб', 'ъг', 'ъд', 'ъз', 'ъй', 'ък', 'ъл', 'ън', 'ъо', 'ъп', 'ър', 'ъс', 'ът', 'ъу', 'ъф', 'ъх', 'ъц', 'ъч', 'ъш', 'ъщ', 'ъъ', 'ъы', 'ъь', 'ъэ', 'ыъ', 'ыь', 'ьъ', 'ьы', 'эа', 'эж', 'эи', 'эо', 'эу', 'эщ', 'эъ', 'эы', 'эь', 'эю', 'эя', 'юъ', 'юы', 'юь', 'яъ', 'яы', 'яь', 'ьь']
    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, 1)]
    for bigram in exception_bigrams:
        if bigram in bigrams:
            return False
    return True

def check_string(string):
    pattern = r"(\w)\1{4,}"
    match = re.search(pattern, string)
    if match:
        return True
    else:
        return False

text = open("4.txt", encoding='utf-8').read().replace('\n', '')
keys = find_keys(text)
print(f"List of possible keys: {keys}Processing\n")
for key in keys:
    dec_text = decrypt(text, key[0], key[1])
    if check_text(dec_text):
        if check_string(dec_text) is not True:
            print("Result for key", key)
            print(f"Decoded text: {dec_text}\n")
