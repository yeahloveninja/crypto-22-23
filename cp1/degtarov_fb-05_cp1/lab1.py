import re
import math
import pandas as pd
import numpy as np
def nadl(e, total): 
    ans = 1 - (e/math.log2(total))
    return ans
def entropy(dictionary, n):
    entropies = []
    for k in dictionary.keys():
        if dictionary[k] != 0:
            entropies.append(abs(float(dictionary[k]) * math.log2(dictionary[k])/n))
    return sum(entropies)

def fre_of_letters(txt,alfavit):
    dictonary={}
    for l in alfavit:
        dictonary.update({l:0})
    for i in txt:
        dictonary[i]+=1
    for l in alfavit:
        dictonary.update({l:round(dictonary[l]/len(txt),5)})
    return dictonary
def fre_of_bigrams(txt, alfavit, cross = True):
    dictionary = {}
    for l1 in alfavit:
        for l2 in alfavit:
            dictionary.update({l1+l2:0})
    if cross==True:
        for i in range(len(txt)-1):
            dictionary[txt[i]+txt[i+1]]+=1
        for key in dictionary.keys():
            dictionary[key]=round(dictionary[key]/(len(txt)-1),5)
    else:
        if len(txt) % 2 == 1:
            txt += "а"  
        i = 0
        for i in range(len(txt) - 1):
            if i%2==1:
                continue
            dictionary[txt[i] + txt[i + 1]] += 1  
        for key in dictionary.keys():
            dictionary[key]=round(dictionary[key]/(len(txt)-1),5) 
    return dictionary


def main():
    
    alfavit = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'  
    alfavit_with_prob = alfavit + ' '  

    ###########################################
    file = open('1.txt',encoding='utf8')
    text = file.read().lower().replace('\n','')
    text = re.sub(r'[^а-яё ]', '', text)
    file.close()

    ###########################################
    print(f'===Обрахунки для тексту з пробілами===')
    ###########################################
    f1=fre_of_letters(text,alfavit_with_prob)
    print(f'Частота букв - {f1}')
    e_f1=entropy(f1,1)
    print(f'H1={e_f1}')
    print(f'Надлишковість = {nadl(e_f1,len(alfavit_with_prob))}')


    f11=fre_of_bigrams(text,alfavit_with_prob,True)
    print(f'Частота біграм - {f11}')
    e_f11=entropy(f11,2)
    print(f'H2={e_f11}')
    print(f'Надлишковість = {nadl(e_f11, len(alfavit_with_prob))}')

    f12=fre_of_bigrams(text,alfavit_with_prob,False)
    print(f'Частота перехресних біграм - {f11}')
    ef12=entropy(f12,2)
    print(f'H2(перехресна) = {ef12}')
    print(f'Надлишковість = {nadl(ef12, len(alfavit_with_prob))}')
    ###########################################
    print(f'===Обрахунки для тексту без пробілів===')
    ###########################################
    file = open('1.txt', encoding='utf8')
    text = file.read().lower().replace('\n', '')
    text = re.sub(r'[^а-яё ]', '', text)
    text=text.replace(' ','')
    file.close()
    ###########################################
    f2 = fre_of_letters(text, alfavit)
    print(f'Частота букв - {f2}')
    e_f2 = entropy(f2, 1)
    print(f'H1={e_f2}')
    print(f'Надлишковість = {nadl(e_f2, len(alfavit))}')

    f21 = fre_of_bigrams(text, alfavit, True)
    print(f'Частота біграм - {f21}')
    e_f21 = entropy(f21, 2)
    print(f'H2={e_f21}')
    print(f'Надлишковість = {nadl(e_f21, len(alfavit))}')
    f22 = fre_of_bigrams(text, alfavit, False)
    print(f'Частота перехресних біграм - {f21}')
    ef22 = entropy(f22, 2)
    print(f'H2(перехресна) = {ef22}')
    print(f'Надлишковість = {nadl(ef22, len(alfavit))}')
    a1=pd.DataFrame(f1.values(),index=f1.keys())
    
    a1.to_excel('first.xlsx')
    vva=np.array(list(f11.values()))
    a11=pd.DataFrame(vva.reshape((34,34)),index=f1.keys(),columns=f1.keys())
    
    a11.to_excel('second.xlsx')

    vva = np.array(list(f12.values()))
    a12 = pd.DataFrame(vva.reshape((34, 34)), index=f1.keys(), columns=f1.keys())
    
    a12.to_excel('tritd.xlsx')

    #################
    a2 = pd.DataFrame(f2.values(), index=f2.keys())
    

    a2.to_excel('forth.xlsx')
    vva = np.array(list(f21.values()))
    a21 = pd.DataFrame(vva.reshape((33, 33)), index=f2.keys(), columns=f2.keys())
    
    a21.to_excel('fifth.xlsx')
    vva = np.array(list(f22.values()))
    a22 = pd.DataFrame(vva.reshape((33, 33)), index=f2.keys(), columns=f2.keys())
    
    a22.to_excel('six.xlsx')
main()