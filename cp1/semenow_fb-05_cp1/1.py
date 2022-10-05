# 2.txt - __ text
# 3.txt - no space
import re
import math
from collections import Counter


def find_monogram(text):
    big_lst = re.findall(r'\w', text)
    clear_lst = set(big_lst)
    letters = {}
    counter = 0
    for letter in clear_lst:
        letters[letter] = len(re.findall(letter, text))
        counter += len(re.findall(letter, text))
    for i in letters:
        letters[i] = float(letters[i]/counter)
    return letters


def find_bigram(text, counter):
    big_lst = re.findall(r'\w\w', text)
    clear_lst = set(big_lst)
    bigrams = {}
    for i in clear_lst:
        bigrams[i] = len(re.findall(i, text))
        counter += len(re.findall(i, text))
    return bigrams, counter


def cross_bigrams(text):
    text_first_letter = ""
    text_second_letter = ""
    for i in text[0::2]:
        text_first_letter += i
    for k in text[1::2]:
        text_second_letter += k
    text_first_letter, counter = find_bigram(text_first_letter, 0)
    text_second_letter, counter = find_bigram(text_second_letter, counter)
    all_bigr, counter = find_bigram(text, counter)
    dicts = (all_bigr, text_second_letter, text_first_letter)
    res = Counter()
    for k in dicts:
        res.update(k)
    for i in res:
        res[i] = float(res[i]/counter)
    return res


def find_entropy(frequency, nrgams):
    entropy = 0
    for values in frequency.values():
        entropy += - values * math.log(values, 2)
    entropy *= 1 / nrgams
    return entropy


def find_r(entrop, elements):
    r = 1 - (entrop/math.log2(elements))
    return r


def sort_dict(dct):
    sorted_dict = {}
    sorted_keys = sorted(dct, key=dct.get)
    for w in reversed(sorted_keys):
        sorted_dict[w] = dct[w]
    return sorted_dict


def print_ngrams(dct):
    column = sort_dict(dct)
    count = 0
    for row in column:
        print(f"{row} --- {to_fixed(column[row], 10)}")
        count += column[row]


def to_fixed(num, digits=0):
    return f"{num:.{digits}f}"


space_txt = open('2.txt', 'r').read()
no_space_txt = open('3.txt', 'r').read()

space_monograms = find_monogram(space_txt)  # монограммы
space_monograms_entropy = find_entropy(space_monograms, 1)
space_monograms_r = find_r(space_monograms_entropy, 34)
no_space_monograms = find_monogram(no_space_txt)
no_space_monograms_entropy = find_entropy(no_space_monograms, 1)
no_space_monograms_r = find_r(no_space_monograms_entropy, 33)

space_bigrams = cross_bigrams(space_txt)  # биграммы
space_bigrams_entropy = find_entropy(space_bigrams, 2)
space_bigrams_r = find_r(space_bigrams_entropy, 34)
no_space_bigrams = cross_bigrams(no_space_txt)
no_space_bigrams_entropy = find_entropy(no_space_bigrams, 2)
no_space_bigrams_r = find_r(no_space_bigrams_entropy, 33)

print(f"h1 in text with space {space_monograms_entropy}")
print(f"r1 in text with space {space_monograms_r}")
print(f"h1 in text without space {no_space_monograms_entropy}")
print(f"r1 in text without space {no_space_monograms_r}\n")

print(f"h2 in text with space {space_bigrams_entropy}")
print(f"r2 in text with space {space_bigrams_r}")
print(f"h2 in text without space {no_space_bigrams_entropy}")
print(f"r2 in text without space {no_space_bigrams_r}")

print_ngrams(no_space_monograms)
print_ngrams(no_space_bigrams)

# print_ngrams(space_bigrams)
