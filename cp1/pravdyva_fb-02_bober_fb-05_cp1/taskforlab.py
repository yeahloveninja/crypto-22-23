import math
import os
from change import change_sym
from decimal import Decimal
from collections import OrderedDict

resultpath = os.getcwd() + r'\result.txt'

def LetterFrequency(text, alphabet): # Підрахунок частоти букв у документі
    pair_LA = {}  
    for lett in alphabet:
        pair_LA[lett] = 0
    for lett in text:
        pair_LA[lett] += 1
    
    pair_LF = {} 
    for lett in alphabet:
        pair_LF[lett] = round((pair_LA[lett])/len(text), 5) # Обчислюємо частоту букв (ділимо кількість входжень символа на загальну)
        
    return OrderedDict(sorted(pair_LF.items(), key = lambda x: x[1], reverse=True))

def BigramFrequency(text, alphabet, cross = True): # Підрахунок частоти біграм
    pair_BA = {}
    pair_BF = {}  # Об'єкт {біграма: кількість}
    for lett1 in alphabet:
        for lett2 in alphabet:
            key = lett1 + lett2
            pair_BA[key] = 0
    if (cross == True): #H1
        i = 0    
        while i < len(text)-1:
            key = text[i] + text[i+1]
            pair_BA[key] += 1
            i += 1

        for key in pair_BA.keys():
            pair_BF[key] = round(Decimal(pair_BA[key])/Decimal((len(text)-1)), 5)
            
    else: #H2
        if len(text)%2 == 1:
            text += "о"
        i = 0
        while i < len(text) - 1:
            key = text[i] + text[i+1]
            pair_BA[key] += 1
            i += 2

        for key in pair_BA.keys():
            pair_BF[key] = round(Decimal(pair_BA[key])/Decimal((len(text)/2)), 5)

    return pair_BF
   
def Entropy(Dict, n):
    Entr = 0
    for key in Dict.keys():
        if Dict[key] != 0:
            Entr = Entr + (float(Dict[key]) * math.log2(1/Dict[key])/n)
            
    return Entr

def redundancy(entropy, alphabet):
    return 1 - (entropy/math.log2(len(alphabet)))

def MakeTable(Data, alphabet):
    table = {}
    table[0] = list(" " + alphabet)
    for i in range(1, len(alphabet)+1):
        table[i] = list(alphabet[i - 1])

    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            table[i + 1] = table[i + 1] + [(Data[alphabet[i] + alphabet[j]])]
    for i in range(0, len(alphabet)+1):
        Temp = ""
        for j in range(len(table[i])):
            Temp += str(table[i][j]) + (5 - len(str(table[i][j]))) * " "
        table[i] = Temp[0:len(Temp)]

    Temp = ""

    for i in range(len(table)):
        Temp += str(table[i]) + "\n"
    Table = Temp
    with open(resultpath, 'a') as res:
        res.write(Table)

def main_function(path, alphabet):

    n_p = os.getcwd() + r'\text_after.txt'
    with open(n_p) as file:
        text = file.read()
        file.seek(0)

    sorted_lf = LetterFrequency(text, alphabet)
    Mono_Entr = Entropy(sorted_lf, 1)
    with open(resultpath, 'a') as res:
        for i in sorted_lf:
            sorted_lf[i] = '{:f}'.format(sorted_lf[i])
            res.write(str(i)+':'+str(sorted_lf[i])+'\n')

    with open(resultpath, 'a') as res:
        res.write('H letter: ' + str(Mono_Entr) + '\n')
        res.write('R letter: ' + str(redundancy(Mono_Entr, alphabet)) + '\n')

    bf_cross = BigramFrequency(text, alphabet, True)
    BiCEntr = Entropy(bf_cross, 2)
    MakeTable(bf_cross, alphabet)

    with open(resultpath, 'a') as res:
        res.write('H cross bigrams: ' + str(BiCEntr) + '\n')
        res.write('R cross bigrams: ' + str(redundancy(BiCEntr, alphabet)) + '\n')

    bf = BigramFrequency(text, alphabet, False)
    BiEntr = Entropy(bf, 2)
    MakeTable(bf, alphabet)

    with open(resultpath, 'a') as res:
        res.write('H non-cross bigrams: ' + str(BiEntr) + '\n')
        res.write('R non-cross bigrams: ' + str(redundancy(BiEntr, alphabet)) + '\n')



if __name__ == '__main__':
    path = os.getcwd() + r'\initial_text.txt'

    with open(resultpath, 'w') as res:
        res.write('Результати з пробілами\n')
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
    change_sym(path, True)  
    main_function(path, alphabet)

    with open(resultpath, 'a') as res:
        res.write('\n\n\nРезультати без пробілів\n')
    alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    change_sym(path, False)
    main_function(path, alpha)
    
    

    