from itertools import *
from collections import Counter
with open('var_8.txt', mode = 'r', encoding="utf8") as var_8:
    var_8 = var_8.read()
data_length = len(var_8)

                                     #  Реалізовуємо підпрограми  #

def upgraded_euclidean(a,b):
    #check
    if a==0 :
        return b,0,1
             
    gcd,x1,y1 = upgraded_euclidean(b % a,a)
    x=y1 - (b//a) * x1
    y=x1
    return gcd,x,y


def inverse(a, m):
    i = [0,1]
    
    while m != 0 and a != 0:
        if a > m: 
            i.append(a // m); a = a % m
        else: i.append(m // a); m = m % a

    for n in range(2,len(i)): 
        i[n] = i[n-2] - i[n] * i[n-1]
    return i[-2]


def lin_compar(m, a, b):
  gcd, a0, y = upgraded_euclidean(a,m)
  sol = []

  if gcd != 1 :
    if b% gcd != 0:
      return None
    else:
      gcd, k, a0 = upgraded_euclidean(a,m)
      for n in range (gcd - 1):
        x = (a0 * b) % m + n*m
        sol.append(x)

      return sol
  else:
    if ((a * a0) % m) == 1:
      sol.append((a0 * b) % m)

      return sol


                                       # 5 найчастіших біграм для тексту 8 варіанта #
def top_bigrams(text_to_read):
    number_of_bigrams=5
    second_bigram_wop = []    
    for x in range(0, len(text_to_read)-1,2):
        second_bigram_wop.append(text_to_read[x]+text_to_read[x+1])

    dictionary_second_bigram_wop = dict(Counter(second_bigram_wop))
    dovzhyna_second_bigram_wop= sum(dictionary_second_bigram_wop.values())
    list_h2_wop_second=[]
    list_h2_wop_second_keys=[]
    for key in dictionary_second_bigram_wop:
        # print("'",key,"'"," : ",dictionary_second_bigram_wop[key]/dovzhyna_second_bigram_wop, sep='')
        list_h2_wop_second_keys.append(key)
        list_h2_wop_second.append(dictionary_second_bigram_wop[key]/dovzhyna_second_bigram_wop)

    lll = dict(islice(sorted(dictionary_second_bigram_wop.items(), key=lambda i: i[1], reverse=True),number_of_bigrams))  
    # print(lll)
    return lll     
    

alf=['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
alf_length = len(alf)


lang_tops = ['ст', 'но', 'то', 'на', 'ен']
unused_bigrams = ['аь','ьь','фщ','юы','еь','уь','яы','чф','жы','щы','юь','ыь','шы','ьы','эы','щъ','эь','чц','яь','цщ']

bigrams_tops = top_bigrams(var_8)
stor = list(product(lang_tops, bigrams_tops.keys()))                       
stor = list(product(stor, stor))

matching = filter(lambda matches: matches[0][0] != matches[1][0] and matches[0][0] != matches[1][1] and matches[0][1] != matches[1][0] and matches[0][1] != matches[1][1], stor)
matches = list(matching)
# print(matches)

def get_data(data_source, a, b):
  gcd, x, y = upgraded_euclidean(a, alf_length*alf_length)

  decrypted = ''
  for n in [data_source[cnt: cnt + 2] 
    for cnt in range(0, data_length, 2)]:
    cnt_b = alf.index(n[0]) * alf_length + alf.index(n[1])       
    cnt_dec = ((cnt_b - b) * x) % (alf_length**2)

    sec_x = cnt_dec % alf_length
    fir_x = (cnt_dec - sec_x) / alf_length
    big_x1 = alf[int(fir_x)]
    big_x2 = alf[int(sec_x)]

    if big_x1+big_x2 not in unused_bigrams: 
      decrypted += big_x1 + big_x2
    else:
      return False
  return decrypted

for (f_dbl, s_dbl) in matches:
    as_y = alf.index(f_dbl[0][0]) * alf_length + alf.index(f_dbl[0][1])
    as_x = alf.index(f_dbl[1][0]) * alf_length + alf.index(f_dbl[1][1])

    as_y2 = alf.index(s_dbl[0][0]) * alf_length + alf.index(s_dbl[0][1])
    as_x2 = alf.index(s_dbl[1][0]) * alf_length + alf.index(s_dbl[1][1])
    
    #get a, b
    key_a_val = as_y - as_y2
    key_b_val = as_x - as_x2

    kf_a = lin_compar(alf_length**2, key_a_val, key_b_val)
    for key_a in kf_a:
        estim_b = (as_x - as_y * key_a) % alf_length**2
        decrypted_data = get_data(var_8, key_a, estim_b)

        if decrypted_data == False:
            continue
        else:
            #get right_result
            result = decrypted_data
            print("")
            print(" [ Результати роботи ] ""\n" )
            print(" -Текст для варіанту 8 має такі 5 найчастіших біграм: ",bigrams_tops,"\n" )
            print(" -Використавши Критерій заборонених l-грам, отримали такі значення: a =",key_a, " i ", "b =",estim_b, "\n" )
            print(" -Отже шуканий ключ, при якому розшифрований текст є змістовним : ( a , b ) = (",key_a,",",estim_b,")" "\n" )
            print(" -Розшифрований текст має такий вигляд: ",result)
            exit()

       
