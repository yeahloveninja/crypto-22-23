import re
import math


def find_entropy(frequency: dict, n: int):
    entropy = 0
    for f in frequency.values():
        if f != 0:
            entropy += - f * math.log(f, 2)
    entropy *= 1 / n
    return entropy


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
    if bi is True:
        new_text = ''
        for i in target_text[0::2]:
            new_text += i
        find_results = re.findall(r'\w\w', new_text)
        for ngram in find_results:
            if ngram not in ready_chars:
                count_ngram = re.findall(f'{ngram}', new_text)
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


monogram_with_space = find_ngram(text_with_space, False)
dictionary_monogram_sort = {}
keys_sort = sorted(monogram_with_space, key=monogram_with_space.get)

for i in keys_sort:
    dictionary_monogram_sort[i] = monogram_with_space[i]


sorted_monogram = dict(reversed(list(dictionary_monogram_sort.items())))
print(sorted_monogram)
for i in sorted_monogram:
    print(f'{i} - {sorted_monogram[i]}')

monogram_with_space_entropy = find_entropy(monogram_with_space, 1)
monogram_without_space = find_ngram(text_without_space, False)
monogram_without_space_entropy = find_entropy(monogram_without_space, 1)
print(f'h1 with space - {monogram_with_space_entropy}')
print(f'r1 with space - {r_calculate(monogram_with_space_entropy, 34)}')
print(f'h1 without space - {monogram_without_space_entropy}')
print(f'r1 without space - {r_calculate(monogram_with_space_entropy, 33)}')

bigram_with_space = find_ngram(text_with_space, True)
dictionary_bigram_sort = {}
keys_sort = sorted(bigram_with_space, key=bigram_with_space.get)

for i in keys_sort:
    dictionary_bigram_sort[i] = bigram_with_space[i]


sorted_bigram = dict(reversed(list(dictionary_bigram_sort.items())))
print(sorted_bigram)
for i in sorted_bigram:
    print(f'{i} - {sorted_bigram[i]}')


bigram_with_space_entropy = find_entropy(bigram_with_space, 2)
bigram_without_space = find_ngram(text_without_space, True)
bigram_without_space_entropy = find_entropy(bigram_without_space, 2)

print(f'h2 with space - {bigram_with_space_entropy}')
print(f'r2 with space - {r_calculate(bigram_with_space_entropy, 34)}')
print(f'h2 without space - {bigram_with_space_entropy}')
print(f'r2 without space - {r_calculate(bigram_without_space_entropy, 33)}')