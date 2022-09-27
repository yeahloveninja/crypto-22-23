# -*- coding: cp1251 -*-
#в мене були проблеми з кодуванням в VS і допомогло те що вище, якщо у вас таких проблем нема краще прирбрати його

import re 
import math
#import pandas as pd
# func for editing text 
def txteditor(file_name):
    with open(file_name, 'r', encoding='utf-8') as file: #open your file -> read text -> close
        txt = file.read().lower()
        file.close()
    txt2 = " ".join(txt.split())
    txt_withspaces = re.sub( r'[^а-яё ]', '', txt2).replace("  ", " ").replace(" ", "_") # all editing stuff like removing spaces and symbols, we also replace a simple space with this symbol _ 
    txt_withoutspaces = re.sub( r'[^а-яё]', '', txt2) #
    with open('spaces.txt', 'w', encoding='utf-8') as file:
        file.write(txt_withspaces)
        file.close()
    with open('nospaces.txt', 'w', encoding='utf-8') as file:
        file.write(txt_withoutspaces)
        file.close()

def monofrequency(text):
    freq = {}; 
    for i in text: #everything is simple - looking in our text-> add index 1 or +1
        if i not in freq:
            freq[i] = 1
        else:
            freq[i] +=1
    for x in freq:
        freq[x] = round(freq[x]/len(text), 6) # calculating frequency
    freq = dict(sorted(freq.items())) # just sorting. we can use it or simply remove
    return freq

def bifrequency(text, cross):
    freq = {} # same case as with monofrequency
    if cross == 'y': # y - calculating cross bigramms, n - calculating simple bigramms
        for i in range(0, len(text)-1): 
            if text[i:i+2] not in freq:
                freq[text[i:i+2]] = 1 #taking two letters
            else:
                freq[text[i:i+2]] += 1
        for x in freq:
            freq[x] = round(freq[x]/(len(text)-1),8) #i use round because numbers are too big
    elif cross == 'n':  # same case as above 
        for i in range(0, len(text)-1, 2): # step 2 
            if text[i:i+2] not in freq:
                freq[text[i:i+2]] = 1
            else:
                freq[text[i:i+2]] += 1
        for x in freq:
            freq[x] = round(freq[x]/int((len(text)-1)/2),8)
    freq = dict(sorted(freq.items())) # sorting, better remove in order the output of bigramms was more understandable
    return freq

def print_entropy(freq, n): # calculating entropy like in example
    ans = 0
    for i in freq.values():
        ans += - i * math.log(i, 2)
    ans *= 1 / n
    return ans

def print_R(h, total): # calculating R like in example
    ans = 1 - (h/math.log2(total))
    return ans

#norm_rualphabet = 33 - для себе аби не забути кількість
#space_rualphabet = 34

# lets edit our txt file 
txteditor('badtxt.txt')
file1 = open('spaces.txt', encoding = 'utf-8')
spacetext = file1.read()
file1.close()
#we open -> read text in var -> close (both cases are the same)
file2 = open('nospaces.txt', encoding = 'utf-8')
nospacetext = file2.read()
file2.close()

#starting with spacetext
print("*********** Here is the full analysis of text with spaces ***********")
#for mono 
x1 = monofrequency(spacetext)
print("----Frequency of each letter in the text(including space):\n", x1) 
x2 = print_entropy(x1,1)
print("-----H1:\n", x2)
x3 = print_R(x2, 34)
print("-----R:\n", x3)
#for cross bi
x4 = bifrequency(spacetext, 'y')
print("----Frequency of cross bigramms:\n", x4) 
x5 = print_entropy(x4,2)
print("-----H2:\n", x5)
x6 = print_R(x5, 34)
print("-----R:\n", x6)
# for simple bi
x7 = bifrequency(spacetext, 'n')
print("----Frequency of simple bigramms:\n", x7) 
x8 = print_entropy(x7,2)
print("-----H2:\n", x8)
x9 = print_R(x8, 34)
print("-----R:\n", x9)

#without spaces 
print("\n*********** Here is the full analysis of text without spaces ***********")
#for mono 
y1 = monofrequency(nospacetext)
print("----Frequency of each letter in the text:\n", y1) 
y2 = print_entropy(y1,1)
print("-----H1:\n", x2)
y3 = print_R(y2, 33)
print("-----R:\n", y3)
#for cross bi
y4 = bifrequency(nospacetext, 'y')
print("----Frequency of cross bigramms:\n", y4) 
y5 = print_entropy(y4,2)
print("-----H2:\n", y5)
y6 = print_R(y5, 33)
print("-----R:\n", y6)
# for simple bi
y7 = bifrequency(nospacetext, 'n')
print("----Frequency of simple bigramms:\n", y7) 
y8 = print_entropy(y7,2)
print("-----H2:\n", y8)
y9 = print_R(y8, 33)
print("-----R:\n", y9)

#далі закоментований код який не дуже потрібний в цій роботі, він лише допомогав мені переносити дані в таблиці 

#a1 = pd.DataFrame(x1.values(),index=x1.keys())
#a1.to_excel("mono_space.xlsx")
#a2 = pd.DataFrame(x4.values(),index=x4.keys())
#a2.to_excel("crossbi_space.xlsx")
#a3 = pd.DataFrame(x7.values(),index=x7.keys())
#a3.to_excel("bi_space.xlsx")

#b1 = pd.DataFrame(y1.values(),index=y1.keys())
#b1.to_excel("mono_nospace.xlsx")
#b2 = pd.DataFrame(y4.values(),index=y4.keys())
#b2.to_excel("crossbi_nospace.xlsx")
#b3 = pd.DataFrame(y7.values(),index=y7.keys())
#b3.to_excel("bi_nospace.xlsx")



