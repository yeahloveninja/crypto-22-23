from collections import Counter
import re 
import math
import pandas as pd

                                                                    ### SET UP ###
just_text = open("E:\Python_filez\Crypto\some_text3.txt", mode="r", encoding="utf-8").read()
just_text = just_text.lower()
new_just_text = re.sub( r'[^а-яё ]', '',just_text)
new_just_text_wop = re.sub( r'[^а-яё]', '',just_text)
new_just_text = ' '.join(new_just_text.split())
new_just_text_wop = ' '.join(new_just_text_wop.split())

text_with_probels = open("E:\Python_filez\Crypto\my_text_with_probels.txt", mode="w", encoding="utf-8").write(new_just_text)
text_with_probels = new_just_text


text_without_probels = open("E:\Python_filez\Crypto\my_text_without_probels.txt", mode="w", encoding="utf-8").write(new_just_text_wop)
text_without_probels = new_just_text_wop

                                                             ###  FREQUENCY OF LETTERS ###
# wp - with probels !!! #


dovzhyna_wp=len(text_with_probels)
dictionary_wp = dict(Counter(text_with_probels))

list_h1_wp=[]
list_h1_wp_keys=[]
print ('Частота букв з пробілом')
for key in dictionary_wp:
    list_h1_wp_keys.append(key)
    list_h1_wp.append(dictionary_wp[key]/dovzhyna_wp)
    print(key,":",dictionary_wp[key]/dovzhyna_wp)



# wop - without probels !!! #


dovzhyna_wop=len(text_without_probels)
# print(dovzhyna_wop)
dictionary_wop = dict(Counter(text_without_probels))

list_h1_wop=[]
list_h1_wop_keys=[]
print ('Частота букв без пробіла')
for key in dictionary_wop:
    list_h1_wop_keys.append(key)
    list_h1_wop.append(dictionary_wop[key]/dovzhyna_wop)
    #print(key,":",dictionary_wop[key]/dovzhyna_wop)


                                                                     ### BIGRAMS ###
# wp !!! #
first_bigram_wp = []
for x in range(0, len(text_with_probels)-1):
    first_bigram_wp.append(text_with_probels[x]+text_with_probels[x+1])

print('first bigram with spaces')

dictionary_first_bigram = dict(Counter(first_bigram_wp))
dovzhyna_first_bigram= sum(dictionary_first_bigram.values())
list_h2_wp_first=[]
list_h2_wp_first_keys=[]
for key in dictionary_first_bigram:
    # print("'",key,"'"," : ",dictionary_first_bigram[key]/dovzhyna_first_bigram, sep='')
    list_h2_wp_first_keys.append(key)
    list_h2_wp_first.append(dictionary_first_bigram[key]/dovzhyna_first_bigram)


second_bigram_wp = []    
for x in range(0, len(text_with_probels)-2,2):
    second_bigram_wp.append(text_with_probels[x]+text_with_probels[x+1])

print('second bigram with spaces')


dictionary_second_bigram = dict(Counter(second_bigram_wp))
dovzhyna_second_bigram= sum(dictionary_second_bigram.values())
list_h2_wp_second=[]
list_h2_wp_second_keys=[]
for key in dictionary_second_bigram:
    # print("'",key,"'"," : ",dictionary_second_bigram[key]/dovzhyna_second_bigram, sep='')
    list_h2_wp_second_keys.append(key)
    list_h2_wp_second.append(dictionary_second_bigram[key]/dovzhyna_second_bigram)





# wop !!! #
first_bigram_wop = []
for x in range(0, len(text_without_probels)-1):
    first_bigram_wop.append(text_without_probels[x]+text_without_probels[x+1])

print('first bigram without spaces')


dictionary_first_bigram_wop = dict(Counter(first_bigram_wop))
dovzhyna_first_bigram_wop= sum(dictionary_first_bigram_wop.values())
list_h2_wop_first=[]
list_h2_wop_first_keys=[]
for key in dictionary_first_bigram_wop:
    # print("'",key,"'"," : ",dictionary_first_bigram_wop[key]/dovzhyna_first_bigram_wop, sep='')
    list_h2_wop_first_keys.append(key)
    list_h2_wop_first.append(dictionary_first_bigram_wop[key]/dovzhyna_first_bigram_wop)


second_bigram_wop = []    
for x in range(0, len(text_without_probels)-1,2):
    second_bigram_wop.append(text_without_probels[x]+text_without_probels[x+1])

print('second bigram without spaces')


dictionary_second_bigram_wop = dict(Counter(second_bigram_wop))
dovzhyna_second_bigram_wop= sum(dictionary_second_bigram_wop.values())
list_h2_wop_second=[]
list_h2_wop_second_keys=[]
for key in dictionary_second_bigram_wop:
    # print("'",key,"'"," : ",dictionary_second_bigram_wop[key]/dovzhyna_second_bigram_wop, sep='')
    list_h2_wop_second_keys.append(key)
    list_h2_wop_second.append(dictionary_second_bigram_wop[key]/dovzhyna_second_bigram_wop)



                                                                   ### ENTROPIA ###
print("ENTROPIA")

