# -------------------------- part 1
from math import gcd


def next(arr: list, b: int):
    odds = [0, 1]
    for i in range(len(arr) - 1): odds.append(arr[i] * odds[-1] + odds[-2])
    return odds[-1] + b if odds[-1] < 0 else odds[-1]


def func(a: int, b: int):
    if gcd(a, b) > 1: return 0
    val1, val2, m = b, a, []
    while val2:
        m.append(-(val1 // val2))
        val1, val2 = val2, val1 % val2
    return next(m, b)


def roots(a: int, b: int, c: int):
    root_numbers = int(gcd(a, b, c))
    if root_numbers > 1: a, b, c = int(a / root_numbers), int(b / root_numbers), int(c / root_numbers)
    a, result = func(a, c), []
    if a == 0: return # print(f'No roots! {a}x={b}mod{c}')
    for i in range(1, root_numbers + 1): result.append((a * b % c) + (i - 1) * c)
    return result

# ---------------------------- part 2


def split(text: str):
    listed_text = list(text)
    blocks = []
    for i in range(len(listed_text)):
        if i % 2 == 0:
            if i != len(listed_text)-1:
                blocks.append(listed_text[i]+listed_text[i+1])
    return blocks


def X_value(bigram: str, alphabet: list):
    bigram = list(bigram)
    id1 = alphabet.index(bigram[0])
    id2 = alphabet.index(bigram[1])
    return (id1*len(alphabet) + id2) % len(alphabet)**2


def get_ab(xbigrams: list, ybigrams: list, alphabet: list):  # input: ['ст', 'то'] ['ку', 'уф']
    y1, y2, x1, x2 = X_value(ybigrams[0], alphabet), X_value(ybigrams[1], alphabet), \
                     X_value(xbigrams[0], alphabet), X_value(xbigrams[1], alphabet)
    m = len(alphabet) ** 2
    x, y = x1 - x2, y1 - y2
    a, b = roots(x, y, m), []
    if a is None: a = [0]  # if no roots
    for i in range(len(a)): b.append((y1 - a[i] * x1) % m)
    return [a, b]


def decrypt(ybigram_ct: str, a: int, b: int, alphabet: list):  # decrypt & convert
    y, m = X_value(ybigram_ct, alphabet), len(alphabet)
    if func(a, m ** 2) == 0: return '.'
    X_val = (func(a, m**2) * (y - b)) % m**2
    b = X_val % m
    a = (X_val - b) // m
    return ''.join([alphabet[a], alphabet[b]])

# =============================================
# === algorithms from lab1 ====================


def adding(words: str, frequency: dict) -> dict:
    for i in words:
        if i in frequency:
            frequency[i] += 1
        else:
            frequency[i] = 1


def adding_bigram_list(array: str, amounts: dict):
    length = len(array)
    for i in range(0, length):
        if i == length - 1: return amounts
        if i % 2 == 0: adding([array[i] + array[i+1]], amounts)


def replace_bigrams(dictionary: dict, total_bigrams: int):
    for k in dictionary.keys(): total_bigrams += dictionary[k]
    for i in dictionary.keys(): dictionary[i] = "{:.10f}".format(dictionary[i] / total_bigrams)
    return sorted(dictionary.items(), key=lambda item: (item[1], item[0]), reverse=True)


banned = ['яь', 'юь', 'йь', 'еь', 'аь', 'иь', 'жь', 'гь', 'эь', 'щь', 'хь', 'фь', 'уь', 'ыь', 'оь', 'жж', 'ьь', 'щщ',
           'жы', 'шы', 'ыы', 'иы', 'яы', 'еы', 'юы', 'уы', 'кь', 'эы', 'аы', 'ць', 'оы']


def statistics(text: str, sorting: bool):
    set_without_spaces, bigram_set, result = {}, {}, []
    adding(text, set_without_spaces)
    tupple_bigrams = replace_bigrams(adding_bigram_list(text, bigram_set), 0)
    for i in range(len(tupple_bigrams)):
        if sorting and tupple_bigrams[i][0] in banned:
            return 'skip'
        result.append(tupple_bigrams[i][0])
    return result

# ==================================================
# -------------------------- part 3


def start(text_block: list, ab: list, alphabet: list):
    result = []
    for i in range(len(text_block)):
        result.append(decrypt(text_block[i], ab[0][0], ab[1][0], alphabet))
    return ''.join(result)


def go(top: list, top_bigrams: list, text_block: list, alphabet: list):
    # choose one from top
    used, visited_i = [[0, 0]], []
    for i in range(len(top)):
        if i not in visited_i:
            visited_i.append(i)
            xbigrams = [top[i], 0]  # initialize and save

            # for chosen choose another one from top
            for j in range(len(top)):
                if j not in visited_i and j != i:
                    xbigrams[1] = top[j]   # save

                    # chose one from top_bigrams
                    visited_k = []
                    for k in range(len(top_bigrams)):
                        visited_k.append(k)
                        ybigrams = [top_bigrams[k], 0]  # initialize and save

                        # for chosen choose another one from top_bigrams
                        for l in range(len(top_bigrams)):
                            if l not in visited_k:
                                ybigrams[1] = top_bigrams[l]  # save

                                ab = get_ab(xbigrams, ybigrams, alphabet)  # getting keys a, b for chosen bigrams

                                if ab in used: continue  # avoid repeating operations and outputs with used a & b
                                used.append(ab)

                                # ↓ show popular bigrams or return skip if there is impossible in language bigram
                                plaintext = start(text_block, ab, alphabet)  # plaintext = PT
                                stats = statistics(plaintext, True)[:21]  # if PT has banned bigrams -  returns 'skip'
                                # print(f'{xbigrams}->{ybigrams} | {stats} | i:{i} j:{j} k:{k} l:{l}')

                                if stats != 'skip' and set(list(plaintext)) != {'.'}:
                                    print(f'PT: {start(text_block, ab, alphabet)[:60]} | A: {ab[0][0]}  B: {ab[1][0]}')
    return


text = open('V4', mode='r').read().lower()
text2 = open('04.txt', mode='r').read().replace('\n', '')

alphabet1 = list("абвгдежзийклмнопрстуфхцчшщыьэюя")  # for text 1
alphabet2 = list("абвгдежзийклмнопрстуфхцчшщьыэюя")  # for text 2
top = ['ст', 'но', 'то', 'на', 'ен']

top_bigrams1 = statistics(text, False)[:5]
top_bigrams2 = statistics(text2, False)[:5]

text_blocks1 = split(text)
text_blocks2 = split(text2)

go(top, top_bigrams1, text_blocks1, alphabet1)
go(top, top_bigrams2, text_blocks2, alphabet2)


# saving to files
t1 = [start(text_blocks1, [[5], [960]], alphabet1)]
t2 = [start(text_blocks2, [[390], [10]], alphabet2)]


for i in range(len(t1)):
    a = 'w' if i == 0 else 'a'
    f, data_ = open("V4_encrypted.txt", a), t1[i]
    for line in list(''.join(data_) + '\n'): f.write(line)
    f.close()

for i in range(len(t2)):
    a = 'w' if i == 0 else 'a'
    f, data_ = open("04_encrypted.txt", a), t2[i]
    for line in list(''.join(data_) + '\n'): f.write(line)
    f.close()
