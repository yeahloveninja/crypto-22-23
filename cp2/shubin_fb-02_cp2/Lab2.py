import re
import matplotlib.pyplot
from matplotlib import pyplot as plt


def read_and_clean(filename):
    with open(filename, encoding='utf8') as file:  # зчитуємо з файлу
        text = file.read().lower().replace('\n', '')  # зчитуємо й прибираємо все інше і робимо маленькими літерами
        text = re.sub(r'[^а-яё ]', '', text)
        text = text.replace(' ', '')
    return text


def vigenere_encrypt(plaintext, key, alf_numbers, numbers_alf):
    r = len(key)
    m = len(alf_numbers)
    pt_numbers = [alf_numbers[letter] for letter in plaintext]
    key_numbers = [alf_numbers[letter] for letter in key]
    ciphertext = ''
    for i, x_i, in enumerate(pt_numbers):
        y_i = (x_i + key_numbers[i % r]) % m
        ciphertext += numbers_alf[y_i]
    return ciphertext


def vigenere_decrypt(ciphertext, key, alf_numbers, numbers_alf):
    r = len(key)
    m = len(alf_numbers)
    ct_numbers = [alf_numbers[letter] for letter in ciphertext]
    key_numbers = [alf_numbers[letter] for letter in key]
    plaintext = ''
    for i, y_i, in enumerate(ct_numbers):
        x_i = (y_i - key_numbers[i % r]) % m
        plaintext += numbers_alf[x_i]
    return plaintext


def index_vidp(txt, alphabet):  # Індекс відповідності
    n = len(txt)
    letters_count = {letter: 0 for letter in alphabet}
    for i in txt:  # скільки разів кожен символ зустрічається у шифротексті
        letters_count[i] += 1
    ind = sum([letters_count[t] * (letters_count[t] - 1) for t in alphabet]) / (n * (n - 1))
    m_ind = sum([(letters_count[t] / n) ** 2 for t in alphabet])
    return ind, m_ind


def plot_r_candidates(r_candidates, d_values):  # графік иожливих значень r
    matplotlib.pyplot.plot(r_candidates, d_values)
    matplotlib.pyplot.xticks(r_candidates)
    matplotlib.pyplot.show()


def find_r(ciphertext):  # знаходимо період шифру (r)
    n = len(ciphertext)
    d_values = []
    r_candidates = [i for i in range(6, 31)]
    for r in r_candidates:
        d_r = sum([ciphertext[i] == ciphertext[i + r] for i in range(n - r)])
        d_values.append(d_r)
    print("D_r=", d_values)
    r_best_candidate = r_candidates[d_values.index(max(d_values))]
    plot_r_candidates(r_candidates, d_values)  # графік значень статистики D_r
    print("r=", r_best_candidate)
    return r_best_candidate


def fre_of_letters(txt, alphabet):  # розрахунок частоти кожного символу
    dic = {}
    for l in alphabet:
        dic.update({l: 0})
    for i in txt:  # скільки разів кожен символ зустрічається у тексті
        dic[i] += 1
    for l in alphabet:
        dic.update({l: round(dic[l] / len(txt), 5)})  # расчет частоты
    return dic


def ciphertext_to_blocks(ciphertext, r):  # розбиваємо шифротекст на блоки
    blocks = [ciphertext[i::r] for i in range(r)]
    return blocks


def find_key_letter_o(ciphertext_blocks, alphabet, alf_numbers, numbers_alf):  # знаходимо ключ
    m = len(alphabet)
    key = []
    for block in ciphertext_blocks:
        block_fre = fre_of_letters(block, alphabet)
        most_fre_letter_block = max(block_fre, key=block_fre.get)
        # 'о' -- найчастіша в російській мові
        k_i = (alf_numbers[most_fre_letter_block] - alf_numbers['о']) % m
        key.append(numbers_alf[k_i])
    return key


def vigenere_cryptanalysis(ciphertext, alphabet, alf_numbers, numbers_alf):
    m = len(alphabet)
    r_best_candidate = find_r(ciphertext)
    # r_best_candidate = 17
    ciphertext_blocks = ciphertext_to_blocks(ciphertext, r_best_candidate)
    key = find_key_letter_o(ciphertext_blocks, alphabet, alf_numbers, numbers_alf)
    print("key =", key)
    decrypted_on_key = vigenere_decrypt(ciphertext, key, alf_numbers, numbers_alf)
    print("decrypted_on_key=", decrypted_on_key)

    # беремо початок тексту, де можемо помітити неправильну розшифровку
    fragment = 'антонионезнаюоыаегоятакпечаленмцо'
    # бачимо що дві останні літери неправильні
    len_fr = len(fragment)
    last_let_ind_in_key = len_fr % r_best_candidate - 1
    second_last_let_ind_in_key = len_fr % r_best_candidate - 2
    # замість "мцо" повинно бути слово "мне"
    proper_second_last = alf_numbers['н']
    proper_last = alf_numbers['е']
    # знаючи правильні літери знаходимо 14 та 15 літери ключа
    key[second_last_let_ind_in_key] = numbers_alf[(alf_numbers[ciphertext[len_fr - 2]] - proper_second_last) % m]
    key[last_let_ind_in_key] = numbers_alf[(alf_numbers[ciphertext[len_fr - 1]] - proper_last) % m]
    print("new key =", key)
    decrypted_on_new_key = vigenere_decrypt(ciphertext, key, alf_numbers, numbers_alf)
    print("decrypted_on_new_key=", decrypted_on_new_key)


if __name__ == '__main__':
    alf_a = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    alphabet_numbers = {letter: i for i, letter in enumerate(alf_a)}
    numbers_alphabet = {i: letter for i, letter in enumerate(alf_a)}

    ################## Зчитування тексту ##############################
    text1 = read_and_clean('TEXT.txt')
    ################### Завдання 1-2 ############################
    print("################### Завдання 1-2 ############################")
    keys = ['аб', 'сто', 'киев', 'альфа', 'асинхронность', 'сложныйдлинныйключ']
    r_vals = []
    I_vals = []
    for k in keys:
        encrypted = vigenere_encrypt(text1, k, alphabet_numbers, numbers_alphabet)
        # decrypted = vigenere_decrypt(encrypted, k, alphabet_numbers, numbers_alphabet)
        index_vidpovidnosti, mat_spodiv = index_vidp(encrypted, alf_a)
        print("r=", len(k), 'I(Y)=', index_vidpovidnosti, "MI(Y)=", mat_spodiv)
        r_vals.append(len(k))
        I_vals.append(index_vidpovidnosti)
    plt.plot(r_vals, I_vals)
    plt.show()

    ################### Завдання 3#################################
    print("\n################### Завдання 3#################################")
    alf_2 = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    alphabet_numbers_2 = {letter: i for i, letter in enumerate(alf_2)}
    numbers_alphabet_2 = {i: letter for i, letter in enumerate(alf_2)}

    ciphertext_var11 = read_and_clean('var11.txt')
    vigenere_cryptanalysis(ciphertext_var11, alf_2, alphabet_numbers_2, numbers_alphabet_2)
