import collections
import unicodedata
import pandas as pd
note = open("/home/kali/lab1.txt").read()
note = note.replace("\n"," ")
note = note.lower()
note = ' '.join(note.split())
text = ''.join(s for s in note if unicodedata.category(s).startswith('L'))
#print(text)
stext = sorted(text)
#print(stext)

quantity = dict(collections.Counter(stext))
#print(quantity) 
squantity = sorted(quantity, key=lambda l: quantity[l], reverse=1 )
#print(squantity)
period = {l: quantity[l]/len(stext) for l in quantity }
#print(period)
speriod =  sorted(period, key=lambda l: period[l], reverse=1 )
#print(speriod)

temp1 = []
temp2 = []
for i in range(0,len(squantity)):
    temp1.append(quantity[squantity[i]])
 
for i in range(0,len(speriod)):
    temp2.append(period[speriod[i]])

df= pd.DataFrame(index = squantity)
df['quantity'] = temp1 
df['periodicity'] = temp2
#df.to_excel("letters.xlsx")
print(df.head(10))






