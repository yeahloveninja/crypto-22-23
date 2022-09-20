import re
import math

with open('sample_text.txt', 'r') as f:
    text = f.read()


#фільтрація тексту, повертає текст з пробілами 
def filter_text(text):
    text = re.sub(r'[^а-яА-Я ]', '', text).replace("  ", " ").lower()
    return text

text = filter_text(text)
text_no_spaces = text.replace(" ", "")

#підрахунок символів
def char_count(text):
    char_counter = {}

    for char in text:
        char_counter.setdefault(char, 0)
        char_counter[char] += 1

    char_counter = dict(sorted(char_counter.items(), key=lambda x: x[1], reverse=True))
    return char_counter


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


slide_bigrmas = [text[i:i+2] for i in range(0, len(text), 1)]
block_bigrams = [text[i:i+2] for i in range(0, len(text), 2)]
slide_bigrmas_no_spaces = [text_no_spaces[i:i+2] for i in range(0, len(text_no_spaces), 1)]
block_bigrams_no_spaces = [text_no_spaces[i:i+2] for i in range(0, len(text_no_spaces), 2)]

#рахуємо h2
def calc_h2(bigrams):
    bigrams_length = len(bigrams)
    unique_bigrams = set(bigrams)
    probabilities = {}

    for i in unique_bigrams:
        probabilities[i] = ('{:.4f}'.format(bigrams.count(i)/bigrams_length))
    probabilities = dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
    h2 = 0
    for i in probabilities.values():
        if float(i) <= 0:
            continue
        h2 += -float(i) * math.log2(float(i))

    h2 = round((h2 / 2), 3)
    print(f"H2 = {h2}")

    
calc_h1(text)
calc_h1(text_no_spaces)
calc_h2(slide_bigrmas)
calc_h2(block_bigrams)
calc_h2(slide_bigrmas_no_spaces)
calc_h2(block_bigrams_no_spaces)