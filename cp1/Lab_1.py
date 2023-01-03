import pandas, numpy, re, math
from pandas import ExcelWriter

print ('Криптографія')
print ("Комп'ютерний практикум №1")
print ('Експериментальна оцінка ентропії на символ джерела відкритого тексту')
print ('Виконали: Лугінін Богдан та Хаустович Артем')
print ('Перевірила: Байденко П. В.')
print ('Waiting...')
print ('Start')

def inputtext(): #Функція читання та форматування тексту
    f = open("orwell.txt", "r", encoding='latin-1')
    text = f.read()
    text = text.replace("\n", "")
    text = text.lower()
    f.close()
    return text

def H(n): #Ентропія ансамблю
    H = 0
    for x in n:
        H = H + n[x]*math.log(n[x], 2)
    return -H

def count(x, dict):
    if x in dict:
        dict[x] += 1
    else:
        dict[x] = 1
    return dict

def freq(dict):
    freq1 = sum(dict.values())
    for x in dict:
        dict[x] = float(dict[x] / freq1)
    return dict

def P(n): #Надлишковість
    P = 1 - n/math.log(33, 2)
    return P

def result(text):
    char_ = char_freq(text)
    bgram1_ = bgram1(text)
    bgram2_ = bgram2(text)
    return char_,bgram1_,bgram2_

def format_df(df, arr, dict):
    for i in list(dict):
        a, b = numpy.where(df == i)
        df.iloc[a, b] = dict[i]
    for i in arr:
        a, b  = numpy.where(df == i)
        df.iloc[a, b] = 0
    return df

def char_freq(str):
    dict = {}
    for x in str:
        dict = count(x,dict)
    return freq(dict)

def bgram2(str): #Пошук біграм із кроком 2
    dict = {}
    cnt = 0
    bgram = ""
    for i in range(len(str)):
        if cnt != 2:
            bgram += str[i]
            cnt += 1
            i += 1
            if i == len(str):
                dict = count(bgram,dict)
        elif cnt == 2:
            cnt = 0
            if bgram != '':
                dict = count(bgram,dict)
            bgram = ""
    return freq(dict)

def bgram1(str): #Пошук біграм із кроком 1
    dict = {}
    cnt = 0
    bgram = ''
    for i in range(len(str)):
        if cnt != 2:
            bgram += str[i]
            i += 1
            cnt += 1
        elif cnt == 2:
            cnt = 0
            i -= 1
            if bgram != '':
                dict = count(bgram,dict)
            bgram = ''
    return freq(dict)


def sort_xlsx(text, file):
    writein = ExcelWriter(file, engine='xlsxwriter')
    df = pandas.DataFrame.from_dict(text, orient='index', columns=['amount']).sort_values(by='amount', ascending=0)
    df.to_excel(writein, "Sort")
    writein.save()

def bgram_xlsx(dict, alphabet, file):
    arr = []
    f = 0
    df = pandas.DataFrame(index=alphabet, columns=alphabet)
    for i in alphabet:
        for j in alphabet:
            arr.append(i + j)
    for i in range(0, len(alphabet)):
        df[alphabet[i]] = arr[f:len(alphabet) + f]
        f = len(alphabet) + f
    df = df.T
    df = format_df(df,arr,dict)
    df.to_excel(file)

def output(text):
    char_spaced, bgram1_spaced, bgram2_spaced = result(text)
    text = text.replace(" ", "")
    char_nospaced, bgram1_nospaced, bgram2_nospaced = result(text)
    while True:
        try:
            ans = int(input('1 - Вивести ентропію і надлишковості(H і R)\n2 - Вивести дані до таблиці\n3 - Підрахувати надлишковості\n4 - Вихід\nВведіть вибір: '))
            if ans == 1:
                print("Із пробілами\nЕнтропія монограми:",H(char_spaced),"Надлишковість:", P(H(char_spaced)))
                print("Ентропія біграми(із кроком 2)",H(bgram2_spaced)*0.5,"Надлишковість:", P(H(bgram2_spaced)*0.5))
                print("Ентропія биграмм(із кроком 1)",H(bgram1_spaced)*0.5,"Надлишковість:", P(H(bgram1_spaced)*0.5))
                print("Без пробілів\nЕнтропія монограми:",H(char_nospaced),"Надлишковість:", P(H(char_nospaced)))
                print("Ентропія біграми(із кроком 2)",H(bgram2_nospaced)*0.5,"Надлишковість:", P(H(bgram2_nospaced)*0.5))
                print("Ентропія біграми(із кроком 1)",H(bgram1_nospaced)*0.5,"Надлишковість:", P(H(bgram1_nospaced)*0.5),'\n')
            elif ans == 2:
                global a,a_space
                sort_xlsx(char_spaced, 'char_spaced.xlsx')
                sort_xlsx(char_nospaced, 'char_nospaced.xlsx')
                bgram_xlsx(bgram1_nospaced, a, 'bigram1_nospaced.xlsx')
                bgram_xlsx(bgram1_spaced, a_space, 'bigram1_spaced.xlsx')
                bgram_xlsx(bgram2_nospaced, a, 'bigram2_nospaced.xlsx')
                bgram_xlsx(bgram2_spaced, a_space, 'bigram2_spaced.xlsx')
            elif ans == 3:
                a = float(input("Введіть число з \"плавучою точкою\": "))
                print('R(a): ', P(a))
            elif ans == 4:
                break
        except:
            pass

a_space = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т','у','ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', ' ']
a = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т','у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

text = re.sub(r'[^\w\s]+|[\d]+', '', inputtext())
output(text)
