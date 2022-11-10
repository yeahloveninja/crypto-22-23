import math
import xlsxwriter
import re

from xlsxwriter import Workbook


def read_file(text_path, include_whitespaces):
    text_file = open(text_path, encoding="utf-8").read()
    text_file = re.sub(r'[^а-яА-Я ]', '', text_file).replace("  ", " ").lower()
    if not include_whitespaces:
        text_file = text_file.replace(" ", "")
    text_file = list(text_file)
    return text_file


def count_letters(text_file, letter):
    letter_counter = 0
    for l in range(len(text_file)):
        if text_file[l] == letter:
            letter_counter += 1
    return letter_counter


def count_bigrams(text_file, letter1, letter2):
    bigram_counter = 0
    for index, letter in enumerate(text_file):
        if index - 1 >= 0 and index + 1 < len(text_file):
            current_letter = letter
            next_letter = text_file[index + 1]
            if current_letter == letter1 and next_letter == letter2:
                bigram_counter += 1
    return bigram_counter


def count_letter_frequency(alphabet, text_file):
    letters_frequency_dict = {}
    text_length = len(text_file)
    for letter in range(len(alphabet)):
        letter_frequency = float(count_letters(text_file, alphabet[letter]) / text_length)
        letters_frequency_dict[alphabet[letter]] = letter_frequency
    return letters_frequency_dict


def count_bigram_frequency(alphabet, text_file, crossed_bigram):
    bigrams_frequency_dict = {}
    text_length = len(text_file)
    for index, letter in enumerate(alphabet):
        if index + 1 < len(alphabet):
            current_letter = letter
            next_letter = alphabet[index + 1]
            if not crossed_bigram:
                if (index % 2) == 0:
                    if text_length % 2 == 0:
                        bigram_frequency = count_bigrams(text_file, current_letter, next_letter) / text_length
                    else:
                        bigram_frequency = count_bigrams(text_file, current_letter, next_letter) / (text_length - 1)
                    bigram = current_letter + next_letter
                    bigrams_frequency_dict[bigram] = bigram_frequency
            else:
                bigram_frequency = count_bigrams(text_file, current_letter, next_letter) / (text_length / 2)
                bigram = current_letter + next_letter
                bigrams_frequency_dict[bigram] = bigram_frequency
    return bigrams_frequency_dict


def calculate_entropy(frequency_dict):
    entropy = 0
    for frequency in frequency_dict.items():
        f = round(frequency[1], 9)
        print(f)
        if f > 0:
            bigram_entropy = abs(f * math.log2(f))
            entropy += bigram_entropy
    return entropy



def calculate_redundancy(alphabet, entropy):
    return 1 - entropy / math.log2(len(alphabet))


def make_excel_table(dict, table_name):
    table = xlsxwriter.Workbook(table_name)
    excel_table = table.add_worksheet()
    keys = list(dict.keys())
    values = list(dict.values())
    for k in range(1, len(keys)+1):
        excel_table.write(k-1, 0, keys[k - 1])
        excel_table.write(k-1, 1, values[k - 1])
    table.close()


alphabet_1 = ["а", "б", "в", "г", "д", "е", "э", "ж", "з", "и", "ы", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
              "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я"]
alphabet_2 = ["а", "б", "в", "г", "д", "е", "э", "ж", "з", "и", "ы", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
              "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я", " "]

text_file_1 = read_file("text.txt", True)
text_file_2 = read_file("text.txt", False)

print("TEXT WITH SPACES \n")
letters_frequency_dict = count_letter_frequency(alphabet_1, text_file_1)
letters_entropy = calculate_entropy(letters_frequency_dict)
redundancy_letters = calculate_redundancy(alphabet_1, letters_entropy)
make_excel_table(letters_frequency_dict, "letter(text_with_space).xlsx")
print("\n ENTROPY = ", letters_entropy, "\n REDUNDANCY = ", redundancy_letters)

letters_frequency_dict_s = count_letter_frequency(alphabet_2, text_file_1)
letters_entropy_s = calculate_entropy(letters_frequency_dict_s)
redundancy_letters_s = calculate_redundancy(alphabet_2, letters_entropy_s)
make_excel_table(letters_frequency_dict, "letter(text_with_space).xlsx")
print("\n ENTROPY = ", letters_entropy_s, "\n REDUNDANCY = ", redundancy_letters_s)


print("\n", "NOT CROSSED BIGRAMS \t", "\n")

bigrams_frequency_dict_1 = count_bigram_frequency(alphabet_1, text_file_1, False)
entropy_bigrams_1 = calculate_entropy(bigrams_frequency_dict_1)
redundancy_bigrams_1 = calculate_redundancy(alphabet_1, entropy_bigrams_1)
make_excel_table(bigrams_frequency_dict_1, "bigrams(text_with_space).xlsx")
print("ALPHABET WITHOUT WHITESPACE \t\n", bigrams_frequency_dict_1, "\n ENTROPY = ", entropy_bigrams_1, "\n REDUNDANCY = ", redundancy_bigrams_1)

