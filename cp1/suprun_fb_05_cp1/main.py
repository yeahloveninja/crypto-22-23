from collections import Counter
import pandas as pd
import re
import math








row_file = 'text.txt'
with open(row_file, mode='r', encoding='utf-8') as file:
    text = file.read()
alphavit = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '


#filtering

def filter_with_space(text):
    text = re.sub('[^а-я]+', ' ', text.lower().rstrip())
    return text

def filter_without_space(text):
    text = re.sub('[^а-я]+', '', text.lower().rstrip())
    return text



#frequency_counting

def letter_frequency(text, mode): #filter with space if mode == 1
    if mode == 1:
        answer = Counter(filter_with_space(text))
        for i in answer:
            answer[i] = answer[i] / len(filter_with_space(text))
    else:
        answer = Counter(filter_without_space(text))
        for i in answer:
            answer[i] = answer[i]/len(filter_without_space(text))
    return answer

# cross = True
def bigram_frequency(text, mode): #filter with space if mode == 1
    answer = {}
    bigram_list = []
    if mode == 1:
        text = filter_with_space(text)
    else:
        text = filter_without_space(text)

    for i in range(0, len(text) - 1):
        bigram = f'{text[i] + text[i + 1]}'
        bigram_list.append(bigram)

    for i in bigram_list:
        if i not in answer:
            answer[i] = answer.setdefault(i, 0)

    for i in bigram_list:
        temp = answer.get(i)
        temp += 1
        answer.update({i: temp})

    for i in answer:
        answer[i] = answer[i]/len(bigram_list)



        #answer[i] = answer.setdefault(i, 0)
    # for i in answer:
    #     answer[i] = answer[i]/len(answer)
    return answer


# cross = False

def bigram_frequency_2(text, mode): #filter with space if mode == 1
    answer = {}
    bigram_list = []
    if mode == 1:
        text = filter_with_space(text)
    else:
        text = filter_without_space(text)

    for i in range(0, len(text) - 1, 2):
        bigram = f'{text[i] + text[i + 1]}'
        bigram_list.append(bigram)

    for i in bigram_list:
        if i not in answer:
            answer[i] = answer.setdefault(i, 0)

    for i in bigram_list:
        temp = answer.get(i)
        temp += 1
        answer.update({i: temp})

    for i in answer:
        answer[i] = answer[i] / len(bigram_list)
    return answer

def h_count(text_with_frequencies, mode ): #рахуємо ентропію
    h = 0
    all_frequencies = []
    for i in text_with_frequencies:
        all_frequencies.append(text_with_frequencies[i])
    for i in all_frequencies:
        h += round(-i * math.log2(i), 3)
    if mode == 1:
        h = h/2
    else:
        h = h
    return h



def to_excel(dictionary, name_of_file, sort_mode):
    if sort_mode == 1:
        dictionary = {k: v for k, v in sorted(dictionary.items())} #sorted
    else:
        dictionary = {k: v for k, v in sorted(dictionary.items(), key=lambda v: v[1], reverse=True)}  # sorted
    keys = []
    values = []
    for i in dictionary:
        keys.append(i)
        values.append(dictionary[i])
    new_dict = {'name': keys, 'amount': values}

    df = pd.DataFrame(new_dict)
    df = df.to_excel(name_of_file, index=False)









#test field


#with spaces
print('With spaces:')
print(letter_frequency(text, 1)) # частотта літер у тексті
print(bigram_frequency(text, 1)) # частотта біграм у тексті, які перетинаються
print(bigram_frequency_2(text, 1))  # частотта біграм у тексті, які не перетинаються з кроком 2

print(h_count(letter_frequency(text, 1), 2)) # ентропія літер у тексті
print(h_count(bigram_frequency(text, 1), 1)) # ентропія біграм у тексті, які перетинаються
print(h_count(bigram_frequency_2(text, 1), 1)) # ентропія біграм у тексті, які не перетинаються з кроком 2
#
print('-' * 1000)# separator
#
# without spaces
print('Without spaces:')
print(letter_frequency(text, 2)) # частотта літер у тексті
print(bigram_frequency(text, 2)) # частотта біграм у тексті, які перетинаються
print(bigram_frequency_2(text, 2))  # частотта біграм у тексті, які не перетинаються з кроком 2

print(h_count(letter_frequency(text, 2), 2)) # ентропія літер у тексті
print(h_count(bigram_frequency(text, 2), 1)) # ентропія біграм у тексті, які перетинаються
print(h_count(bigram_frequency_2(text, 2), 1)) # ентропія біграм у тексті, які не перетинаються з кроком 2


to_excel(letter_frequency(text, 1), 'output_with_spaces_letters.xlsx', 1)
to_excel(bigram_frequency(text, 1), 'output_with_spaces_bigrams.xlsx', 2)
to_excel(bigram_frequency_2(text, 1), 'output_with_spaces_bigrams_step2.xlsx', 2)

to_excel(letter_frequency(text, 2), 'output_without_spaces_letters.xlsx', 1)
to_excel(bigram_frequency(text, 2), 'output_without_spaces_bigrams.xlsx', 2)
to_excel(bigram_frequency_2(text, 2), 'output_without_spaces_bigrams_step2.xlsx', 2)







# print(letter_frequency(text, 2))
#print(text)
# print(bigram_frequency(text, 2))
# print(bigram_frequency_2(text, 2))
# print("entropy")
# print(h_count(bigram_frequency(text,2)))
#
# print(h_count(bigram_frequency_2(text,2)))
# print(bigram_frequency_2(text, 2))






file.close()