from collections import Counter
import pandas as pd
import math

FILE = "text.txt"
FORMATTED_FILE = "ftext.txt"
ALPH_LEN = 33
S_ALPH_LEN = 34


def format_file(file, formated_file):
    """ Gives the text an appropriate form to research """

    formatting_symbols = []
    for i in range(ord('А'), ord('я') + 1):
        formatting_symbols += chr(i)
    formatting_symbols += [' ']

    formatted_text = []
    with open(file, 'r', encoding="UTF-8") as text, open(formated_file, "w", encoding="UTF-8") as ftext:
        arr = text.read().strip()
        result = []
        for letter in arr:
            if letter == '\n':
                result += ' '
            elif letter not in formatting_symbols:
                continue
            else:
                if not (letter == ' ' and result[len(result) - 1] == ' '):
                    result += letter

        result = ''.join(result).lower().strip().split()
        ftext.write(' '.join(result))
    return


def monogram_frequency(formated_file, with_space=False):
    """ Returns top ten monograms from given text file """

    text = None
    data_header = 'With space'
    with open(formated_file, 'r', encoding="UTF-8") as ftext:
        text = ftext.read()
        if not with_space:
            text = text.replace(" ", '')
    data = Counter(text)
    data = dict(data)
    for item in data:
        data[item] = [data[item], data[item] / len(text)]
    indexes = range(1, 10)
    df = pd.DataFrame(data.values(), index=data, columns=['count', 'periodicity'])
    return df


def bigram_frequency(formated_file, with_space=False, intersection=False):
    """ Returns frequency of bigrams from given text file """
    text = None
    with open(formated_file, 'r', encoding="UTF-8") as ftext:
        text = ftext.read()
        if not with_space:
            text = text.replace(' ', '')

    unformatted_data = []
    if intersection:
        for i in range(0, len(text) - 1):
            unformatted_data.append(text[i] + text[i + 1])
    else:
        for i in range(0, len(text) - 1, 2):
            unformatted_data.append(text[i] + text[i + 1])

    bigrams_data = Counter(unformatted_data)
    bigrams = dict(bigrams_data)

    for item in bigrams:
        bigrams[item] = [bigrams[item], bigrams[item] / sum(bigrams_data.values())]
    df = pd.DataFrame(bigrams.values(), index=bigrams, columns=['count', 'periodicity'])
    return df


def top(df, amount=10):
    """ prints top elements from given datraframe by 'count' value """
    return df.nlargest(amount, 'count')


def H1(df):
    """ enthropy for monograms """
    periodicity = df['periodicity']
    h = []
    for x in periodicity.values:
        h.append(x * math.log(x, 2))
    return -sum(h)


def H2(df):
    """ enthropy for bigrams """
    periodicity = df['periodicity']
    h = []
    for x in periodicity.values:
        h.append(x * math.log(x, 2))
    return (-(sum(h)) / 2)


def excess(h, alph_len):
    return 1 - (h / math.log2(alph_len))


#
# Final results 
#

format_file(FILE, FORMATTED_FILE)
df, h1, h2, exc = [None for i in range(4)]

print("#       Monograms")
##############################################
print("#    -- With spaces --")
df = monogram_frequency(FORMATTED_FILE, True)
h1 = round(H1(df), 8)
exc = round(excess(h1, S_ALPH_LEN), 7)

print(top(df))
print(f"H1: {h1}")
print(f"Exc: {exc}\n")

print("#    -- With no spaces --")
df = monogram_frequency(FORMATTED_FILE, False)
h1 = round(H1(df), 8)
exc = round(excess(h1, ALPH_LEN), 7)
print(top(df))
print(f"H1: {h1}")
print(f"Exc: {exc}\n")

print("----------------------------------")
print("#       Bigrams (no intersection)")
##############################################
print("#    -- With spaces --")
df = bigram_frequency(FORMATTED_FILE, with_space=True, intersection=False)
h2 = H2(df)
exc = round(excess(h2, S_ALPH_LEN), 7)
print(top(df))
print(f"H2: {h2}")
print(f"Exc: {exc}\n")

print("#    -- With no spaces --")
df = bigram_frequency(FORMATTED_FILE, with_space=False, intersection=False)
h2 = H2(df)
exc = round(excess(h2, ALPH_LEN), 7)
print(top(df))
print(f"H2: {h2}")
print(f"Exc: {exc}\n")

print("#         Bigrams (intersection)")
##############################################
print("#    -- With spaces --")
df = bigram_frequency(FORMATTED_FILE, with_space=True, intersection=True)
h2 = H2(df)
exc = round(excess(h2, S_ALPH_LEN), 7)
print(top(df))
print(f"H2: {h2}")
print(f"Exc: {exc}\n")

print("#    -- With no spaces --")
df = bigram_frequency(FORMATTED_FILE, with_space=False, intersection=True)
h2 = H2(df)
exc = round(excess(h2, ALPH_LEN), 7)
print(top(df))
print(f"H2: {h2}")
print(f"Exc: {exc}\n")

# def bigram_frequency(formated_file, with_space = False, intersection = False):
#     """ Returns frequency of bigrams from given text file """
#     text = None
#     with open(formated_file, 'r') as ftext:
#         text = ftext.read()
#         if not with_space:
#             text = text.replace(' ','')

#     data = []
#     if intersection:
#         for i in range(0, len(text)-1):
#             data.append(text[i]+text[i+1])
#     else:
#         for i in range(0, len(text)-1, 2):
#             data.append(text[i]+text[i+1])

#     if not intersection: data *= 2
#     data = Counter(data)
#     data = dict(data)

#     for item in data:
#         data[item] = [data[item], data[item]/len(text)]
#     df = pd.DataFrame(data.values(), index=data, columns=['count', 'periodicity'])
#     return df
