import collections
import re 
import numpy as np

   
alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']

def index_coincidence(text):
    letters = sorted(text)
    #alphabetDict = dict(collections.Counter(letters))
    sum = 0
    
    alphabetDict = alphabet
    alphabetDict = dict((k,0) for k in alphabetDict)
    temp = dict(collections.Counter(letters))
    
    for i in temp:
        alphabetDict[i] = temp[i]
    
    for char in alphabet:
        sum += alphabetDict[char]*(alphabetDict[char]-1)
    
    IC = (sum/(len(text)*(len(text)-1)))
    return(IC)


def encode(plaintext, key):
    keyLetterIndex=0
    ciphertext = ''
    
    for char in plaintext:
        ciphertext += alphabet[(alphabet.index(char) + alphabet.index(key[keyLetterIndex%len(key)]))%32]
        keyLetterIndex+=1
        
    return(ciphertext)


def decode(ciphertext, key):
    keyLetterIndex=0
    plaintext = ''
    
    for char in ciphertext:
        plaintext += alphabet[(alphabet.index(char) - alphabet.index(key[keyLetterIndex%len(key)]))%32]
        keyLetterIndex+=1
        
    return(plaintext)  


def separate_into_blocks(ciphertext, keyLength):
    blocks = []
    i = 0
    
    #Розбиваємо шифртекст на блоки Y0, Y1, ..., Y(r-1)
    while i < keyLength:
        block = ''
        j = 0
        
        #Записуємо в блоки значення (y0, ..., y(nr + 0)), (y1, ..., y(nr + 1)), ..., (y(r-1), ..., y(nr + r)) 
        while i + j*keyLength < len(ciphertext):
            block += ciphertext[i + j*keyLength]
            j += 1
        blocks.append(block)
        i += 1
        
    return(blocks)



def find_block_IC(ciphertext):
    #Перебір всіх можливих ключів довжиною від 2 до 32(довжина алфавіта)
    maxKeyLength = 32
    currentKeyLength = 2
    
    while currentKeyLength < maxKeyLength:
        i=0
        index = []
        blocks = separate_into_blocks(ciphertext, currentKeyLength)
        
        #Перебір всіх блоків Y
        while i < len(blocks):
            index.append(index_coincidence(blocks[i]))
            i += 1
        print(np.mean(index))
        currentKeyLength += 1
        
        

def find_key(ciphertext, keyLength):
    blocks = separate_into_blocks(ciphertext, keyLength)
    possibleKeyLetter1 = ''
    possibleKeyLetter2 = ''
    
    for block in blocks:
        mostCommonLetter = collections.Counter(block).most_common()[0]
        possibleKeyLetter1 += alphabet[(alphabet.index(mostCommonLetter[0]) - alphabet.index('о'))%32]
        possibleKeyLetter2 += alphabet[(alphabet.index(mostCommonLetter[0]) - alphabet.index('е'))%32]

        
    print(possibleKeyLetter1)
    print(possibleKeyLetter2)
    return ''
    

def clean_file(file):
    file = open(file).read()
    file = file.replace("\n","").replace('ё', 'е').lower()
    clearString = re.sub(r'[\W\s]+|[\d]+|_+', '',file).strip()
    return clearString
    

    
def encode_with_several_keys(plaintextFile):
    keys = ['он', 'ром', 'джин', 'тоник', 'шампанское', 'полныйбокал', 'красноесухое', 'текиласанрайз', 'грузинскоевино','полусладкоевино','полусладкоебелое','американовискилед','егермейстерредбулл','вермутводочкаоливка','японскийкосмополитен']
    plaintext = clean_file(plaintextFile)
    print(index_coincidence(plaintext))
    
    for key in keys:
        ciphertext = encode(plaintext, key)
        print(index_coincidence(ciphertext))
    
    print('______________________________________\n') 
        
def decode_task_ciphertext(ciphertextFile):
    ciphertext = clean_file(ciphertextFile)
    find_block_IC(ciphertext)
    print('______________________________________\n') 
    find_key(ciphertext, 17)
    print('______________________________________\n') 
    print(decode(ciphertext, "возвращениеджинна"))
    


encode_with_several_keys("plain.txt")
decode_task_ciphertext("cipher.txt")






