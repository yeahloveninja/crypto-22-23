import collections
import re

#під'єднаємо наші файлики до програмки

with open("1task.txt", 'r', encoding='utf-8') as ofile:
	note = ofile.read()
	note = note.replace("\n","")
	note = note.lower()
	note = note.replace(" ","").replace("  "," ")		
	note= re.sub( r'[^а-яё]', '', note )
	note = note.replace("ё", "е")

with open("3task.txt", 'r', encoding='utf-8') as opfile:
	note2 = opfile.read()
	note2 = note2.replace('\n',"")
	
#виведемо обраний нами фрагмент тексту (все ще Орвелл "Скотоферма")
print(note)

abetka = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    
def IndexVidp(text): #обчислюємо потрібний нам індекс відповідності 
    x = dict(collections.Counter(text))
    i = []
    for key in list(x.keys()):
        i.append(x[key]*(x[key]-1))
    I = 1/(len(text)*(len(text)-1))*sum(i)
    return(I)
   

def DecodeText(chipertxt, kluch): #здійснюємо розшифрування шифротексту
    g=0
    text = ''
    for i in chipertxt:
        text += abetka[(abetka.index(i) - abetka.index(kluch[g]))%32]
        g+=1
        if (g >= len(kluch)):
            g = 0
    return(text)  
    
    
def EncodeText(text, kluch): #здійснюємо зашифрування відкритого тексту
    chipertxt = ''
    g=0
    for i in text:
        chipertxt += abetka[(abetka.index(i) + abetka.index(kluch[g]))%32]
        g+=1
        if (g >= len(kluch)):
            g = 0
    return(chipertxt)   


def Block(text, r): #виконуємо розбиття тексту на блоки
	bl=list()
	for i in range(r):
		bl.append('')
		j=i
		while(j<len(text)):
			bl[i] = bl[i]+text[j]
			j+=r
	return bl

  
def IndVidpEachBl(text, r): #шукаємо індекс відповідності для кожного блоку
    blocks = Block(text, r) 
    ind = 0
    for i in range(len(blocks)):
        ind = ind + IndexVidp(blocks[i])
    ind = ind/r
    return ind     

def FindKluch(text, r, bukva): #визначаємо ключ для дешифрування шифротексту
    blocks = Block(text, r)
    litera = ''
    for b in blocks:
        tmp = collections.Counter(b).most_common(1)[0]
        litera += abetka[(abetka.index(tmp[0]) - abetka.index(bukva))%32]
    print(litera)

def FirstTask(text): 
    kluchi = ['да','жук','муха','пчела','луггихауст','еммороженко','здесьстобукв','ведьмынегорят','параллелограмм','всегдаделаюлабы','петухидеткиндюку','напитокмаргаритта','хочускушатьконфету','дайтежратьпокаживой','спасибонадопкунехочу']
    print('---------------Задачка #1---------------')
    print("Iндекс відповідності для відкритого тексту:",IndexVidp(text), "\n")
    for i in kluchi:
    	print("Довжина ключа ",len(i),":",IndexVidp(EncodeText(text, i)))


def SecondTask(text):
	print('---------------Задачка #2---------------') 
	for i in range(2, len(abetka)):   
		print("Довжина ключа ", i,':', IndVidpEachBl(text, i))
	print('-----------------------------------')
	for letter in 'оеа':
    		FindKluch(note2, 13, letter)  # так як ключ має довжину 13 або 26
	print("-----------------------------------")
	print('---------------Задачка #3---------------')
	print(DecodeText(text, 'громыковедьма'))
	
FirstTask(note)
print('-----------------------------------')
print(EncodeText(note, 'луггихауст'))
SecondTask(note2)	



