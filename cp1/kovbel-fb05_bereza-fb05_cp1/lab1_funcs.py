import math
from collections import Counter

# Frequency of every letter in random_text
def freq(random_text):
    freq_num = Counter(random_text)
    total = len(random_text)
    for letter in freq_num:
        freq_num[letter] = freq_num[letter]/total
    return freq_num

# Determine entropy
def entropy(freq_num):
    entr_list = []
    for freq in freq_num.values():
        if freq != 0:
            entr_list.append(-1 * freq * math.log2(freq))
    entropy = sum(entr_list)
    return entropy

# Frequency of bigrams in random_text
def bigram_freq(random_text, cross=True):
    bigram_num = {}
    # H1 crossed pairs (на,чи,мо,ст) etc.
    if cross:
        for i in range(len(random_text)-1):
            if i%2 ==0:
                if random_text[i:i + 2] in bigram_num:
                    bigram_num[random_text[i:i+2]] += 1
                else:
                    bigram_num[random_text[i:i+2]] = 1
    # H2 two letters each (на,чи,мо,ст) etc.
    else:
        for i in range(len(random_text)-1):
            if i%2 == 1:
                if random_text[i:i + 2] in bigram_num:
                    bigram_num[random_text[i:i + 2]] += 1
                else:
                    bigram_num[random_text[i:i + 2]] = 1
    for res in bigram_num:
        bigram_num[res] = bigram_num[res]/len(random_text)
    return bigram_num




