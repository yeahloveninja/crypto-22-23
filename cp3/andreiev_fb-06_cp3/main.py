import re

def ext_gcd(a, b):
    if a == 0:
        x = 0
        y = 1
        return (abs(b), x, y)
    else:
        gcd, y, x = ext_gcd(b % a, a)
        x = x - (b // a) * y
        return (gcd, x, y)


def inverse_mod(a, m):
    gcd, x, y = ext_gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        return 0


# ax = b mod n 
def solve_mod_eq(a, b, n):
    d = ext_gcd(a, n)[0]
    if d == 1:
        return [(inverse_mod(a, n) * b) % n]
    elif d > 1:
        if b % d != 0:
            return []
        else:
            a, b, n = a // d, b // d, n // d
            root = solve_mod_eq(a, b, n)
            return [root[0] + (i * n) for i in range(d)]


def filter_text(text):
    text = re.sub(r'[^а-яА-Я ]', '', text).lower().replace(" ", "").replace("ё", "е").replace("ъ", "ь")
    return text


def get_top_bigrams(text):
    block_bigrams = [text[i:i+2] for i in range(0, len(text), 2)]
    bigram_stats = {}
    for i in block_bigrams:
        bigram_stats[i] = block_bigrams.count(i)

    bigram_stats = {k: v for k, v in sorted(bigram_stats.items(), key=lambda item: item[1], reverse=True)}
    top_bigrams = list(bigram_stats.keys())[:5]
    return top_bigrams


def bigrams_to_nums(bigrams):
    return [alphabet.index(i[0]) * len(alphabet) + alphabet.index(i[1]) for i in bigrams]

def get_possible_keys(text):
    possible_keys = []
    top_theory_nums = bigrams_to_nums(['ст', 'но', 'ен', 'то', 'на'])
    top_ciphertext_nums = bigrams_to_nums(get_top_bigrams(text))
    combs = []
    for i in top_theory_nums:
        for j in top_ciphertext_nums:
            combs.append((i, j))
    possible_keys = []
    for i in combs:
        for j in combs:
            if i == j or (i[0] == j[0] or i[1] == j[1]):
                continue
            else:
                possible_keys.append((i, j))
    final_keys = []


    for i in possible_keys:
        x = i[0][0] - i[1][0]
        y = i[0][1] - i[1][1]
        roots = solve_mod_eq(x, y, len(alphabet) ** 2)
        for j in roots:
            if ext_gcd(j, 31)[0] == 1:
                b = (i[0][1] - j * i[0][0]) % (len(alphabet) ** 2)
                final_keys.append((j, b))
    return final_keys


def affine_decrypt(ciphertext, key):
    open_text = ""
    a, b = key[0], key[1]
    block_bigrams_nums = bigrams_to_nums([ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)])
    for i in block_bigrams_nums:
        bigram_num = (inverse_mod(a, len(alphabet) ** 2) * (i - b)) % len(alphabet) ** 2
        char1 = bigram_num // len(alphabet)
        char2 = bigram_num % len(alphabet)
        open_text += alphabet[char1]
        open_text += alphabet[char2]
    return open_text
    

def text_detector(open_text):
    is_text_flag = True
    # підрахунок символів (найчастіші символи)
    char_counter = {}

    for char in filter_text(open_text):
        char_counter.setdefault(char, 0)
        char_counter[char] += 1

    char_counter = dict(sorted(char_counter.items(), key=lambda x: x[1], reverse=True))
    if list(char_counter.keys())[0] != "о" and list(char_counter.keys())[0] != "e":
        is_text_flag = False

    # індекс відповідності
    index = 0
    for i in range(len(alphabet)):
        char_count = open_text.count(alphabet[i])
        index += char_count * (char_count - 1)
    index = index / (len(open_text) * (len(open_text) - 1))

    if not (index > 0.05 and index < 0.06):
        is_text_flag = False

    return is_text_flag

    
def check_keys(ciphertext, possible_keys):
    final_keys = []
    for key in possible_keys:
        open_text = affine_decrypt(ciphertext, key)
        flag = text_detector(open_text)
        if (flag is True) and (key not in final_keys):
            final_keys.append(key)
    return final_keys


alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

with open("given_ct.txt", "r") as f:
    text = f.read()

text = filter_text(text)

# [(654, 777)]
checked_keys = check_keys(text, get_possible_keys(text))
print(checked_keys)
open_text = affine_decrypt(text, checked_keys[0])
print(open_text[:100])
# with open("open_text.txt", "w") as w:
#     w.write(open_text)

