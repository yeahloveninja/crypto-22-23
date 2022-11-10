import pandas as pd
f = open("encr.txt", encoding='utf-8')
text = f.read()
text = text.replace("\n", "")

Letters = []
for i in range(ord('а'), ord('я')+1):
    Letters.append(chr(i))


#букви -> цифри
def ToNum(t):
    inNum = []
    for i in t:
        inNum.append(Letters.index(i))
    return inNum

#цифри -> букви
def ToLet(t):
    inLet = []
    for i in t:
        inLet.append(Letters[i])
    return ''.join(inLet)

def ToBlock(text, lenBlock):
    blocks = []
    i = 0
    while (i < lenBlock):
        blocks.append(text[i])
        i = i+1
    for j in range(lenBlock, len(text)):
        blocks[j%lenBlock] += text[j]
        j = j+1
    return blocks

def Index(text):
    s=0
    for i in Letters:
        s = s + text.count(i)*(text.count(i)-1)
    index = (1/(len(text)*(len(text)-1))) * s
    return index

def SumIndex(list):
    s = 0
    for i in list:
        s+=Index(i)
    return s/len(list)


def get_key(val, dictionary):
    for key, value in dictionary.items():
        if val == value:
            return key

def find_key_len():
    I_teor = 0.055
    indexes={}
    for i in range(2,32):
        indexes[i]= (SumIndex(ToBlock(text, i)))
    print(indexes)
    f = pd.DataFrame(indexes, index=["index"])
    f.to_excel("indexes.xlsx")
    keys = []
    for index in indexes.values():
        if index > I_teor:
            keys.append(index)
    lenKey = get_key(min(keys), indexes)
    return lenKey
KeyLen=find_key_len()

print("Довжина ключа: ", KeyLen)
freq_letters=['о', 'е', 'а'] #найчастіші букви в рос. алфавіті

def fr(text):
    freq = {}
    for i in text:
        freq[i] = text.count(i)/len(text)
    k = 0
    k = dict(sorted(freq.items()))
    return k


def key_search(blocks):
    Y_list = [] #список найчастіших літер у кожному блоці шифрованого тексту
    for block in blocks:
        freq = fr(block)
        y = get_key(max(freq.values()), freq)
        Y_list.append(y)
    keys = [] # значення ключа
    for i in Y_list:
        key = (Letters.index(i) - Letters.index(freq_letters[0]))% len(Letters)
        keys.append(key)
    final_key = ToLet(keys)
    return final_key

print('Отриманий ключ - ', key_search(ToBlock(text, KeyLen)))
print('Змістовний ключ - последнийдозор')


def VigenerD(text,key):
    text = ToNum(text)
    key = ToNum(key)
    PairsLet = {}
    iter = 0
    NumL = 0

    #словник (номер букви в тексті: номер букви ВТ, номер букви К )
    for i in text:
        PairsLet[NumL] = [i, key[iter]]
        NumL += 1
        iter += 1
        if (iter >= len(key)):
            iter = 0
    #список символів ШТ в цифрах
    l = []
    for v in PairsLet:
        go = (PairsLet[v][0] - PairsLet[v][1] + len(PairsLet))%32
        l.append(go)
    DecText = ToLet(l)  #шт
    return DecText
print(VigenerD(text, 'последнийдозор'))

f = open('decode.txt', 'w')
f.write(VigenerD(text, 'последнийдозор'))
