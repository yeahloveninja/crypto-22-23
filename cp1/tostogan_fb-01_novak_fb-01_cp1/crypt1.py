import collections
import pandas as pd
import re
import math as m
import numpy as np

symbols = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']
symbols_2 = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']

#edit text: delete punctuation marks and spaces, replace capital letters with lowercase letters

with open("/home/kali/lab1.txt", 'r', encoding='utf-8') as ofile:
	note = ofile.read()
	note = note.replace("\n","")
	note = note.lower()
	new_note1 = re.sub( r'[^а-яё]', '', note )
	new_note2 = re.sub( r'[^а-яё ]', '', note )	

snote1 = sorted(new_note1)
snote2 = sorted(new_note2)

#create dataframe for future analysis
def createDataFrame(quantity, periodicity):
	squantity = sorted(quantity, key=lambda l: quantity[l], reverse=1 )
	speriod =  sorted(periodicity, key=lambda l: periodicity[l], reverse=1 )
	temp1 = []
	temp2 = []
	for i in range(0,len(squantity)):
    		temp1.append(quantity[squantity[i]])
	for i in range(0,len(speriod)):
    		temp2.append(periodicity[speriod[i]])

	df= pd.DataFrame(index = squantity)
	df['quantity'] = temp1 
	df['periodicity'] = temp2
	name=input('Enter name of excel: ')
	df.to_excel(f'{name}.xlsx')
	print(df.head(10))
	
#periodicity matrix for bigram
def createbgDataFrame(bigram, periodicity, symb):
	#create list of every possible bigrams using alphabet(symbols)
	df = pd.DataFrame(index = symb, columns=symb)
	bg = []
	for i in symb:
   		for j in symb:
        		bg.append(i+j)	
	n = 0
	for i in range(0,len(symb)):
    		df[symb[i]] = bg[n:len(symb)+n]
    		n = len(symb)+n
	df = df.T
	for i in list(periodicity.keys()):
    		x,y = np.where(df == i)
    		df.iloc[x,y] = periodicity[i]
	for i in bg:
		x,y = np.where(df == i)
		df.iloc[x,y] = 0
	name=input('Enter name of excel: ')
	df.to_excel(f'{name}.xlsx')
	print(df)

#Create bigrams(w/o crossing)
def bigramCross(new_note):
	bigram_cross = []
	for i in range(0, len(new_note)-1):
		bigram_cross.append(new_note[i]+new_note[i+1])
	return bigram_cross

def bigram(new_note):
	bigram=[]
	if len(new_note)==2:
		for i in range(0, len(new_note)):
			bigram.append(new_note[i]+new_note[i+1])
	else:
		for i in range(0, len(new_note)-2,2):
			bigram.append(new_note[i]+new_note[i+1])
	return bigram
	
#H_1
def H_1(periodicity):
	h_1 = []
	for p in periodicity.values():
		h_1.append(p*m.log(p,2))
	H_1 = -sum(h_1)
	return H_1

#H_2
def H_2(periodicity):
	h_2 = []
	for p in periodicity.values():
		h_2.append(p*m.log(p,2))
	H_2 = -sum(h_2)/2
	return H_2


#determine quantity and periodicity of letters in our note
quantity1 = dict(collections.Counter(snote1))
quantity2 = dict(collections.Counter(snote2))
period1 = {l: quantity1[l]/len(snote1) for l in quantity1 }
period2 = {l: quantity2[l]/len(snote2) for l in quantity2 }


#bigram without spaces
bigram_cross1 = bigramCross(new_note1)
bigram1 = bigram(new_note1)
bg_cross_q1 = dict(collections.Counter(bigram_cross1))
bg_q1 = dict(collections.Counter(bigram1))
bg_cross_period1 = {l: bg_cross_q1[l] / len(bigram_cross1) for l in bg_cross_q1}
bg_period1 = {l: bg_q1[l] / len(bigram1) for l in bg_q1}

#bigram with spaces
bigram_cross2 = bigramCross(new_note2)
bigram2 = bigram(new_note2)
bg_cross_q2 = dict(collections.Counter(bigram_cross2))
bg_q2 = dict(collections.Counter(bigram2))
bg_cross_period2 = {l: bg_cross_q2[l] / len(bigram_cross2) for l in bg_cross_q2}
bg_period2 = {l: bg_q2[l] / len(bigram2) for l in bg_q2}


def frequency(periodicity):
	speriod =  sorted(periodicity, key=lambda l: periodicity[l], reverse=1 )
	temp2 = []
	for i in range(0,len(speriod)):
    		temp2.append(periodicity[speriod[i]])

	df= pd.DataFrame(index = periodicity)
	df['periodicity'] = temp2
	#name=input('Enter name of excel: ')
	#df.to_excel(f'{name}.xlsx')
	print(df.head(10))



print('////////////////////WITHOUT SPACES///////////////////')
#createDataFrame(quantity1, period1)
print("\nH_1(entropy) without spaces: ",H_1(period1))
print("Excess_1: ",(1-(H_1(period1)/m.log2(len(symbols_2)))))
#createbgDataFrame(bigram_cross1, bg_cross_period1, symbols_2)
#frequency(bg_cross_period1)
print("\nH_2(entropy) cross without spaces: ",H_2(bg_cross_period1))
print("Excess_2: ",(1-(H_2(bg_cross_period1)/m.log2(len(symbols_2)))))
#createbgDataFrame(bigram1, bg_period1, symbols_2)
#frequency(bg_period1)
print("\nH_2(entropy) without spaces: ",H_2(bg_period1))
print("Excess_3: ",(1-(H_2(bg_period1)/m.log2(len(symbols_2)))), '\n')

print('////////////////////WITH SPACES////////////////////')
#createDataFrame(quantity2, period2)	
print("\nH_1(entropy) with spaces: ",H_1(period2))
print("Excess_4: ",(1-(H_1(period2)/m.log2(len(symbols)))))
#createbgDataFrame(bigram_cross2, bg_cross_period2, symbols)
#frequency(bg_cross_period2)
print("\nH_2(entropy) cross with spaces: ",H_2(bg_cross_period2))
print("Excess_5: ",(1-(H_2(bg_cross_period2)/m.log2(len(symbols)))))
#createbgDataFrame(bigram2, bg_period2, symbols)
#frequency(bg_period2)
print("\nH_2(entropy) with spaces: ",H_2(bg_period2))
print("Excess_6: ",(1-(H_2(bg_period2)/m.log2(len(symbols)))))


		








