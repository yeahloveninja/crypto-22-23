import math
import re
from lab1_funcs import*


rtext_file = open("rtext.txt", encoding="utf-8")
rtext = rtext_file.read()
rtext_file.close()

alphabet = "абвгдеёэжзиыйклмнопрстуфхцчшщъьюя"
alphabet_space = "абвгдеёэжзиыйклмнопрстуфхцчшщъьюя "

rtext = re.sub(r"[^а-яё ]", "", rtext)
rtext = rtext.lower()
rtext_space = rtext.replace(" ", "")
##############################################################################################

#Calc freq of letters in rtext w/ spaces
letter_freq = freq(rtext_space)
entropy_l = entropy(letter_freq)
print("\n\n\n-----------------------------------------------------------------------------")
print("\nSome calculations for rtext w/ spaces\n\n")
print("Frequency of letters in rtext: ", letter_freq)
print("H1: ", entropy_l)
print("Surplus: ", (1 - (entropy_l/math.log2(len(alphabet_space)))))

#Calc freq of bigrams in rtext w/ spaces
big_freq = bigram_freq(rtext_space, True)
entropy_b = entropy(big_freq)
print("\nFrequency of bigrams in rtext", big_freq)
print("H2: ", entropy_b)
print("Surplus: ", (1 - (entropy_b/math.log2(len(alphabet_space)))))

#Calc freq of cross bigrams in rtext w/ spaces
bigram_cross_freq = bigram_freq(rtext_space, False)
print("\nFrequency of cross bigrams in rtext", bigram_cross_freq)
entropy_cb = entropy(bigram_cross_freq)
print("H2: ", entropy_cb)
print("Surplus: ", (1 - (entropy_cb/math.log2(len(alphabet_space)))))

##############################################################################################

# Calc freq of letter for rtext w/o spaces
letter_freq = freq(rtext)
entropy_l = entropy(letter_freq)
print("\n\n\n-----------------------------------------------------------------------------\n")
print("Doing calculations for rtext w/o spaces\n\n")
print("Frequency of letters in rtext: ", letter_freq)
print("H1: ", entropy_l)
print("Surplus: ", (1 - (entropy_l/math.log2(len(alphabet)))))

# Calc freq of bigrams for rtext w/o spaces
big_freq = bigram_freq(rtext, True)
entropy_b = entropy(big_freq)
print("\nFrequency of bigrams in rtext", big_freq)
print("H2: ", entropy_b)
print("Surplus: ", (1 - (entropy_b/math.log2(len(alphabet)))))

#Calc freq of cross bigrams for rtext w/o spaces
bigram_cross_freq = bigram_freq(rtext, False)
print("\nFrequency of cross bigrams in rtext", bigram_cross_freq)
entropy_cb = entropy(bigram_cross_freq)
print("H2: ", entropy_cb)
print("Surplus: ", (1 - (entropy_cb/math.log2(len(alphabet)))))

##############################################################################################


