import pandas as pd
import warnings
import xlsxwriter
from math import log2
from mpmath import *
mp.dps = 8

warnings.simplefilter(action='ignore', category=FutureWarning)

text = open('thetext.txt', encoding='utf-8', mode='r').read().lower()


for u in ["\n", "\r"]:
    text = text.replace(u, ' ')
for i in list("-01234567890!,.#;:?abcdefghijklmnopqrstuvwxyz()/_’\"«»&[]{}–…	 *<>„“—"):
    text = text.replace(i, '')
for _ in range(0, 3):
    text = text.replace("     ", " ").replace("   ", " ").replace("  ", " ")

with open('processedtext.txt', 'w') as f:
    for line in list(text):
        f.write(line)

text_without_spaces = text.replace(" ", "")
summary = amount_without_spaces = len(text_without_spaces)
amount_with_spaces = len(text)
splitted_letters = list(text)
length_spll = len(splitted_letters)


bigram_set_1 = {}  # with spaces
bigram_set_2 = {}  # without them
set_with_spaces = {}
set_without_spaces = {}


def adding(words, frequency):
    for i in words:
        if i in frequency:
            frequency[i] += 1
        else:
            frequency[i] = 1


def adding_bigram_list(array, amounts):
    length = len(array)
    for i in range(0, length):
        if i != length - 1:
            adding([array[i] + array[i+1]], amounts)
        else:
            adding([array[i] + array[-1]], amounts)
    return amounts


def replace(dictionary, sum):
    for i in dictionary.keys():
        dictionary[i] = "{:.5f}".format(dictionary[i] / sum)
    return sorted(dictionary.items(), key=lambda item: item[1], reverse=True)


def replace_bigrams(dictionary, total_bigrams):
    for k in dictionary.keys():
        total_bigrams += dictionary[k]
    for i in dictionary.keys():
        dictionary[i] = "{:.10f}".format(dictionary[i] / total_bigrams)
    return sorted(dictionary.items(), key=lambda item: item[1], reverse=True)


def count_entropy_value(dictionary):
    n = len(((list(dictionary[0]))[0]))
    result = 0
    for j in range(0, len(dictionary)):
        p = mpf(((list(dictionary[j]))[1]))
        # print(str(dictionary[j])+' '+str(p))
        result += p * log2(p)
    return -result / n


def count_redundancy(inf, zero):
    return 1 - count_entropy_value(inf) / zero


adding(text, set_with_spaces)
adding(text_without_spaces, set_without_spaces)


letter_frequency_set1 = replace(set_with_spaces, amount_with_spaces)
letter_frequency_set2 = replace(set_without_spaces, amount_without_spaces)
bigrams_frequency_set1 = replace_bigrams(adding_bigram_list(text, bigram_set_1), 0)
bigrams_frequency_set2 = replace_bigrams(adding_bigram_list(text_without_spaces, bigram_set_2), 0)

print("H:")
print(count_entropy_value(letter_frequency_set1))
print(count_entropy_value(letter_frequency_set2))
print(count_entropy_value(bigrams_frequency_set1))
print(count_entropy_value(bigrams_frequency_set2))

df = pd.DataFrame(letter_frequency_set1)
df1 = pd.DataFrame(letter_frequency_set2)
df2 = pd.DataFrame(bigrams_frequency_set1[0:10])
df3 = pd.DataFrame(bigrams_frequency_set2[0:10])

writer = pd.ExcelWriter("tables.xlsx", engine="xlsxwriter")

df.to_excel(writer, startrow=0, startcol=0, sheet_name = 'Symbols')
worksheet = writer.sheets['Symbols']
worksheet.write(0, 1, "Symbols")
worksheet.write(0, 2, "Frequency")
df1.to_excel(writer, startrow=0, startcol=0, sheet_name = 'Letters')
worksheet = writer.sheets['Letters']
worksheet.write(0, 1, "Symbols",)
worksheet.write(0, 2, "Frequency")
df2.to_excel(writer, startrow=0, startcol=0, sheet_name = 'Bigrams')
worksheet = writer.sheets['Bigrams']
worksheet.write(0, 1, "Bigrams",)
worksheet.write(0, 2, "Frequency")
df3.to_excel(writer, startrow=0, startcol=0, sheet_name = 'Bigrams_no_spaces')
worksheet = writer.sheets['Bigrams_no_spaces']
worksheet.write(0, 1, "Bigrams",)
worksheet.write(0, 2, "Frequency")

writer.save()

#  ---------------------------------------------------second part---------------------------------------

entropy_of_language = log2(33)  # takes value of H(0), 33 letters in alphabet
# R = 1 - H(inf)/H(0)
entropy_inf_letters = count_redundancy(letter_frequency_set1, entropy_of_language)  # for letters with space
entropy_inf_letters_no_spaces = count_redundancy(letter_frequency_set2, entropy_of_language)  # only letters

entropy_inf_bigrams = count_redundancy(bigrams_frequency_set1, entropy_of_language)  # same for bigrams
entropy_inf_bigrams_no_spaces = count_redundancy(bigrams_frequency_set2, entropy_of_language)  # no space

print("R:")
print(entropy_inf_letters)
print(entropy_inf_letters_no_spaces)
print(entropy_inf_bigrams)
print(entropy_inf_bigrams_no_spaces)