entropia_h1_wp = map(lambda x: -x * math.log2(x), list_h1_wp) 
entropia_h1_wp_final = sum(list(entropia_h1_wp))
nadlyshkovist_h1_wp = 1 - (entropia_h1_wp_final/math.log2(34))
print("Ентропія h1 з пробілами:",entropia_h1_wp_final,'  Надлишковість:',nadlyshkovist_h1_wp)

entropia_h1_wop = map(lambda x: -x * math.log2(x), list_h1_wop) 
entropia_h1_wop_final = sum(list(entropia_h1_wop))
nadlyshkovist_h1_wop = 1 - (entropia_h1_wop_final/math.log2(33))
print("Ентропія h1 без пробів:",entropia_h1_wop_final,'  Надлишковість:',nadlyshkovist_h1_wop)


entropia_h2_wp_first = map(lambda y: -y * math.log2(y), list_h2_wp_first) 
entropia_h2_wp_first_final = sum(list(entropia_h2_wp_first))/2
nadlyshkovist_h2_wp_first = 1 - (entropia_h2_wp_first_final/math.log2(34))
print("Ентропія h2 з пробілами для першого випадку:",entropia_h2_wp_first_final,'  Надлишковість:',nadlyshkovist_h2_wp_first)


entropia_h2_wp_second = map(lambda y: -y * math.log2(y), list_h2_wp_second) 
entropia_h2_wp_second_final = sum(list(entropia_h2_wp_second))/2
nadlyshkovist_h2_wp_second = 1 - (entropia_h2_wp_second_final/math.log2(34))
print("Ентропія h2 з пробілами для другого випадку:",entropia_h2_wp_second_final,'  Надлишковість:',nadlyshkovist_h2_wp_second)

entropia_h2_wop_first = map(lambda x: -x * math.log2(x), list_h2_wop_first) 
entropia_h2_wop_first_final = sum(list(entropia_h2_wop_first))/2
nadlyshkovist_h2_wop_first = 1 - (entropia_h2_wop_first_final/math.log2(33))
print("Ентропія h2 без пробілів для першого випадку:",entropia_h2_wop_first_final,'  Надлишковість:',nadlyshkovist_h2_wop_first)

entropia_h2_wop_second = map(lambda x: -x * math.log2(x), list_h2_wop_second) 
entropia_h2_wop_second_final = sum(list(entropia_h2_wop_second))/2
nadlyshkovist_h2_wop_second = 1 - (entropia_h2_wop_second_final/math.log2(33))
print("Ентропія h2 без пробілів для другого випадку:",entropia_h2_wop_second_final,'  Надлишковість:',nadlyshkovist_h2_wop_second)


# топ 10 букв і біграм #
print('Top 10 list')

dictionary_wp_h1_top10 = sorted(dictionary_wp.items(), key=lambda item: item[1], reverse=True)
s=dictionary_wp_h1_top10[:10]
print("Топ 10 h1_wp:",s)
w = dict(s)
df = pd.DataFrame.from_dict(w,orient='index')
df.to_excel('E:\Python_filez\Crypto\list_top10.xlsx')

dictionary_wop_h1_top10 = sorted(dictionary_wop.items(), key=lambda item: item[1], reverse=True)
s=dictionary_wop_h1_top10[:10]
print("Топ 10 h1_wop:",s)

dictionary_wp_h2_first_top10 = sorted(dictionary_first_bigram.items(), key=lambda item: item[1], reverse=True)
s=dictionary_wp_h2_first_top10[:10]
print("Топ 10 h2_wp_first:",s)

dictionary_wp_h2_second_top10 = sorted(dictionary_second_bigram.items(), key=lambda item: item[1], reverse=True)
s=dictionary_wp_h2_second_top10[:10]
print("Топ 10 h2_wp_second:",s)

dictionary_wop_h2_first_top10 = sorted(dictionary_first_bigram_wop.items(), key=lambda item: item[1], reverse=True)
s=dictionary_wop_h2_first_top10[:10]
print("Топ 10 h2_wop_first:",s)

dictionary_wop_h2_second_top10 = sorted(dictionary_second_bigram_wop.items(), key=lambda item: item[1], reverse=True)
s=dictionary_wop_h2_second_top10[:10]
print("Топ 10 h2_wop_second:",s)



# Таблиця частот букв, яка відсортована за спаданням частот і занесена в ексель #
#h1_wp excel#

fresh_dict = {}
for key in list_h1_wp_keys:
    for value in list_h1_wp:
        fresh_dict[key] = value
        list_h1_wp.remove(value)
        break 
# print(res)
fresh_dict=sorted(fresh_dict.items(), key=lambda item: item[1], reverse=True)
fresh_dict=dict(fresh_dict)
df = pd.DataFrame.from_dict(fresh_dict,orient='index')
df.to_excel('E:\Python_filez\Crypto\h1_wp.xlsx')


#h1_wop excel#

fresh_dict2 = {}
for key in list_h1_wop_keys:
    for value in list_h1_wop:
        fresh_dict2[key] = value
        list_h1_wop.remove(value)
        break 
# print(res)
fresh_dict2=sorted(fresh_dict2.items(), key=lambda item: item[1], reverse=True)
fresh_dict2=dict(fresh_dict2)
df = pd.DataFrame.from_dict(fresh_dict2,orient='index')
df.to_excel('E:\Python_filez\Crypto\h1_wop.xlsx')



