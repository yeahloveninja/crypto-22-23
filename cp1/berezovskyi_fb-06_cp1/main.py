import math
import re

samptext_file = open("samptext.txt", encoding="utf-8")
samptext = samptext_file.read()
samptext_file.close()

samptext = re.sub(r"[^а-яё ]", "", samptext)  # Прибираємо всі зайві елементи та пробіли
samptext = samptext.lower()
samptext_space = samptext.replace(" ", "")


# просто частота символів
def freq_letter(text):
    num = {}
    for i in text:
        if i in num:
            num[i] += 1
        else:
            num[i] = 1
    for letter in num:
        num[letter] = num[letter] / len(text)
    return num


# частота біграм
def freq_bigram(text):
    num = {}
    for i in range(len(text) - 1):
        if text[i:i + 2] in num:
            num[text[i:i + 2]] += 1
        else:
            num[text[i:i + 2]] = 1
    for res in num:
        num[res] = num[res] / len(text)
    return num


# частота кросс біграм
def bigram_freq_cross(text):
    num = {}
    for i in range(0, len(text) - 1, 2):
        if text[i:i + 2] in num:
            num[text[i:i + 2]] += 2
        else:
            num[text[i:i + 2]] = 2
    for res in num:
        num[res] = num[res] / len(text)
    return num


def entropy(num, n):
    enlist = []
    for i in num.keys():
        a = float(num[i]) * math.log2(num[i]) / n
        b = abs(a)
        enlist.append(b)
    entrop = sum(enlist)
    return entrop


alphabet_space = "абвгдеёэжзиыйклмнопрстуфхцчшщъьюя "

# Із пробілами
letter_freq1 = freq_letter(samptext)
print("Частота літер у тексті:\n ", letter_freq1)
entropy1 = entropy(letter_freq1, 1)
print("H1: ", entropy1)
redundancy1 = (1 - (entropy1 / math.log2(len(alphabet_space))))
print("Надлишковість: ", redundancy1)

bigram_freq1 = freq_bigram(samptext)
print("\nЧастота біграми у тексті:\n ", bigram_freq1)
entropy2 = entropy(bigram_freq1, 2)
print("H2: ", entropy2)
redundancy2 = (1 - (entropy2 / math.log2(len(alphabet_space))))
print("Надлишковість: ", redundancy2)

bigram_cross_freq1 = bigram_freq_cross(samptext)
print("\nЧастота перехресних біграми у тексті:\n", bigram_cross_freq1)
entropy3 = entropy(bigram_cross_freq1, 2)
print("H2: ", entropy3)
redundancy3 = (1 - (entropy3 / math.log2(len(alphabet_space))))
print("Надлишковість: ", redundancy3)

# без пробілів------------------------------------------------------

letter_freq2 = freq_letter(samptext_space)
print("\n\nБез пробілів\n")
print("Частота літер у тексті(Без):\n ", letter_freq2)
entropy_1 = entropy(letter_freq2, 1)
print("H1: ", entropy_1)
redundancy_1 = (1 - (entropy_1 / math.log2(len(alphabet_space))))
print("Надлишковість: ", redundancy_1)

bigram_freq2 = freq_bigram(samptext_space)
print("\nЧастота біграми у тексті(Без):\n", bigram_freq2)
entropy_2 = entropy(bigram_freq2, 2)
print("H2: ", entropy_2)
redundancy_2 = (1 - (entropy_2 / math.log2(len(alphabet_space))))
print("Надлишковість: ", redundancy_2)

bigram_cross_freq2 = bigram_freq_cross(samptext_space)
print("\nЧастота перехресних біграми у тексті(Без):\n", bigram_cross_freq2)
entropy_3 = entropy(bigram_cross_freq2, 2)
print("H2: ", entropy_3)
redundancy_3 = (1 - (entropy_3 / math.log2(len(alphabet_space))))
print("Надлишковість: ", redundancy_3)
