import re
import math


def find_entropy(frequency: dict, n: int):
    entropy = 0
    for f in frequency.values():
        if f != 0:
            entropy += - f * math.log(f, 2)
    entropy *= 1 / n
    return entropy


def find_ngram_with_intersection(target_text: str):
    ready_chars = []
    total_count = 0
    ngram_dict = {}
    new_text = ''
    for ne_i in target_text[0::2]:
        new_text += ne_i
    find_results = re.findall(r'\w\w', new_text)
    for ngram in find_results:
        if ngram not in ready_chars:
            count_ngram = re.findall(f'{ngram}', new_text)
            ngram_dict[ngram] = len(count_ngram)
            total_count += len(count_ngram)
            ready_chars.append(ngram)
    for ne_i in target_text[1::2]:
        new_text += ne_i
    find_results = re.findall(r'\w\w', new_text)
    ready_chars = []
    for ngram in find_results:
        if ngram not in ready_chars:
            if ngram not in ngram_dict:
                count_ngram = re.findall(f'{ngram}', new_text)
                ngram_dict[ngram] = len(count_ngram)
                total_count += len(count_ngram)
                ready_chars.append(ngram)
            else:
                count_ngram = re.findall(f'{ngram}', new_text)
                ngram_dict[ngram] += len(count_ngram)
                total_count += len(count_ngram)
                ready_chars.append(ngram)
    for ngram in ngram_dict:
        ngram_dict[ngram] = round(ngram_dict[ngram]/total_count, 6)

    return ngram_dict


def find_ngram(target_text: str, bi: bool):
    ready_chars = []

    if bi is False:
        n = 1
    else:
        n = 2
    find_results = re.findall(r'\w' * n, target_text)
    total_count = 0
    ngram_dict = {}
    for ngram in find_results:
        if ngram not in ready_chars:
            count_ngram = re.findall(f'{ngram}', target_text)
            ngram_dict[ngram] = len(count_ngram)
            total_count += len(count_ngram)
            ready_chars.append(ngram)
    for ngram in ngram_dict:
        ngram_dict[ngram] = round(ngram_dict[ngram]/total_count, 6)

    return ngram_dict


def r_calculate(h, count):
    ans = 1 - (h/math.log2(count))
    return ans


text_with_space = open("2.txt", 'r').read()
text_without_space = open("3.txt", 'r').read()

monogram = 1
bigram = 2
alpha_with_space = 34
alpha_without_space = 33


monogram_with_space = find_ngram(text_with_space, False)
monogram_with_space_entropy = find_entropy(monogram_with_space, monogram)
monogram_without_space = find_ngram(text_without_space, False)
monogram_without_space_entropy = find_entropy(monogram_without_space, monogram)
print(f'h1 with space - {monogram_with_space_entropy}')
print(f'r1 with space - {r_calculate(monogram_with_space_entropy, alpha_with_space)}')
print(f'h1 without space - {monogram_without_space_entropy}')
print(f'r1 without space - {r_calculate(monogram_with_space_entropy, alpha_without_space)}')


bigram_with_space = find_ngram_with_intersection(text_with_space)
bigram_with_space_without_intersection = find_ngram(text_with_space, True)
bigram_with_space_without_intersection_entropy = find_entropy(bigram_with_space_without_intersection, bigram)
bigram_with_space_entropy = find_entropy(bigram_with_space, bigram)
bigram_without_space = find_ngram_with_intersection(text_without_space)
bigram_without_space_without_intersection = find_ngram(text_without_space, True)
bigram_without_space_entropy = find_entropy(bigram_without_space, bigram)
bigram_without_space_without_intersection_entropy = find_entropy(bigram_without_space_without_intersection, bigram)


print(f'h2 with space - {bigram_with_space_entropy}')
print(f'r2 with space - {r_calculate(bigram_with_space_entropy, alpha_with_space)}')
print(f'h2 with space without intersection - {bigram_with_space_without_intersection_entropy}')
print(f'r2 with space without intersection - {r_calculate(bigram_with_space_without_intersection_entropy, alpha_with_space)}')
print(f'h2 without space - {bigram_without_space_entropy}')
print(f'h2 without space without intersection - {bigram_without_space_without_intersection_entropy}')
print(f'r2 without space without intersection - {r_calculate(bigram_without_space_without_intersection_entropy, alpha_without_space)}')
print(f'r2 without space - {r_calculate(bigram_without_space_entropy, alpha_without_space)}')