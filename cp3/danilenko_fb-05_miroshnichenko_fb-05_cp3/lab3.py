from math import gcd

ALPHA = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
BI_GRAMS_TOP = ('ст', 'но', 'то', 'на', 'ен')

text_13 = open("13.txt", 'r').read()


def extended_euclid(first_num: int, second_num: int) -> (int, int, int):
    if second_num == 0:
        return first_num, 1, 0
    d, x, y = extended_euclid(second_num, first_num % second_num)
    return d, y, x - (first_num // second_num) * y


def inverse_mod(first_num: int, second_num: int) -> int:
    k = extended_euclid(first_num, second_num)[1]
    return k


def solve_linear_comparison(first_num, second_num, mod) -> list:
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
    total_count = 0
    ngram_dict = {}

    counter = 1
    target_text = list(target_text)
    for ne_i_6 in range(len(target_text))[1:]:
        if counter % 2 == 0:
            current_gram = str(target_text[ne_i_6-1]) + str(target_text[ne_i_6])
            if current_gram in ngram_dict:
                ngram_dict[current_gram] += 1
                total_count += 1
            else:
                ngram_dict[current_gram] = 1
                total_count += 1
        counter += 1
    for ngram in ngram_dict:
        ngram_dict[ngram] = round(ngram_dict[ngram]/total_count, 6)

    bi_grams_sort = {}

    bi_grams_keys = sorted(ngram_dict, key=ngram_dict.get)

    for num in bi_grams_keys:
        bi_grams_sort[num] = ngram_dict[num]

    sorted_bigramms = dict(reversed(list(bi_grams_sort.items())))

    return list(sorted_bigramms)[:5]