bigrams_frequency_dict_2 = count_bigram_frequency(alphabet_2, text_file_1, False)
entropy_bigrams_2 = calculate_entropy(bigrams_frequency_dict_2)
redundancy_bigrams_2 = calculate_redundancy(alphabet_2, entropy_bigrams_2)
make_excel_table(bigrams_frequency_dict_1 , "bigrams_space(text_with_space).xlsx")
print("ALPHABET WITH WHITESPACE \t\n", bigrams_frequency_dict_2, "\n ENTROPY = ", entropy_bigrams_2, "\n REDUNDANCY = ", redundancy_bigrams_2)

print("\n", " CROSSED BIGRAMS \t", "\n")

crossed_bigrams_frequency_dict_1 = count_bigram_frequency(alphabet_1, text_file_1, True)
entropy_crossed_bigrams_1 = calculate_entropy(crossed_bigrams_frequency_dict_1)
redundancy_crossed_bigrams_1 = calculate_redundancy(alphabet_1, entropy_crossed_bigrams_1)
make_excel_table(crossed_bigrams_frequency_dict_1, "crossed_bigrams(text_with_space).xlsx")

print("ALPHABET WITHOUT WHITESPACE \t\n", crossed_bigrams_frequency_dict_1, "\n ENTROPY = ", entropy_crossed_bigrams_1, "\n REDUNDANCY = ", entropy_crossed_bigrams_1)

print("\n")
crossed_bigrams_frequency_dict_2 = count_bigram_frequency(alphabet_2, text_file_1, True)
entropy_crossed_bigrams_2 = calculate_entropy(crossed_bigrams_frequency_dict_2)
redundancy_crossed_bigrams_2 = calculate_redundancy(alphabet_2, entropy_crossed_bigrams_2)
make_excel_table(crossed_bigrams_frequency_dict_2, "crossed_bigrams_space(text_with_space).xlsx")
print("ALPHABET WITH WHITESPACE \t\n", crossed_bigrams_frequency_dict_2, "\n ENTROPY = ", entropy_crossed_bigrams_2, "\n REDUNDANCY = ", entropy_crossed_bigrams_2)

print(" TEXT WITHOUT SPACES \n")
letters_frequency_dict = count_letter_frequency(alphabet_1, text_file_2)
letters_entropy = calculate_entropy(letters_frequency_dict)
make_excel_table(letters_frequency_dict, "letter(text_without_space).xlsx")

print("FOR EACH LETTER \t\n", letters_frequency_dict, "\n ENTROPY = ", letters_entropy)

print("\n", " NOT CROSSED BIGRAMS \t", "\n")

bigrams_frequency_dict_1 = count_bigram_frequency(alphabet_1, text_file_2, False)
entropy_bigrams_1 = calculate_entropy(bigrams_frequency_dict_1)
redundancy_bigrams_1 = calculate_redundancy(alphabet_1, entropy_bigrams_1)
make_excel_table(bigrams_frequency_dict_1 , "bigrams(text_without_space).xlsx")
print("ALPHABET WITHOUT WHITESPACE \t\n", bigrams_frequency_dict_1, "\n ENTROPY = ", entropy_bigrams_1, "\n REDUNDANCY = ", redundancy_bigrams_1)

print("\n")
bigrams_frequency_dict_2 = count_bigram_frequency(alphabet_2, text_file_2, False)
entropy_bigrams_2 = calculate_entropy(bigrams_frequency_dict_2)
redundancy_bigrams_2 = calculate_redundancy(alphabet_2, entropy_bigrams_2)
make_excel_table(bigrams_frequency_dict_2, "bigrams(text_without_space).xlsx")
print("ALPHABET WITH WHITESPACE \t\n", bigrams_frequency_dict_2, "\n ENTROPY = ", entropy_bigrams_2, "\n REDUNDANCY = ", redundancy_bigrams_2)

print("\n", " CROSSED BIGRAMS \t", "\n")

crossed_bigrams_frequency_dict_1 = count_bigram_frequency(alphabet_1, text_file_2, True)
entropy_crossed_bigrams_1 = calculate_entropy(crossed_bigrams_frequency_dict_1)
redundancy_crossed_bigrams_1 = calculate_redundancy(alphabet_1, entropy_crossed_bigrams_1)
make_excel_table(crossed_bigrams_frequency_dict_1, "crossed_bigrams(text_without_space).xlsx")
print("ALPHABET WITHOUT WHITESPACE \t\n", crossed_bigrams_frequency_dict_1, "\n ENTROPY = ", entropy_crossed_bigrams_1, "\n REDUNDANCY = ", entropy_crossed_bigrams_1)

print("\n")
crossed_bigrams_frequency_dict_2 = count_bigram_frequency(alphabet_2, text_file_2, True)
entropy_crossed_bigrams_2 = calculate_entropy(crossed_bigrams_frequency_dict_2)
redundancy_crossed_bigrams_2 = calculate_redundancy(alphabet_2, entropy_crossed_bigrams_2)
make_excel_table(crossed_bigrams_frequency_dict_2, "crossed_bigrams_space(text_without_space).xlsx")
print("ALPHABET WITH WHITESPACE \t\n", crossed_bigrams_frequency_dict_2, "\n ENTROPY = ", entropy_crossed_bigrams_2, "\n REDUNDANCY = ", entropy_crossed_bigrams_2)
