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
    total_count = 0
    ngram_dict = {}

    if bi:
        check = 2
    else:
        check = 1

    counter = 1
    target_text = list(target_text)
    for ne_i_5 in range(len(target_text))[1:]:
        if counter % check == 0:
            if bi:
                current_gram = str(target_text[ne_i_5-1]) + str(target_text[ne_i_5])
            else:
                current_gram = str(target_text[ne_i_5])
            if current_gram in ngram_dict:
                ngram_dict[current_gram] += 1
                total_count += 1
            else:
                ngram_dict[current_gram] = 1
                total_count += 1
        counter += 1
    for ngram in ngram_dict:
        ngram_dict[ngram] = round(ngram_dict[ngram]/total_count, 6)

    return ngram_dict


def find_ngram_with_intersection(target_text: str):
    ready_chars = []
    find_results = re.findall(r'\w\w', target_text)
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

monogram = 1
bigram = 2

alpha_with_space = 34
alpha_without_space = 33

text_with_space = open("2.txt", 'r').read()
text_without_space = open("3.txt", 'r').read()

mono_gram_with_space = find_ngram(text_with_space, False)
mono_gram_without_space = find_ngram(text_without_space, False)
mono_gram_with_space_entropy = find_entropy(mono_gram_with_space, monogram)
mono_gram_without_space_entropy = find_entropy(mono_gram_without_space, monogram)
print(f"mono_gram_with_space_entropy - {mono_gram_with_space_entropy}")
print(f"R mono_gram_with_space - {r_calculate(mono_gram_with_space_entropy, alpha_with_space)}")
print(f"mono_gram_without_space_entropy - {mono_gram_without_space_entropy}")
print(f"R mono_gram_without_space - {r_calculate(mono_gram_without_space_entropy, alpha_without_space)}")


bi_gram_with_space = find_ngram(text_with_space, True)
bi_gram_without_space = find_ngram(text_without_space, True)
bi_gram_with_space_entropy = find_entropy(bi_gram_with_space, bigram)
bi_gram_without_space_entropy = find_entropy(bi_gram_without_space, bigram)
print(f"bi_gram_with_space_entropy - {bi_gram_with_space_entropy}")
print(f"R bi_gram_with_space - {r_calculate(bi_gram_with_space_entropy, alpha_with_space)}")
print(f"bi_gram_without_space_entropy - {bi_gram_without_space_entropy}")
print(f"R bi_gram_without_space - {r_calculate(bi_gram_without_space_entropy, alpha_without_space)}")

bi_gram_with_space_with_intersection = find_ngram_with_intersection(text_with_space)
bi_gram_without_space_with_intersection = find_ngram_with_intersection(text_without_space)
bi_gram_with_space_with_intersection_entropy = find_entropy(bi_gram_with_space_with_intersection, bigram)
bi_gram_without_with_intersection_space_entropy = find_entropy(bi_gram_without_space_with_intersection, bigram)
print(f"bi_gram_with_space_entropy_with_intersection - {bi_gram_with_space_with_intersection_entropy}")
print(f"R bi_gram_with_space_with_intersection - {r_calculate(bi_gram_with_space_with_intersection_entropy, alpha_with_space)}")
print(f"bi_gram_without_space_entropy_with_intersection - {bi_gram_without_with_intersection_space_entropy}")
print(f"R bi_gram_without_space_with_intersection - {r_calculate(bi_gram_without_with_intersection_space_entropy, alpha_without_space)}")

# for i in list(bi_gram_with_space_with_intersection.keys())[:15]:
#     print(f"{i} - {bi_gram_with_space_with_intersection[i]}")
# print('--------------------------')
# for i in list(bi_gram_without_space_with_intersection.keys())[:15]:
#     print(f"{i} - {bi_gram_without_space_with_intersection[i]}")
