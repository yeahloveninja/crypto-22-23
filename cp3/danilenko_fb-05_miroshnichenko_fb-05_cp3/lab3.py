from math import gcd

ALPHA = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
BI_GRAMS_TOP = ['ст', 'но', 'то', 'на', 'ен']


def extended_euclid(first_num: int, second_num: int) -> (int, int, int):
    if second_num == 0:
        return first_num, 1, 0
    d, x, y = extended_euclid(second_num, first_num % second_num)
    return d, y, x - (first_num // second_num) * y


def inverse_mod(first_num: int, second_num: int) -> int:
    k = extended_euclid(first_num, second_num)[1]
    return k


def solve_linear_comparison(first_num: int, second_num: int, mod: int) -> list:
    roots = []
    d = gcd(first_num, mod)
    if d == 1:
        roots.append((inverse_mod(first_num, mod) * second_num) % mod)
    else:
        if (second_num % d) == 0:
            result = (inverse_mod(int(first_num / d) * int(second_num / d), int(mod / d))) % int(mod / d)
            for i in range(d):
                roots.append(result + i * int(mod / d))
        else:
            roots.append(-1)
    return roots


def find_ngram(target_text: str):
    full_list = []
    for i in range(0, len(target_text) - 2, 2):
        full_list.append(target_text[i] + target_text[i + 1])
    bi_grams_dict = {}
    for i in all_bi_grams:
        bi_grams_dict[i] = full_list.count(i)/(2 * len(full_list))
    final = []
    sorted_bi_grams = list(sorted(bi_grams_dict.items(), key=lambda item: item[1], reverse=True))
    for i in range(5):
        final.append(sorted_bi_grams[i][0])
    return final


def bi_gram_to_num(bi_gram: str) -> int:
    bi_gram_list = list(bi_gram)
    num = ALPHA.index(bi_gram_list[0])*31 + ALPHA.index(bi_gram_list[1])
    return num


def num_to_bi_gram(num: int) -> str:
    first_letter = num % 31
    second_letter = (num-first_letter) // 31
    return ALPHA[second_letter] + ALPHA[first_letter]


def decrypt(text: str, first_key: int, second_key: int) -> str:
    a1 = inverse_mod(first_key, 961)
    clear_text = []
    bi_grams_list = []
    for i in range(0, len(text) - 2, 2):
        bi_grams_list.append(text[i] + text[i + 1])
    for i in bi_grams_list:
        current = (a1 * (bi_gram_to_num(i) - second_key)) % 961
        clear_text.append(num_to_bi_gram(current))
    return ''.join(clear_text)


def check(text):
    letters_dict = {
        'о': 0.07,
        'е': 0.06,
        'а': 0.06,
    }
    let_count = 0
    for _ in text:
        let_count += 1
    for letter in list(letters_dict.keys()):
        counter = 0
        for current_letter in text:
            if letter == current_letter:
                counter += 1
        if counter/let_count < letters_dict[letter]:
            return False
    return True


all_bi_grams = []
for i in ALPHA:
    for j in ALPHA:
        all_bi_grams.append(i+j)

with open('13.txt', 'r') as f:
    file_text = f.read()
    file_text = file_text.replace("\n", "")

current_bi_grams = find_ngram(file_text)
keys = []
for i in range(0, 4):
    for j in range(0, 5):
        for n in range(0, 5):
            if n == j:
                continue
            X1 = bi_gram_to_num(BI_GRAMS_TOP[j])
            X2 = bi_gram_to_num(BI_GRAMS_TOP[n])
            Y1 = bi_gram_to_num(current_bi_grams[i])
            Y2 = bi_gram_to_num(current_bi_grams[i+1])
            a = solve_linear_comparison((X1 - X2), (Y1 - Y2), 961)
            for f in a:
                if f != -1:
                    k = (f, ((Y1 - f*X1) % (31*31)))
                    keys.append(k)


result = ''
for k in keys:
    final_text = decrypt(file_text, k[0], k[1])
    if check(final_text):
        result = final_text

print(result)
