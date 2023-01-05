from pathlib import Path
import itertools


def read_and_clean(filename):
    with open(filename, encoding='utf8') as file:  # зчитуємо з файлу
        text = file.read().lower().replace('\n', '')  # зчитуємо й прибираємо \n і робимо маленькими літерами
    return text


def extended_gcd(a, b):  # РАЕ. повертає b=НСД(a, b), u,v -- такі що a*u + b*v = 1
    if a == 0:
        return b, 0, 1
    else:
        gcd, u1, v1 = extended_gcd(b % a, a)
        u = v1 - (b // a) * u1
        v = u1
        return gcd, u, v


def modular_inverse(a, n):  # знаходить x = a^-1 (mod n)
    gcd, u, v = extended_gcd(a, n)
    if gcd == 1:
        return u % n
    else:
        return None


def solve_congruence(a, b, n):  # знаходить х з лін. порівняння ax = b (mod n)
    gcd, u, v = extended_gcd(a, n)
    if gcd == 1:
        return [(modular_inverse(a, n) * b) % n]
    else:
        if b % gcd != 0:
            return None
        else:
            a1 = a / gcd
            b1 = b / gcd
            n1 = n / gcd
            a1_inv = modular_inverse(a1, n1)
            x0 = (b1 * a1_inv) % n
            return [int(x0 + i * n1) for i in range(gcd)]


def fre_of_bigrams(txt, alphabet, cross=True):  # для розрахунка частот біграм
    dic = {}
    for l1 in alphabet:
        for l2 in alphabet:
            dic.update({l1 + l2: 0})
    if cross:  # для перехресних біграм
        for i in range(len(txt) - 1):
            dic[txt[i] + txt[i + 1]] += 1  # рахуємо кількість появ біграми в тексті
        for key in dic.keys():
            dic[key] = round(dic[key] / (len(txt) - 1), 5)  # рахуємо частоту
    else:  # для неперехресних біграм
        if len(txt) % 2 == 1:
            txt += "а"  # щоб кожній літері була пара
        for i in range(len(txt) - 1):
            if i % 2 == 1:
                continue
            dic[txt[i] + txt[i + 1]] += 1  # рахуємо кількість появ біграми в тексті
        for key in dic.keys():
            dic[key] = round(dic[key] / (len(txt) / 2), 5)  # рахуємо частоту
    return dic


def fre_of_letters(txt, alphabet):  # розрахунок частоти кожного символу
    dic = {}
    for l in alphabet:
        dic.update({l: 0})
    for i in txt:  # скільки разів кожен символ зустрічається у тексті
        dic[i] += 1
    for l in alphabet:
        dic.update({l: round(dic[l] / len(txt), 5)})  # рахуємо частоту
    return dic


def find_5_most_freq_bi(text, alphabet, cross=False):  # повертає 5 найчастіших біграм в тексті
    bigrams_freqs = fre_of_bigrams(text, alphabet, cross=cross)
    most_freq_5 = sorted(bigrams_freqs, key=lambda key: bigrams_freqs[key], reverse=True)[:5]
    return most_freq_5


def bigram_to_num(bigram, alphabet, alf_numbers):  # переводить біграму в число
    m = len(alphabet)
    return alf_numbers[bigram[0]] * m + alf_numbers[bigram[1]]


def find_possible_keys(ciphertext, alphabet, alf_numbers):  # знаходить всі можливі ключі
    m = len(alphabet)
    m_2 = m ** 2
    ct_bigrams = find_5_most_freq_bi(ciphertext, alphabet)  # 5 найчастіших біграм шифротексту
    print("5 найчастіших біграм:", ct_bigrams)
    ru_bigrams = ['ст', 'но', 'то', 'на', 'ен']  # 5 найчастіших біграм російської мови
    all_matches = list(itertools.product(ru_bigrams, ct_bigrams))  # пари (x, y)
    all_matches_pairs = list(itertools.combinations(all_matches, 2))  # пари ((x1,y1), (x2,y2))
    # прибираємо ті пари де x1=x2 або y1=y2, бо в нас біграми переходять однозначно:
    matches_pairs = [match for match in all_matches_pairs if match[0][0] != match[1][0] and match[0][1] != match[1][1]]
    possible_keys = {}
    for pair in matches_pairs:
        x1 = bigram_to_num(pair[0][0], alphabet, alf_numbers)
        x2 = bigram_to_num(pair[1][0], alphabet, alf_numbers)
        y1 = bigram_to_num(pair[0][1], alphabet, alf_numbers)
        y2 = bigram_to_num(pair[1][1], alphabet, alf_numbers)

        x = (x1 - x2) % m_2
        y = (y1 - y2) % m_2

        a_variants = solve_congruence(x, y, m_2)  # знаходимо а
        if a_variants:
            b_variants = [(y1 - a * x1) % m_2 for a in a_variants]  # знаходимо b
            possible_keys[pair] = (a_variants, b_variants)
    return possible_keys


def is_meaningful(text, alphabet):  # розпізнавач російської мови
    # критерій частих l-грам: перевіряємо частоти найчастіших символів-- "о", "е", "а"
    text_lett_freqs = fre_of_letters(text, alphabet)
    if not (text_lett_freqs['о'] >= 0.05 and text_lett_freqs['а'] >= 0.05 and text_lett_freqs['е'] >= 0.05):
        return False
    # критерій заборонених l-грам: перевіряємо частоти найрідших символів -- "ф", "э", "щ"
    if not (text_lett_freqs['ф'] <= 0.01 and text_lett_freqs['э'] <= 0.01 and text_lett_freqs['щ'] <= 0.01):
        return False
    # критерій частих l-грам: перевіряємо частоти найчастіших біграм -- 'ст', 'но', 'то'
    text_bi_freqs = fre_of_bigrams(text, alphabet, cross=True)
    if not (text_bi_freqs['ст'] >= 0.009 and text_bi_freqs['но'] >= 0.009 and text_bi_freqs['то'] >= 0.009):
        return False
    return True


def text_to_bigrams(text):  # розбиває текст на неперехресні біграми
    bigrams = []
    if len(text) % 2 == 1:
        text += "а"  # щоб кожній літері була пара
    for i in range(0, len(text) - 1, 2):
        bigrams.append(text[i] + text[i + 1])
    return bigrams


def affine_bigram_decrypt(ciphertext, a, b, alphabet, alf_numbers, numbers_alf):  # розшифровка афінного шифру
    m = len(alphabet)
    m_2 = m ** 2
    a_inv = modular_inverse(a, m_2)
    if a_inv:  # якщо існує обернений по модулю
        bigrams = text_to_bigrams(ciphertext)  # розбиваємо текст на біграми
        bigrams_as_nums = [bigram_to_num(bi, alphabet, alf_numbers) for bi in bigrams]  # переводимо біграми в числа
        decrypted_bigrams_as_nums = [(a_inv * (y_i - b)) % m_2 for y_i in bigrams_as_nums]  # розшифровуємо
        decrypted_bigrams = [numbers_alf[x // m] + numbers_alf[x % m] for x in
                             decrypted_bigrams_as_nums]  # числа в біграми
        decrypted_text = ''.join(decrypted_bigrams)  # склеюємо список біграм в рядок
        return decrypted_text
    return None


def find_right_key(ciphertext, possible_keys, alphabet, alf_numbers, numbers_alf):  # перебирає можливі ключі
    meaningful_texts = {}
    for pair in possible_keys.values():
        a = pair[0][0]
        b = pair[1][0]
        decrypted = affine_bigram_decrypt(ciphertext, a, b, alphabet, alf_numbers, numbers_alf)  # розшифровка
        if decrypted:  # якщо текст можливо розшифрувати, тобто існує обернений по модулю для а
            if is_meaningful(decrypted, alphabet):  # якщо текст змістовний
                meaningful_texts[(a, b)] = decrypted
    return meaningful_texts


if __name__ == '__main__':
    alf = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
    alphabet_numbers = {letter: i for i, letter in enumerate(alf)}
    numbers_alphabet = {i: letter for i, letter in enumerate(alf)}

    p = Path.cwd()

    the_text = read_and_clean(p / 'variants.utf8' / '11.txt')

    all_possible_keys = find_possible_keys(the_text, alf, alphabet_numbers)
    # print(all_possible_keys)

    right_key = find_right_key(the_text, all_possible_keys, alf, alphabet_numbers, numbers_alphabet)
    print("Ключ і текст:", right_key)
