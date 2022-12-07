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


def calculate_h1(textWithSpace):
    symbol_frequencies = [textWithSpace.count(symbol) / len(textWithSpace) for symbol in set(textWithSpace)]
    return -sum([frequency * math.log(frequency, 2) for frequency in symbol_frequencies])


def calculate1_h1(textWithoutSpace):
    symbol_frequencies = [textWithoutSpace.count(symbol) / len(textWithoutSpace) for symbol in set(textWithoutSpace)]
    return -sum([frequency * math.log(frequency, 2) for frequency in symbol_frequencies])


def calculate_space_h2():
    bigrams = [textWithSpace[i:i + 2] for i in range(0, len(textWithSpace) - 1)]
    bigrams_frequencies = [bigrams.count(symbol) / len(bigrams) for symbol in set(bigrams)]
    return -sum([frequency * math.log(frequency, 2) / 2 for frequency in bigrams_frequencies])


def calculate_space_step2_h2():
    bigrams = [textWithSpace[i:i + 2] for i in range(0, len(textWithSpace) - 1, 2)]
    bigrams_frequencies = [bigrams.count(symbol) / len(bigrams) for symbol in set(bigrams)]
    return -sum([frequency * math.log(frequency, 2) / 2 for frequency in bigrams_frequencies])


def calculate_nospace_h2():
    bigrams = [textWithoutSpace[i:i + 2] for i in range(0, len(textWithoutSpace) - 1)]
    bigrams_frequencies = [bigrams.count(symbol) / len(bigrams) for symbol in set(bigrams)]
    return -sum([frequency * math.log(frequency, 2) / 2 for frequency in bigrams_frequencies])


def calculate_nospace_step2_h2():
    bigrams = [textWithoutSpace[i:i + 2] for i in range(0, len(textWithoutSpace) - 1, 2)]
    bigrams_frequencies = [bigrams.count(symbol) / len(bigrams) for symbol in set(bigrams)]
    return -sum([frequency * math.log(frequency, 2) / 2 for frequency in bigrams_frequencies])


def R_h1_s():
    return 1 - calculate_h1(textWithSpace) / math.log2(33)


def R_h1_ns():
    return 1 - calculate1_h1(textWithoutSpace) / math.log2(32)


def R_h2_s1():
    return 1 - calculate_space_h2() / math.log2(33)


def R_h2_s2():
    return 1 - calculate_space_step2_h2() / math.log2(33)


def R_h2_ns1():
    return 1 - calculate_nospace_h2()/ math.log2(32)


def R_h2_ns2():
    return 1 - calculate_nospace_step2_h2() / math.log2(32)


# print("H1 для літер з пробілами: ", calculate_h1(textWithSpace))
# print("H1 для літер без пробілів: ", calculate1_h1(textWithoutSpace))
# print("H2 для біграм з пробілами: ", calculate_space_h2())
# print("H2 для біграм з пробілами кроком 2: ", calculate_space_step2_h2())
# print("H2 для біграм без пробілів: ", calculate_nospace_h2())
# print("H2 для біграм без пробілів кроком 2: ", calculate_nospace_step2_h2())
# print("Надлишковість для H1: ", R_h1_s())
# print("Надлишковість для H1 без пробілів: ", R_h1_ns())
# print("Надлишковість для H2 з пробілами: ", R_h2_s1())
# print("Надлишковість для H2 з пробілами кроком 2: ", R_h2_s2())
# print("Надлишковість для H2 без пробілів: ", R_h2_ns1())
# print("Надлишковість для H2 без пробілів кроком 2: ", R_h2_ns2())
