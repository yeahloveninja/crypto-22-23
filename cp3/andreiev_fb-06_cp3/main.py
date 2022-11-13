import re
from itertools import permutations

def ext_gcd(a, b):
    if a == 0:
        x = 0
        y = 1
        return (b, x, y)
    else:
        gcd, y, x = ext_gcd(b % a, a)
        x = x - (b // a) * y
        return (gcd, x, y)

def inverse_mod(a, m):
    gcd, x, y = ext_gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        print("Inverse doesn't exist")
        return

# ax = b mod n 
def solve_mod_eq(a, b, n):
    d = ext_gcd(a, n)[0]
    if d == 1:
        return (inverse_mod(a, n) * b) % n
    elif d > 1:
        if b % d != 0:
            return 
        else:
            a, b, n = a // d, b // d, n // d
            root = solve_mod_eq(a, b, n)
            return [root + (i * n) for i in range(d)]



def filter_text(text):
    text = re.sub(r'[^а-яА-Я ]', '', text).lower().replace(" ", "").replace("ё", "е").replace("ъ", "ь")
    return text

with open("given_ct.txt", "r") as f:
    text = f.read()

text = filter_text(text)

def get_top_bigrams(text):
    block_bigrams = [text[i:i+2] for i in range(0, len(text), 2)]
    bigram_stats = {}
    for i in block_bigrams:
        bigram_stats[i] = block_bigrams.count(i)

    bigram_stats = {k: v for k, v in sorted(bigram_stats.items(), key=lambda item: item[1], reverse=True)}
    top_bigrams = list(bigram_stats.keys())[:5]
    return top_bigrams

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']

def bigrams_to_nums(bigrams):
    return [alphabet.index(i[0]) * len(alphabet) + alphabet.index(i[1]) for i in bigrams]

def combinations(text):
    possible_keys = []
    top_theory_nums = bigrams_to_nums(['ст', 'но', 'ен', 'то', 'на'])
    top_ciphertext_nums = bigrams_to_nums(get_top_bigrams(text))
    theory_combinations_nums = list(permutations(top_theory_nums, 2))
    ciphertext_combinations_nums = list(permutations(top_ciphertext_nums, 2))

    for i in range(len(top_theory_nums)):
        y_star_minus_y_double_star = (theory_combinations_nums[i][0] - theory_combinations_nums[i][1]) % len(alphabet) ** 2
        x_star_minus_x_double_star = (ciphertext_combinations_nums[i][0] - ciphertext_combinations_nums[i][0]) % len(alphabet) ** 2

        a = solve_mod_eq(y_star_minus_y_double_star, x_star_minus_x_double_star, len(alphabet) ** 2)
        b = (ciphertext_combinations_nums[i][0] - a * theory_combinations_nums[i][0]) % len(alphabet) ** 2
        possible_keys.append((a, b))
    return possible_keys



def affine_decrypt(ciphertext, key):
    open_text = ""
    a, b = key[0], key[1]
    block_bigrams_nums = bigrams_to_nums([ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)])
    for i in block_bigrams_nums:
        bigram_num = re(a, len(alphabet) ** 2) * (i - b) % len(alphabet) ** 2
        char1 = bigram_num // len(alphabet)
        char2 = bigram_num % len(alphabet)
        open_text += char1
        open_text += char2
    return open_text







     


