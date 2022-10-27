# -*- coding: cp1251 -*-
import re
#sort function from lab1
def txteditor(file_name):
    with open(file_name, 'r', encoding='utf-8') as file: #open your file -> read text -> close
        txt = file.read().lower()
        file.close()
    txt2 = " ".join(txt.split())
    edited_text = re.sub( r'[^а-яё]', '', txt2) 
    edited_text = edited_text.replace("ё","е")
    with open('goodtext.txt', 'w', encoding='utf-8') as file:
        file.write(edited_text)
        file.close()

#ru alphabet
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
#randomly generetaed keys with length from 2-20 
keys = ['жг','ишб', 'зпеф', 'юмыех', 'пжмзяг', 'йогучмф', 'сгряуцвш', 'ахпатлдгп', 'жячкьевщпю', 'этбсснддчмй', 'рщалцйзьпохц', 'ноинрсшдайупв',  'ххдсынвдовзэгх', 'йчшхвклябютмюйы', 'чйцжоъоэнавгжвюб', 'вевуюргначитвшдьж', 'жзфкостеьлщйцэтсна', 'рмыньквзжпюэчаднудс', 'эбокрэижтжъебътчодиг']

#some helpful functions to decrypt/encrypt
def encrypt(key, text):
    return VigenereCipher(key, text, 'encrypt')

def decrypt(key, text):
    return VigenereCipher(key, text, 'decrypt')

#simple implementation of Vigenere cipher, it is familiar to Caesar cipher 
def VigenereCipher(key, text, mode):
    tmp = [] # for saving output text
    kindex = 0
    for t in text: # each letter in text 
        num = alphabet.find(t)
        if num != -1: #-1 is what .find() returns when the letter wasn't found 
            if mode == 'encrypt':
                num += alphabet.find(key[kindex])
                num %= len(alphabet)
                tmp.append(alphabet[num])
                kindex += 1 
                if kindex == len(key): #repeat key
                    kindex = 0
            elif mode == 'decrypt':
                num -= alphabet.find(key[kindex]) 
                num %= len(alphabet)
                tmp.append(alphabet[num])
                kindex += 1 
                if kindex == len(key):
                    kindex = 0
        else:
            tmp.append(t)
    return ''.join(tmp)

#from lab1; using it for index of coincidence 
def frequency(text):
    freq = {}; 
    for i in text: 
        if i not in freq:
            freq[i] = 1
        else:
            freq[i] +=1
    freq = dict(sorted(freq.items()))
    return freq

# find index of coincidence, formula was given 
def CoinIndex(text):
    res = 0
    n = len(text)
    for f in frequency(text).values():
        res = res +  f * (f- 1)
    res = res * 1/(n * (n - 1))
    return res


# text, size=2
#'я к вам пишу чего же боле' = 'я' -> block1 'к' -> block2 'в' -> block1 'a' -> block2 ... 
#function didvides text into blocks
def get_blocks(text, size):
    blocks = []
    for i in range(0, size):
        blocks.append(text[i::size])
    return blocks

# get the index of each block, but actually we need max value from it to get key length 
def BlockCoinIndex(text):
    res = {}
    for i in range(1,len(alphabet)):
        idx = 0
        total = get_blocks(text, i)
        for j in total:
            idx = idx + CoinIndex(j)
        idx /= i
        res[i] = idx
    return res

#using it just to help to find that max value from prev func
def keysize():
        size = max(BlockCoinIndex(enctxt).values())
        data = BlockCoinIndex(enctxt)
        for i in data.keys():
            if data[i] == max(data.values()):
                klen = i
        return klen

# this function will build key 
def GetTrueKey(text, keylen):
    possible_keys = {} #here we gather possible keys
    blocks = get_blocks(text, keylen) #divide your text
    top = "оаенитсл" # top ru letters we took from lab1
    for l in top: # start of calculation
        cipherkey = "" #key we will output
        for block in blocks:  #for each block           
            letter_freq = frequency(block) # get the freq of letters
            top_freq = max(letter_freq.values()) #get the most frequent letter 
            for k, val in letter_freq.items(): # get from dict which letter is this
                if val == top_freq:
                    ktop=k 
            #letter_freq.pop(ktop)
            cipherkey += alphabet[(alphabet.index(ktop) - alphabet.index(l)) % len(alphabet)] # formula for decrypting 
        possible_keys[l] = cipherkey 
        print(possible_keys[l]) # print it
        print("One of possible keys was found, do you want to continue searching?") #if key is okay stop searching, else continue
        ans = input('>>')
        if ans == 'yes':
            continue
        elif ans == 'no':
            return possible_keys[l]

#start task1+task2
txteditor('badtext.txt')
file = open('goodtext.txt', encoding = 'utf-8')
somedata = file.read()
file.close()

print('Coincidence index of all text:', CoinIndex(somedata))

for k in keys:
    x1 = encrypt(k, somedata)
    print('-----Data was encrypted with key:',k)
    print('-----Output:')
    print(x1)
    print('-----Coincidence index of encrypted text:', CoinIndex(x1), '\n')
    #print('-----Decrypt:')
    #print(decrypt(k, x1),'\n')


#task3
print("-----------------------------")
file2 = open('task3.txt', encoding = 'utf-8')
enctxt = file2.read()
file2.close()
#print(BlockCoinIndex(enctxt))
print(CoinIndex(enctxt))
print("Finding the length of key ...")
keylen = keysize()
print(keylen)
print(GetTrueKey(enctxt,keylen))

truekey = 'венецианскийкупец'
final_answer = decrypt(truekey, enctxt)
print("The end:)\n", final_answer)

