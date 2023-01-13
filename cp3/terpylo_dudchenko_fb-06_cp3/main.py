import re
from collections import Counter

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
most_common_bigrams = ['ст', 'но', 'ен', 'то', 'на']
nonexistent_bigrams = ['аы', 'аь', 'бй', 'бф', 'бц', 'вй', 'гы', 'гй', 'гф', 'гц', 'гщ', 'гь', 'гю', 'дй', 'дщ', 'еы',
                       'еь', 'эа', 'эб', 'эе', 'эж', 'эз', 'эи', 'эы', 'эн', 'эо', 'эр', 'эс', 'эу', 'эц', 'эч', 'эщ',
                       'эь', 'эю', 'эя', 'жы', 'жй', 'жф', 'жц', 'жш', 'жщ', 'жю', 'зй', 'зщ', 'иы', 'иь', 'ыы', 'ыь',
                       'йы', 'йй', 'йь', 'кы', 'кй', 'лй', 'лщ', 'мй', 'мю', 'нй', 'оы', 'оь', 'пг', 'пд', 'пэ', 'пж',
                       'пй', 'пф', 'пх', 'рэ', 'рй', 'сй', 'сщ', 'тй', 'тщ', 'уы', 'уь', 'фг', 'фэ', 'фж', 'фз', 'фй',
                       'фк', 'фп', 'фс', 'фх', 'фц', 'фч', 'фш', 'фщ', 'фю', 'хы', 'хй', 'хц', 'хь', 'хю', 'цй', 'цф',
                       'цц', 'цш', 'цщ', 'ць', 'цю', 'чы', 'чй', 'чф', 'чц', 'чщ', 'чю', 'шэ', 'шж', 'шз', 'шы', 'шй',
                       'шф', 'шц', 'шч', 'шш', 'шщ', 'шю', 'шя', 'щб', 'щв', 'щг', 'щж', 'щз', 'щы', 'щй', 'щк', 'щл',
                       'щм', 'щт', 'щф', 'щх', 'щц', 'щч', 'щш', 'щщ', 'щю', 'ьы', 'ьь', 'юы', 'юй', 'юь', 'яы', 'яь']



def read_file(text_path):
    plain_text = open(text_path, encoding='utf-8')
    pt = plain_text.read()
    plain_text.close()
    pt = pt.replace("\n", "")
    pt = re.sub(r'[^а-яА-Я ]', '', pt).lower().replace(" ", "").replace("ё", "е").replace("ъ", "ь")
    return pt


def find_gcd(a, n):
    return abs(a) if n == 0 else find_gcd(n, a % n)


def find_inverse_modulo(a, n):
    for x in range(1, n):
        if ((a % n) * (x % n)) % n == 1:
            return x


def solve_modulo_equations(a, b, n):
    d = find_gcd(a, n)
    if d == 1:
        return [(find_inverse_modulo(a, n) * b) % n]
    elif d > 1:
        if b % d != 0:  # no possible roots
            return []
        else:
            roots = solve_modulo_equations(a // d, b // d, n // d)
            return [roots[0] + (i * n) for i in range(d)]


def find_most_common(ciphertext):
    bigrams = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]
    bigrams_frequency = Counter(bigrams)
    bigrams_frequency = dict(bigrams_frequency)
    return sorted(bigrams_frequency, key=bigrams_frequency.get, reverse=True)[:5]


def transform_to_numeric_form(bigram, alphabet):
    return alphabet.index(bigram[0]) * len(alphabet) + alphabet.index(bigram[1])


def combine_most_common_bigrams(most_common_bigrams_given, most_common_bigrams):
    bigrams = []
    system_eq = []
    for i in most_common_bigrams:
        for j in most_common_bigrams_given:
            bigrams.append((i, j))
    for i in bigrams:
        for j in bigrams:
            if i == j or (j, i) in system_eq or i[0] == j[0] or i[1] == j[1]:
                continue
            system_eq.append((i, j))
    return system_eq


def find_key_from_bigram(system_eq, alphabet): #solutions
    keys = []
    x1, x2 = transform_to_numeric_form(system_eq[0][0], alphabet), transform_to_numeric_form(system_eq[1][0], alphabet)
    y1, y2 = transform_to_numeric_form(system_eq[0][1], alphabet), transform_to_numeric_form(system_eq[1][1], alphabet)
    a = solve_modulo_equations(x1 - x2, y1 - y2, len(alphabet) ** 2)
    for i in a:
        if find_gcd(i, len(alphabet)) != 1:
            continue
        b = (y1 - i * x1) % len(alphabet) ** 2
        keys.append((i, b))
    return keys


def decrypt(ciphertext, clear_keys, alphabet):
    alphabet_length = len(alphabet)
    decrypted_text = ""
    a, b = clear_keys[0], clear_keys[1]
    for i in range(0, len(ciphertext), 2):
        x = (find_inverse_modulo(a, alphabet_length ** 2)) * (
                    transform_to_numeric_form(ciphertext[i:i + 2], alphabet) - b) % (alphabet_length ** 2)
        decrypted_bigram = alphabet[x // alphabet_length] + alphabet[x % alphabet_length]
        decrypted_text += decrypted_bigram
    return decrypted_text


def find_correct_text(decrypted_text, most_common_bigrams, nonexistent_bigrams):
    most_common_given = find_most_common(decrypted_text)
    print(most_common_given)
    correctness_flag = True
    for i in most_common_given:
        if i in most_common_bigrams and i not in nonexistent_bigrams:
            print('true flag & bigram =', i)
            correctness_flag = True
        else:
            return False
    return correctness_flag


def find_possible_keys(combined_bigrams, alphabet):
    possible_keys = []
    for bigram in combined_bigrams:
        keys = find_key_from_bigram(bigram, alphabet)
        if len(keys) != 0:
            for k in range(len(keys)):
                possible_keys.append(keys[k])
    return possible_keys


def find_true_key(possible_keys, ciphertext, alphabet, nonexistent_bigrams):
    for k in possible_keys:
        plaintext = decrypt(ciphertext, k, alphabet)
        plaintext_bigrams = [plaintext[i:i + 2] for i in range(0, len(plaintext), 2)]
        letters_count = Counter(plaintext)
        letters_count = dict(letters_count)
        letters_count = sorted(letters_count, key=letters_count.get, reverse=True)[:5]
        if (letters_count[0] == 'о' or letters_count[0] == 'е') and not set(nonexistent_bigrams) & set(plaintext_bigrams):
            return k


ciphertext = read_file('encrypted_var2.txt')
most_common_bigrams_given = find_most_common(ciphertext)
print('most common bigrams in ciphertext: ', most_common_bigrams_given)
combined_bigrams = combine_most_common_bigrams(most_common_bigrams_given, most_common_bigrams)
possible_keys = find_possible_keys(combined_bigrams, alphabet)
print('possible keys:', possible_keys)
true_key = find_true_key(possible_keys, ciphertext, alphabet, nonexistent_bigrams)
print('true key:', true_key)
plaintext = decrypt(ciphertext, true_key, alphabet)
print(plaintext[:100])
