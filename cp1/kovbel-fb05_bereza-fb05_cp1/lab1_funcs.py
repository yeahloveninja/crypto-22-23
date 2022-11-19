import math

#freq of every letter in random_text
def freq(random_text):
    freq_num = {}
    for i in random_text:
        if i in freq_num:
            freq_num[i] += 1
        else:
            freq_num[i] = 1
    for letter in freq_num:
        freq_num[letter] = freq_num[letter]/len(random_text)
    return freq_num

#freq of bigram in random_text
def bigram_freq(random_text, cross = True):
    bigram_num = {}
    #H1 crosssed pairs (на,чи,мо,ст) etc.
    if (cross == True):
        for i in range(len(random_text)-1):
            if random_text[i:i + 2] in bigram_num:
                bigram_num[random_text[i:i+2]] += 1
            else:
                bigram_num[random_text[i:i+2]] = 1
    #H2 two letters each (на,чи,мо,ст) etc.
    else:
        if len(random_text) % 2 == 1:
            random_text += "й" # for parity elems in text
        for i in range(0, len(random_text)-1, 2):
            if random_text[i:i + 2] in bigram_num:
                bigram_num[random_text[i:i + 2]] += 2
            else:
                bigram_num[random_text[i:i + 2]] = 2
    #freq bigram
    for res in bigram_num:
        bigram_num[res] = bigram_num[res]/len(random_text)
    return bigram_num

#determ of entropy
def entropy(freq_num, n):
    entr_list = []
    for i in freq_num.keys():
        if freq_num[i] != 0:
            en = abs(float(freq_num[i]) * math.log2(freq_num[i])/n)
            entr_list.append(en)
    entropy = sum(entr_list)
    return entropy