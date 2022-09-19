import re
import math

with open('sample_text.txt', 'r') as f:
    text = f.read()


#фільтрація тексту, повертає текст з пробілами 
def filter_text(text):
    text = re.sub(r'[^\w ]', '', text).replace("  ", " ").lower()
    return text


#підрахунок символів
def char_count(text):
    char_counter = {}
    text = filter_text(text)

    for char in text:
        char_counter.setdefault(char, 0)
        char_counter[char] += 1

    #char_counter.pop(' ', None)
    char_counter = dict(sorted(char_counter.items(), key=lambda x: x[1], reverse=True))
    return char_counter

#підрахунок біграм, перехресна - type=slide, неперехресна - type=block
def bigram_count(text, type):
    bigram_counter = {}
    text = filter_text(text)
    n = 0
    if type == 'block':
        n = 2
    elif type == 'slide':
        n = 1
    for i in range(0, len(text) - 1, n):
        bigram = text[i] + text[i+1]
        bigram_counter.setdefault(bigram, 0)
        bigram_counter[bigram] += 1

    bigram_counter = dict(sorted(bigram_counter.items(), key=lambda x: x[1], reverse=True))
    return bigram_counter


#рахуємо h1
def calc_h1(text):
    text_length = len(text)
    chars = char_count(text)
    probablities = {char:round((frequency / text_length), 3) for char, frequency in chars.items()}

    h1 = 0
    for i in probablities.values():
        if i <= 0:
            continue
        h1 += round(-i * math.log2(i), 3)

    print(f"H1 = {round(h1, 3)}")

#рахуємо h2 перехресно - type=slide, неперехресно - type=block
def calc_h2(text, type):
    pass


