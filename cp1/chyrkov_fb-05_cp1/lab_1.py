import math

text = open('text.txt', encoding="utf8").read() # відкриваю файл, та відразу записую весь текст в змінну

# Підрахувати частоту букв
def letter_frequency(space):
    len_text = 0
    letters = {}
    for i in text:
        if (i == ' ' and space == 1): # ось тут позбуваємось пробілів
            continue
        len_text += 1
        if letters.get(i) == None: # Якщо ключ ще немає значення, тобто порожній
            letters[i] = 1 # присвоюємо значення 1
        else:
            letters[i] += 1 # в усіх інших випадках до значення додаємо 1
    for i in letters:
        letters[i] = letters[i]/len_text

    return letters

# Підрахувати частоту біграм
def bigram_with_spaces(space):

    bigrams = {} # Словарь для біграм
    letter_fusion = ''# злиття букв в біграму
    j = 0 # лічильник
    len_text = 0

    for i in text: # проходимось по всьому тексту 
        if (i == ' ' and space == 1): # ось тут позбуваємось пробілів
            continue
        if j == 0 and i != None: # беремо першу букву для злиття
            letter_fusion += i 
            j = 1 # встановлюємо що перша буква додана
            continue # перестрибуваємо на наступну ітерацію бо поки в нас одна буква
        if j == 1 and i != None: # беремо другу букву
            letter_fusion += i # додаємо її
            j = 0
        else:
            break 
        len_text += 1
        if bigrams.get(letter_fusion) == None: # якщо ця біграма зустрілась вперше
            bigrams[letter_fusion] = 1 # то встановлюємо 1
        else:
            bigrams[letter_fusion] += 1 # у всіх інших випадках додаємо 1

        letter_fusion = '' 
    for i in bigrams:
        bigrams[i] = bigrams[i]/len_text
    return bigrams


def entropy_H1(dictionary):
    HZ = 0
    for i in dictionary:
        HZ -= dictionary[i] * math.log(dictionary[i], 2)
    H1 = HZ / 1
    return H1

def entropy_H2(dictionary):
    HZ = 0
    for i in dictionary:
        HZ -= dictionary[i] * math.log(dictionary[i], 2)
    H2 = HZ / 2
    return H2

def excess(dictionary,):
    Hinf = 0
    counter = 0
    for i in dictionary:
        Hinf -= dictionary[i] * math.log(dictionary[i], 2)
        counter += 1
    H0 = math.log(counter, 2)
    R = 1 - Hinf/H0
    return R

letters = letter_frequency(0)
letters_without_space = letter_frequency(1)
bigrams = bigram_with_spaces(0)
bigrams_without_space = bigram_with_spaces(1)


print (entropy_H1(letters))
print (excess(letters))
print (entropy_H1(letters_without_space))
print (excess(letters_without_space))
print (entropy_H2(bigrams))
print (excess(bigrams))
print (entropy_H2(bigrams_without_space))
print (excess(bigrams_without_space))












    
