import math
from collections import Counter
alphbet = ["а","б","в","г","д","е","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ", "ы",
        "ь","э","ю","я", " "] 
# entering our alphabet
probels = []
say_no_to_probels = []
with open('text_example.txt', 'r', encoding = 'UTF-8') as f:
    file = f.read()
    file = file.lower()
    distance = len(file)
    file.replace("ё", "е")
    file.replace("ъ", "ь")
    prbl = False
# меняем буквы в файле, убираем пробелы, считаем длинну и убираем заглавные буквы
# analyzing our text file
    for i in range(distance):
        if file[i] in alphbet:
            if file[i] == " ":
                if prbl == True:
                    continue
                else:
                    probels.append(" ")
                    prbl = True
                    #список с пробелами
            else:
                probels.append(file[i])
                say_no_to_probels.append(file[i])
                prbl = False
                #список без пробелов
        else:
            if prbl == False:
                probels.append(" ")
                prbl = True
                #если нет нужного символа, меняем его на пробел
#считываем текст на пробелы
# here text editing ends


def redundancy_checkon(n, m):
    return 1 - (n / math.log(m, 2))
# calculating redundancy stats


def entropy_bigr(txt, touch_point):
    distance = len(txt)
    if distance % 2 == 1 and touch_point == 0:
        distance -= 1
        #если иду с шагом два, отнимается 1
    bigr = []
    for i in range(0, distance-1, 2-touch_point): #проходимся с определенным шагом
        bigr.append(txt[i]+txt[i+1]) #склейка букв и добавляется в биграмму
    count = len(bigr)
    frequency = Counter(bigr) #количество повторений элементов
    # print(frequency)
    for i in frequency:
        frequency[i] /= count
    result = sum(frequency [k] * math.log(frequency [k], 2) for k in frequency ) / (-2) #энтропия, на -2 бо минус перед ответом
    frequency = sorted(frequency .items(), key=lambda item: item[1], reverse=True) #сортируем и разворачиваем очередь
    for key, value in frequency :
        print(key, ':', value)
    print("Redundancy", redundancy_checkon(result, len(''.join(set(txt)))))
    return result

#привет
#короп

def entropy_lett(txt):
    distance = len(txt)
    frequency = Counter(txt)
    # print(frequency)
    for i in frequency:
        frequency [i] /= distance
    result = -1 * sum(frequency[k] * math.log(frequency [k], 2) for k in frequency ) #энтропия
    frequency  = sorted(frequency .items(), key=lambda item: item[1], reverse=True) #сортируем и разворачиваем очередь
    for key, value in frequency:
        print(key, ':', value)
    print("Redundancy", redundancy_checkon(result, len(frequency)))
    return result


print("H2 txt with probels without touch_points", entropy_bigr(probels, 0)) #задаем шаг и выводим
print("H1 txt with probels with touch_points", entropy_bigr(probels, 1))
print("H2 txt without probels without touch_points", entropy_bigr(say_no_to_probels, 0))
print("H1 txt without probels with touch_points", entropy_bigr(say_no_to_probels, 1))
print("letters with probels", entropy_lett(probels))
print("letters without probels", entropy_lett(say_no_to_probels))
