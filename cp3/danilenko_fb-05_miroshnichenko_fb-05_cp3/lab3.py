from math import gcd

ALPHA = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
BI_GRAMS_TOP = ['ст', 'но', 'то', 'на', 'ен']


def extended_euclid(first_num: int, second_num: int) -> (int, int, int):
    if second_num == 0:
        return first_num, 1, 0
    d, x, y = extended_euclid(second_num, first_num % second_num)
    return d, y, x - (first_num // second_num) * y


def inverse_mod(first_num: int, second_num: int) -> int:
    return extended_euclid(first_num, second_num)[1]


def solve_linear_comparison(first_num: int, second_num: int, mod: int) -> list:
    roots = []
    d = gcd(first_num, mod)
    if d == 1:
        roots.append((inverse_mod(first_num, mod) * second_num) % mod)
    else:
        if (second_num % d) == 0:
            result = (inverse_mod(int(first_num / d) * int(second_num / d), int(mod / d))) % int(mod / d)
            for ne_i_8 in range(d):
                roots.append(result + ne_i_8 * int(mod / d))
        else:
            roots.append(-1)
    return roots


def find_ngram(target_text: str) -> list:
    total_count = 0
    ngram_dict = {}
    counter = 1
    target_text = list(target_text)
    dictionary_bi_gram_sort = {}
    for ne_i_7 in range(len(target_text)):
        if counter % 2 == 0:
            current_gram = str(target_text[ne_i_7-1]) + str(target_text[ne_i_7])
            if current_gram in ngram_dict:
                ngram_dict[current_gram] += 1
                total_count += 1
            else:
                ngram_dict[current_gram] = 1
                total_count += 1
        counter += 1
    for ngram in ngram_dict:
        ngram_dict[ngram] = round(ngram_dict[ngram]/total_count, 6)

    keys_sort = sorted(ngram_dict, key=ngram_dict.get)
    for ne_i_7 in keys_sort:
        dictionary_bi_gram_sort[ne_i_7] = ngram_dict[ne_i_7]

    sorted_bi_gram = list(reversed(list(dictionary_bi_gram_sort.keys())))
    return sorted_bi_gram[:5]


def bi_gram_to_num(bi_gram: str) -> int:
    bi_gram_list = list(bi_gram)
    return ALPHA.index(bi_gram_list[0])*31 + ALPHA.index(bi_gram_list[1])


def num_to_bi_gram(num: int) -> str:
    first_letter = num % 31
    second_letter = (num-first_letter) // 31
    return ALPHA[second_letter] + ALPHA[first_letter]


def decrypt(text: str, first_key: int, second_key: int) -> str:
    inverse_a = inverse_mod(first_key, 961)
    clear_text = []
    bi_grams_list = []
    for ne_i_8 in range(0, len(text) - 2, 2):
        bi_grams_list.append(text[ne_i_8] + text[ne_i_8 + 1])
    for ne_i_8 in bi_grams_list:
        current = (inverse_a * (bi_gram_to_num(ne_i_8) - second_key)) % 961
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


if __name__ == '__main__':
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
                first_x = bi_gram_to_num(BI_GRAMS_TOP[j])
                second_x = bi_gram_to_num(BI_GRAMS_TOP[n])
                first_y = bi_gram_to_num(current_bi_grams[i])
                second_y = bi_gram_to_num(current_bi_grams[i+1])
                answers = solve_linear_comparison((first_x - second_x), (first_y - second_y), 31 * 31)
                for answer in answers:
                    if answer != -1:
                        key = (answer, ((first_y - answer * first_x) % (31 * 31)))
                        keys.append(key)

    for k in keys:
        final_text = decrypt(file_text, k[0], k[1])
        if check(final_text):
            print(final_text)
            break
