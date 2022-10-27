import collections
import re


with open("/home/kali/cr2/lab2.txt", 'r', encoding='utf-8') as ofile:
	note = ofile.read()
	note = note.replace("\n","")
	note = note.lower()
	note = note.replace(" ","").replace("  "," ")		
	note= re.sub( r'[^а-яё]', '', note )
	note = note.replace("ё", "е")

with open("/home/kali/cr2/var4.txt", 'r', encoding='utf-8') as opfile:
	note2 = opfile.read()
	note2 = note2.replace('\n',"")
	

#print(note)

bukvy = ['а', 'б', 'в', 'г', 'д', 'е', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']
    
def IndexVidp(text): #індекс відповідності 
    x = dict(collections.Counter(text))
    i = []
    for key in list(x.keys()):
        i.append(x[key]*(x[key]-1))
    I = 1/(sum(x.values())*(sum(x.values())-1))*sum(i)
    return(I)
   

def DecodeText(shyfrtxt, kluch): #розшифрування ШТ
    g=0
    text = ''
    for i in shyfrtxt:
        text += bukvy[(bukvy.index(i) + 32 - bukvy.index(kluch[g]))%32]
        g+=1
        if (g >= len(kluch)):
            g = 0
    return(text)  
    
    
def EncodeText(text, kluch): #зашифрування відкритого тексту
    shyfrtxt = ''
    g=0
    for i in text:
        shyfrtxt += bukvy[(bukvy.index(i) + bukvy.index(kluch[g]))%32]
        g+=1
        if (g >= len(kluch)):
            g = 0
    return(shyfrtxt)   


def Block(text, r): #розбиваємо текст на блоки
	bl=list()
	for i in range(r):
		bl.append('')
		j=i
		while(j<len(text)):
			bl[i] = bl[i]+text[j]
			j+=r
	return bl

  
def IndVidpEachBl(text, r): #індекс відповідності для кожного блоку
    blocks = Block(text, r) 
    ind = 0
    for i in range(len(blocks)):
        ind = ind + IndexVidp(blocks[i])
    ind = ind/len(blocks)
    return ind     

def FindKluch(text, r, bukva): #визначаємо ключ
    blocks = Block(text, r)
    litera = ''
    for b in blocks:
        tmp = collections.Counter(b).most_common(1)[0]
        litera += bukvy[(bukvy.index(tmp[0]) - bukvy.index(bukva))%32]
    print(litera)

def FirstTask(text): 
    kluchi = ['ок','дух','змея','почка','лапшерезка','явлабиринте','хомяквклетке','высокоедерево','онвлесопосадке','ялегкомысленный','ялюблюфантастику','литературоведение','сменачасовыхпоясов','психопатологический','многообещающаялирика']
    print('---------------Task1---------------')
    print("Iндекс відповідності для відкритого тексту:",IndexVidp(text), "\n")
    for i in kluchi:
    	print("Довжина ключа",len(i),":",IndexVidp(EncodeText(text, i)))


def SecondTask(text):
	print('---------------Task2---------------') 
	for i in range(2, len(bukvy)):   
		print("Довжина ключа", i,':', IndVidpEachBl(text, i))
	print('-----------------------------------')
	for letter in 'оеа':
    		FindKluch(note2, 13, letter)  # так як ключ має довжину 13 або 26'''
	print("-----------------------------------")
	print(DecodeText(text, 'громыковедьма'))
	
FirstTask(note)
#print('-----------------------------------')
#print(EncodeText(note, 'лапшерезка'))
SecondTask(note2)	




