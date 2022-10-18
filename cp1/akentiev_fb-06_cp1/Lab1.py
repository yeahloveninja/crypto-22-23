import re
import math

file = open('book.txt', encoding='utf-8')
text = file.read()


def text_space(text):
    txt = re.sub(r'[^а-яА-Я ]', '', text)
    space = txt.lower().replace('  ', ' ').replace('   ', ' ')
    return space


file_Space = open('fileSpace.txt', 'w', encoding='utf-8')
file_Space.write(text_space(text))
file_Space.close()

textWithSpace = text_space(text)
textWithoutSpace = textWithSpace.replace(' ', '')

file_No_Space = open('fileNoSpace.txt', 'w', encoding='utf-8')
file_No_Space.write(textWithoutSpace)
file_No_Space.close()


def letter_freq_with_space(textWithSpace):
    d = {}
    for i in textWithSpace:
        d[i] = d.get(i, 0) + 1 / (len(textWithSpace))
        d[i] = round(d[i], 6)
    return d


def letter_freq_without_space(textWithoutSpace):
    d = {}
    for i in textWithoutSpace:
        d[i] = d.get(i, 0) + 1 / (len(textWithoutSpace))
        d[i] = round(d[i], 6)
    return d


def bigram_freq_with_space_step1(textWithSpace):
    freq_bigram = {}
    dict_bigram = [] #список усіх біграм із алфавіту з пробілом
    for i in range(0, len(textWithSpace)-1):
        dict_bigram.append(textWithSpace[i] + textWithSpace[i + 1])
    for i in dict_bigram:
        freq_bigram[i] = freq_bigram.get(i, 0) + 1 / (len(textWithSpace))
        freq_bigram[i] = round(freq_bigram[i], 6)
    return freq_bigram


def bigram_freq_with_space_step2(textWithSpace):
    freq_bigram = {}
    dict_bigram = []
    for i in range(0, len(textWithSpace)-1, 2):
        dict_bigram.append(textWithSpace[i] + textWithSpace[i + 1])
    for i in dict_bigram:
        freq_bigram[i] = freq_bigram.get(i, 0) + 1 / (len(textWithSpace))
        freq_bigram[i] = round(freq_bigram[i], 6)
    return freq_bigram


def bigram_freq_without_space_step1(textWithoutSpace):
    freq_bigram = {}
    dict_bigram = []
    for i in range(0, len(textWithoutSpace)-1):
        dict_bigram.append(textWithoutSpace[i] + textWithoutSpace[i + 1])
    for i in dict_bigram:
        freq_bigram[i] = freq_bigram.get(i, 0) + 1 / (len(textWithoutSpace))
        freq_bigram[i] = round(freq_bigram[i], 6)
    return freq_bigram


def bigram_freq_without_space_step2(textWithoutSpace):
    freq_bigram = {}
    dict_bigram = []
    for i in range(0, len(textWithoutSpace)-1, 2):
        dict_bigram.append(textWithoutSpace[i] + textWithoutSpace[i + 1])
    for i in dict_bigram:
        freq_bigram[i] = freq_bigram.get(i, 0) + 1 / (len(textWithoutSpace))
        freq_bigram[i] = round(freq_bigram[i], 6)
    return freq_bigram


dictionary_with_1 = bigram_freq_with_space_step1(textWithSpace)
dictionary_with_2 = bigram_freq_with_space_step2(textWithSpace)
dictionary_without_1 = bigram_freq_without_space_step1(textWithoutSpace)
dictionary_without_2 = bigram_freq_without_space_step2(textWithoutSpace)


def calculate_h1(textWithSpace):
    symbol_frequencies = [textWithSpace.count(symbol) / len(textWithSpace) for symbol in set(textWithSpace)]
    return -sum([frequency * math.log(frequency, 2) for frequency in symbol_frequencies])


def calculate1_h1(textWithoutSpace):
    symbol_frequencies = [textWithoutSpace.count(symbol) / len(textWithoutSpace) for symbol in set(textWithoutSpace)]
    return -sum([frequency * math.log(frequency, 2) for frequency in symbol_frequencies])


def calculate_space_h2():
    return -sum([frequency * math.log(frequency, 2) for frequency in dictionary_with_1.values()])


def calculate_space_step2_h2():
    return -sum([frequency * math.log(frequency, 2) for frequency in dictionary_with_2.values()])


def calculate_nospace_h2():
    return -sum([frequency * math.log(frequency, 2) for frequency in dictionary_without_1.values()])


def calculate_nospace_step2_h2():
    return -sum([frequency * math.log(frequency, 2) for frequency in dictionary_without_2.values()])


def R_h1_s():
    return 1 - calculate_h1(textWithSpace) / math.log2(34)


def R_h1_ns():
    return 1 - calculate1_h1(textWithoutSpace) / math.log2(33)


def R_h2_s1():
    return 1 - (calculate_space_h2() / 2) / math.log2(34)


def R_h2_s2():
    return 1 - (calculate_space_step2_h2() / 2) / math.log2(34)


def R_h2_ns1():
    return 1 - (calculate_nospace_h2() / 2) / math.log2(33)


def R_h2_ns2():
    return 1 - (calculate_nospace_step2_h2() / 2) / math.log2(33)


# print("H1 для літер з пробілами: ", calculate_h1(textWithSpace))
# print("H1 для літер без пробілів: ", calculate1_h1(textWithoutSpace))
# print("H2 для біграм з пробілами: ", calculate_space_h2())
# print("H2 для біграм з пробілами кроком 2: ", calculate_space_step2_h2())
# print("H2 для біграм без пробілів: ", calculate_nospace_h2())
# print("H2 для біграм без пробілів кроком 2: ", calculate_nospace_step2_h2() )
# print("Надлишковість для H1: ", R_h1_s())
# print("Надлишковість для H1 без пробілів: ", R_h1_ns())
# print("Надлишковість для H2 з пробілами: ", R_h2_s1())
# print("Надлишковість для H2 з пробілами кроком 2: ", R_h2_s2())
# print("Надлишковість для H2 без пробілів: ", R_h2_ns1())
# print("Надлишковість для H2 без пробілів кроком 2: ", R_h2_ns2())



