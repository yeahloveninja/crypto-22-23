import re
from math import log2

sort_rules = r'[1-9.,"\'-?:–!;a-z»A-Z„n{}#°—’’%` +\f\r\v\0^\ufeff@№&…*\\\n\t“«]'


def open_sort(file, spaces):
    text = open(file, "r", encoding="utf-8").read()
    return re.sub(sort_rules, '', text).replace(" ", "`").lower() if spaces else re.sub(sort_rules, '', text).replace(
        " ", "").lower()


def char_counter(text):
    counter = {}
    for letter in text:
        counter.setdefault(letter, 0)
        counter[letter] += 1
    return counter


def char_frequency(char_count):
    all_chars = 0
    count_frequency = {}
    for letter in char_count:
        all_chars += char_count[letter]
    for char in char_count:
        count_frequency.setdefault(char, 0)
        count_frequency[char] = char_count[char] / all_chars
    return count_frequency


def entropy(text, n):
    h = 0
    for letter in text:
        h += -text[letter] * log2(text[letter])
    h = h * 1 / n

    return round(h, 5)


def bigrams_counter(text, step):
    text = text.replace(" ", "_")
    counter = {}
    slide_bigrmas = [text[i:i + 2] for i in range(0, len(text), step)]
    for bigram in slide_bigrmas:
        counter.setdefault(bigram, 0)
        counter[bigram] += 1

    return counter


def sort_dict(dictionary):
    sorted_dict = {}
    sorted_values = sorted(dictionary.values(), reverse=True)
    for i in sorted_values:
        for k in dictionary.keys():
            if dictionary[k] == i:
                sorted_dict[k] = dictionary[k]
                break
    return sorted_dict


def calc_R(h, atphabet):
    return round(1 - h / log2(atphabet), 5)


alphabet_nospace = 33
alphabet_space = 34

text_with_spaces = open_sort("some_text.txt", True)
text_with_no_spaces = open_sort("some_text.txt", False)

char_frequency_spaces = sort_dict(char_frequency(char_counter(text_with_spaces)))
char_frequency_no_spaces=sort_dict(char_frequency(char_counter(text_with_no_spaces)))
# entropy and R for H1
print("h1 with space: " + str(entropy(char_frequency_spaces, 1)))
print("R for h1 with space: " + str(calc_R(entropy(char_frequency_spaces, 1), alphabet_space)), '\n')

print("h1 without space: " + str(entropy(char_frequency_no_spaces, 1)))
print(
    "R for h1 without space: " + str(calc_R(entropy(char_frequency_no_spaces, 1), alphabet_nospace)), '\n')
print("====================================================================", "\n")
# entropy and R for H2
# with intersection
slide_bigrmas = sort_dict(char_frequency(bigrams_counter(text_with_spaces, 1)))
print("h2 with space(slide): " + str(entropy(slide_bigrmas, 2)))
print("R for h2 with space(slide): " + str(calc_R(entropy(slide_bigrmas, 2), alphabet_space)), '\n')

slide_with_no_spaces = sort_dict(char_frequency(bigrams_counter(text_with_no_spaces, 1)))
print("h2 without space(slide_with_no_spaces): " + str(entropy(slide_with_no_spaces, 2)))
print("R for h2 without space(slide_with_no_spaces): " + str(calc_R(entropy(slide_with_no_spaces, 2), alphabet_nospace)), '\n')

# without intersection
block_bigrams = sort_dict(char_frequency(bigrams_counter(text_with_spaces, 2)))
print("h2 with space(block): " + str(entropy(block_bigrams, 2)))
print("R for h2 with space (block): " + str(calc_R(entropy(block_bigrams, 2), alphabet_space)), '\n')

block_with_no_spaces = sort_dict(char_frequency(bigrams_counter(text_with_no_spaces, 2)))
print("h2 without space(block_with_no_spaces): " + str(entropy(block_with_no_spaces, 2)))
print("R for h2 without space(block_with_no_spaces): " + str(calc_R(entropy(block_with_no_spaces, 2), alphabet_nospace)))
# print(char_frequency_spaces)
with open("char_frequency.txt", 'w', encoding='utf-8') as f:
    for key, value in char_frequency_spaces.items():
        f.write('%s : %s\n' % (key, value))
with open("char_frequency_no_spaces.txt", 'w', encoding='utf-8') as f:
    for key, value in char_frequency_no_spaces.items():
        f.write('%s : %s\n' % (key, value))
with open("block_bigrams.txt", 'w', encoding='utf-8') as f:
    for key, value in block_bigrams.items():
        f.write('%s : %s\n' % (key, value))
with open("slide_bigrmas.txt", 'w', encoding='utf-8') as f:
    for key, value in slide_bigrmas.items():
        f.write('%s : %s\n' % (key, value))
with open("block_with_no_spaces.txt", 'w', encoding='utf-8') as f:
    for key, value in block_with_no_spaces.items():
        f.write('%s : %s\n' % (key, value))
with open("slide_with_no_spaces.txt", 'w', encoding='utf-8') as f:
    for key, value in slide_with_no_spaces.items():
        f.write('%s : %s\n' % (key, value))