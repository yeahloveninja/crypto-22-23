import re 
import collections
import pandas as pd
import math
import numpy as np

#--- Очищення тексту від непотрібних символів ---

print("/// Тест з пробілами чи без? ///")
userInput = input("+ з пробілами, - без пробілів: ")

file = open("./lab1.TXT").read()
file = file.lower()
file = file.replace("\n","")

if userInput == "+":
    clearString = re.sub(r'[^\w\s]+|[\d]+|_+', '',file).strip()
    clearString = re.sub(r'[\s\s]+', " ", clearString)
    clearString = re.sub(r'[\s\s]+', " ", clearString)
    clearString = re.sub(r'[\s\s]+', " ", clearString)
else:
    clearString = re.sub(r'[\W\s]+|[\d]+|_+', '',file).strip()

letter = sorted(clearString)
print(clearString)

#--- Кількість та частота появи літер ---

alphabet = []    
for i in range(0,len(letter)):
    alphabet.append(letter[i])
    
print("\n/// Словник, де ключ - це літера, а значення - кількість цієї літери в тексті ///")
alphabetDict = dict(collections.Counter(alphabet))
print(alphabetDict)
print("\n/// Частота появи кожної літери алфавіту в тексті ///")
frequency = {k: alphabetDict[k] / len(letter) for k in alphabetDict}
print(frequency)

#--- Вивід кількості літер у вигляді датафрейму ---

alphabetFiltred = sorted(alphabetDict, key=lambda x : alphabetDict[x], reverse=1) 

letterAmount = []
for i in range(0,len(alphabetFiltred)):
    letterAmount.append(alphabetDict[alphabetFiltred[i]])

df = pd.DataFrame(index = alphabetFiltred)
df['Кількість у тексті'] = letterAmount
df = df.rename(index={" ": "пробіл"})
print("\n", df.head(10))


#--- Вивід частоти появи літер ---

frequencyFiltred = sorted(frequency, key=lambda x : alphabetDict[x], reverse=1) 

letterFrequency = []
for i in range(0,len(alphabetFiltred)):
    letterFrequency.append(frequency[alphabetFiltred[i]])
   
df2 = pd.DataFrame(index = alphabetFiltred)
df2['Частота'] = letterFrequency
df2 = df2.rename(index={" ": "пробіл"})
print("\n", df2.head(10))


#--- Пошук біграм, підрахунок їх кількості та частоти появи ---

file = clearString
bigram = []
bigramUncrossed = []
for i in range(0, len(file)-1):
    bigram.append(file[i]+file[i+1])
    
for i in range(0, len(file)-2, 2):
    bigramUncrossed.append(file[i]+file[i+1])


bigramAmount = dict(collections.Counter(bigram))

bigramFrequency = {k: bigramAmount[k] / len(bigram) for k in bigramAmount}


bigramUncrossedAmount = dict(collections.Counter(bigramUncrossed))
bigramUncrossedFrequency = {k: bigramUncrossedAmount[k] / len(bigramUncrossed) for k in bigramUncrossedAmount}

#--- H1 ---

preH1 = []
for f in frequency.values():
    preH1.append(-f*math.log(f,2))
preH1 = sorted(preH1, reverse = 1)
H1 = sum(preH1)  
print("\n/// Ентропія:", H1, "///")  

#--- H2 ---

def specific_entropy(bigram,bigramFrequency):
    preH2 = []
    for f in bigramFrequency.values():
        preH2.append(-f*math.log(f,2))
    preH2 = sorted(preH2)
    H2 = sum(preH2)/2
    return H2
  
H2_Crossed = specific_entropy(bigram,bigramFrequency) 
H2_Uncrossed = specific_entropy(bigramUncrossed,bigramUncrossedFrequency) 

print("/// Питома ентропія на символ пересічної біграми:", H2_Crossed, "///")
print("/// Питома ентропія на символ непересічної біграми:", H2_Uncrossed, "///")


alphabetFiltred = sorted(alphabetFiltred)
alphabetFiltred.insert(-27, "ё")
alphabetFiltred.pop()

df3 = pd.DataFrame(index = alphabetFiltred, columns=alphabetFiltred)

bigramList = []

for i in alphabetFiltred:
    for j in alphabetFiltred:
        bigramList.append(i+j)
 
n = 0
for i in range(0,len(alphabetFiltred)):
    df3[alphabetFiltred[i]] = bigramList[n:len(alphabetFiltred)+n]
    n = len(alphabetFiltred)+n
    
df3 = df3.T

for i in list(bigramFrequency.keys()):
    x,y = np.where(df3 == i)
    df3.iloc[x,y] = bigramFrequency[i]

for i in bigramList:
    x,y = np.where(df3 == i)
    df3.iloc[x,y] = 0
    
if " " in df3.index:
    df3 = df3.rename(index={" ": "пробіл"}, columns={" ": "пробіл"})

print("\n/// Таблиця частот пересічних біграм ///")
print(df3)


df4 = pd.DataFrame(index = alphabetFiltred, columns=alphabetFiltred)
    
n = 0
for i in range(0,len(alphabetFiltred)):
    df4[alphabetFiltred[i]] = bigramList[n:len(alphabetFiltred)+n]
    n = len(alphabetFiltred)+n
    
df4 = df4.T

for i in list(bigramUncrossedFrequency.keys()):
    x,y = np.where(df4 == i)
    df4.iloc[x,y] = bigramUncrossedFrequency[i]

for i in bigramList:
    x,y = np.where(df4 == i)
    df4.iloc[x,y] = 0
    
if " " in df4.index:
    df4 = df4.rename(index={" ": "пробіл"}, columns={" ": "пробіл"})

print("\n/// Таблиця частот непересічних біграм ///")
print(df4)

H0 = math.log(32,2)
temp101 = 1.895429108
temp102 = 2.621338130
R101 = 1 - temp101 / H0
R102 = 1 - temp102 / H0
print("R10min", R101)
print("R10max", R102)
temp201 = 1.895935004
temp202 = 2.636216938
R201 = 1 - temp201 / H0
R202 = 1 - temp202 / H0
print("R20min", R201)
print("R20max", R202)
temp301 = 1.558360800
temp302 = 2.261537094
R301 = 1 - temp301 / H0
R302 = 1 - temp302 / H0
print("R30min", R301)
print("R30max", R302)




if "пробіл" in df.index:
    df.to_excel("Amount_with_space.xlsx")
    df2.to_excel("Frequency_with_space.xlsx")
    df3.to_excel("Bigram_Crossed_Frequency_with_space.xlsx")
    df4.to_excel("Bigram_Uncrossed_Frequency_with_space.xlsx")
else:
    df.to_excel("Amount_without_space.xlsx")
    df2.to_excel("Frequency_without_space.xlsx")
    df3.to_excel("Bigram_Crossed_Frequency_without_space.xlsx")
    df4.to_excel("Bigram_Uncrossed_Frequency_without_space.xlsx")
        








