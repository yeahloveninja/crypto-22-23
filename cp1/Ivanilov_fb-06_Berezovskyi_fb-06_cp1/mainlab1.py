import re
from math import log2

text_var = open("some_text.txt", "r").read()

def char_get(text):
    vals = {}
    for char in text:
        vals[char] = vals.get(char, 0)
        vals[char] += 1
    return vals


def char_freq(char_get):
    charset = {}
    all_chars = sum(char_get[char] for char in char_get)
    for char in char_get:
        charset[char] = charset.get(char, 0)
        charset[char] = char_get[char] / all_chars
    return charset


def bigrams_cnt(text, step):
    cross_bigrams =[]
    vals = {}
    for i in range(0, len(text) - 1, step):
        cross_bigrams.append(text[i:i + 2])
    for bigram in cross_bigrams:
        vals[bigram] = vals.get(bigram, 0)
        vals[bigram] += 1
    return vals


def H_calc_N(text, n):
    h = sum(-text[char] * log2(text[char]) for char in text)
    return h * (1 / n)


text_wspaces = re.sub(r'[1-9.,"\'-?:–!;a-z»A-Z„n{} #°—’’%`+\f\r\v\0^\ufeff@№&…*\\\n\t“«]', '', text_var).replace("  ", " ").replace(" ", "`").replace("]", "").replace("[", "").lower()
text_wospaces = re.sub(r'[1-9.,"\'-?:–!;a-z»A-Z„n{} #°—’’%`+\f\r\v\0^\ufeff@№&…*\\\n\t“«]', '', text_var).replace(" ", "").replace("]","").replace("[","").lower()

char_freqws = char_freq(char_get(text_wspaces))
char_freqwos = char_freq(char_get(text_wospaces))
with open("character_frequencies_with_spaces.csv", 'w') as txt:
    for key, value in char_freqws.items():
        txt.write(f"{key} : {value}\n")
with open("character_frequencies_wo_space.csv", 'w') as txt:
    for key, value in char_freqwos.items():
        txt.write(f"{key} : {value}\n")

cross_bigrams = char_freq(bigrams_cnt(text_wspaces, 1))
cross_wos = char_freq(bigrams_cnt(text_wospaces, 1))
with open("crosses_bigrams.csv", 'w') as txt:
    for key, value in cross_bigrams.items():
        txt.write(f"{key} : {value}\n")
with open("crosses_wo_spaces.csv", 'w') as txt:
    for key, value in cross_wos.items():
        txt.write(f"{key} : {value}\n")

block_bigrams = char_freq(bigrams_cnt(text_wspaces, 2))
block_wos = char_freq(bigrams_cnt(text_wospaces, 2))
with open("block_bigrams.csv", 'w') as txt:
    for key, value in block_bigrams.items():
        txt.write(f"{key} : {value}\n")
with open("block_wo_spaces.csv", 'w') as txt:
    for key, value in block_wos.items():
        txt.write(f"{key} : {value}\n")

print("H1 with spaces :####: H1 w/o spaces")
print(f"{H_calc_N(char_freqws, 1)} :####: {H_calc_N(char_freqwos, 1)}", "\n")

print("R for H1 with spaces :####: R for H1 w/o spaces")
print(f"{1 - H_calc_N(char_freqws, 1)/ log2(34)} :####: {1 - H_calc_N(char_freqwos, 1) / log2(33)}", "\n")

print("H2 crossed and with spaces :####: H2 crossed and w/o spaces")
print(f"{H_calc_N(cross_bigrams, 2)} :####: {H_calc_N(cross_wos, 2)}", "\n")

print("R for H2 crossed and with spaces :####: R for H2 crossed and w/o spaces")
print(f"{1 - (H_calc_N(cross_bigrams, 2) / log2(34))} :####: {1 - H_calc_N(cross_wos, 2) / log2(33)}", "\n")

print("H2 uncrossed and with spaces :####: H2 uncrossed and w/o spaces")
print(f"{H_calc_N(block_bigrams, 2)} :####: {H_calc_N(block_wos, 2)}", "\n")

print("R for H2 uncrossed and with spaces :####: R for H2 uncrossed and w/o spaces")
print(f"{1 - H_calc_N(block_bigrams, 2) / log2(34)} :####: {1 - H_calc_N(block_wos, 2) / log2(33)}", "\n")