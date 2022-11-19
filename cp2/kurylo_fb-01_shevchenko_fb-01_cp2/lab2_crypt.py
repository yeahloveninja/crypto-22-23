with open('source.txt', mode = 'r', encoding="utf8") as source:
    source = source.read()
with open('var_8.txt', mode = 'r', encoding="utf8") as var_8:
    var_8 = var_8.read()


alfavit = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'                         #російський(крінж) алфавіт
dovzhyna_alf = len(alfavit)

our_keys = ['ке', 'длу', 'язхв', 'фухжс', 'ътуйжгщоас', 'оучхжпоугцч', 'дгктсячцщпфэ', 'аьбкущяфауеой', 'гкольфвапкушщд', 'золмиейжбчугвтш', 'хъяеьщувонтчзетм', 'аотугшахйъвапнгтщ', 'кюсвщгпрйкувздшлтю', 'уъафгмивщлшдцчаьенв', 'епвдштмрвнуцрхцсмнга']
# for x in our_keys:
#     print(x)

def encryption(key, data):                                           #функція шифрування
    count=0
    final_result = ''
    for value in data:

        key_index = count % len(key)
        final_result  = final_result + alfavit[(alfavit.index(value) + alfavit.index(key[key_index])) % dovzhyna_alf]
        count = count + 1

    return final_result


def decryption(key, data):                                             #функція розшифровування
    count=0
    final_result = ''
    for value in data:
        key_index = count % len(key)
        final_result = final_result + alfavit[(alfavit.index(value) - alfavit.index(key[key_index])) % dovzhyna_alf]
        count = count + 1

    return final_result 


def get_index(data):                                                  #функція знаходження індексу відповідності

    index = 0
    for x in range(dovzhyna_alf):
        iter = data.count(alfavit[x])
        index = index + iter * (iter - 1)
    index = index * 1/(len(data)*(len(data)-1))

    return index


plaintext=get_index(source)                                          #індекс відповідності для відкритого тексту
print("Індекс відповідності для Відкритого тексту : ",plaintext)

our_indexes = []                                                     #індекси відповідності для зашифрованих текстів 
for x in our_keys:
    text_encrypted = encryption(x,source)     
    my_index=get_index(text_encrypted)  
    our_indexes.append(my_index)
# for x in our_indexes:
#     print(x)   

print("Реалізація першого алгоритму для знаходження довжини ключа за допомогою індекса відповідності")

def blocks_indexes(length,data):         
    segments = []

    for x in range(length):                    #розбиття ШТ на блоки
        segments.append(data[x::length])    
    index = 0
    for x in range(len(segments)):             #обчислення ІВ для кожного блоку
        index=index+get_index(segments[x])
    index=index/len(segments)
    return index

equally_likely_alf = 1/dovzhyna_alf            #значення мови з рівноімовірним алфавітом
for x in range (1,dovzhyna_alf):   
    print(equally_likely_alf, " | ", blocks_indexes(x,var_8),"----- key length:",x)     #вивід значень для порівняння
for x in range (1,dovzhyna_alf): 
    print(blocks_indexes(x,var_8))

print(" ")
found_key_length = 20       #значення довжини ключа, що схиляється до теоретичного значення I для даної мови
    
freq_letters = ['о','е','а','и','н']   #найчастіші букви в рос.алфавіті

def get_key(data, letters, length):    #функція пошуку ключа
    for letter in letters:   
        segments = []
        for x in range(length):
            segments.append(data[x::length])        
        possible_key = ""                            
        for x in range(len(segments)):
            freq_ones = max(segments[x], key=lambda c: segments[x].count(c))
            possible_key = possible_key + alfavit[(alfavit.index(freq_ones)-alfavit.index(letter))%dovzhyna_alf]
        print("For letter",letter,'we have key:', possible_key)


our_key = get_key(var_8, freq_letters, found_key_length) #отриманий ключ

right_key='улановсеребряныепули' #змістовний ключ

revealed_text = (decryption(right_key, var_8)) #розкодований текст
print("\nРозшифрований текст:")
print(revealed_text)










