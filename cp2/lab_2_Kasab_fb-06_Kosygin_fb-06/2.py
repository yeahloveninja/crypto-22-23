# --------------------------------------------------------------------------------------------Main
from shutil import rmtree
import os
NewDir = 'Result'
ParentDir = 'D:/ВСЁ МОЁ/KPI/SEM5/Крипта/Labs/crypto-22-23/cp2/lab_2_Kasab_fb-06_Kosygin_fb-06'
os.chdir(ParentDir)
path = os.path.join(ParentDir, NewDir)
if os.path.exists(NewDir) is True:
    rmtree(NewDir)
    os.mkdir(path)
else:
    os.mkdir(path)

with open('CipherTextVar1.txt', 'r', encoding='utf-8') as f:
    CipherTextVar1 = f.read()
with open('OpenText.txt', 'r', encoding='utf-8') as f:
    OpenText = f.read()

AlphaB32 = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
UpAlphaB32 = AlphaB32.upper()
UpFile = OpenText.upper()

Indexes = []
LC = ['2', '3', '4', '5', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
Keys = ['хм', 'бар', 'этот', 'понял', 'авантюризм', 'архимандрит', 'абаксиальный', 'академический', 'автотракторный', 'антирелигиозный', 'абажуродержатель', 'аббревиировавшись', 'абдоминоаортальный', 'неудовлетворительно', 'неттакихсловдватцать']
Result = f'{"Індекси відповідності":-^46}''\n'
CTReult = 'Індекси літер шифрованного тексту\n'
# --------------------------------------------------------------------------------------------Main
# --------------------------------------------------------------------------------------------VigenerCipher
def VigenerCipher(key, text, mode):
    EncryptedKavun = []
    Kindex = 0
    key = key.upper()

    for symbol in text:
        num = UpAlphaB32.find(symbol.upper())
        if num != -1:
            if mode == 'encrypt':
                num += UpAlphaB32.find(key[Kindex])
            elif mode == 'decrypt':
                num -= UpAlphaB32.find(key[Kindex])

            num %= len(UpAlphaB32)

            if symbol.isupper():
                EncryptedKavun.append(UpAlphaB32[num])
            elif symbol.islower():
                EncryptedKavun.append(UpAlphaB32[num].lower())

            Kindex += 1
            if Kindex == len(key):
                Kindex = 0
        else:
            EncryptedKavun.append(symbol)
    return ''.join(EncryptedKavun)
# --------------------------------------------------------------------------------------------VigenerCipher
# --------------------------------------------------------------------------------------------OpenTextIndex
def FindIndex(file):
    Index = 0
    for i in range(len(AlphaB32)):
        CounterCycle = file.count(UpAlphaB32[i])
        Index = Index + CounterCycle * (CounterCycle - 1)
    return Index * 1 / (len(file) * (len(file) - 1))
Result += 'Відкритого тексту:       ' + str(FindIndex(UpFile)) + '\n'

for i in Keys:
    CryptedFile = VigenerCipher(i, UpFile, 'encrypt')
    Indexes.append(FindIndex(CryptedFile))
for i, j  in dict(zip(LC, Indexes)).items():
    Result += 'Зашифрованного тексту ' + str(i) + ': ' + str(j) + '\n'
# --------------------------------------------------------------------------------------------OpenTextIndex
# --------------------------------------------------------------------------------------------ClosedTextIndex
def PandorasBox(file, length):
    Block = []
    for i in range(length):
        Block.append(file[i::length])
    return Block

def IndexMatchFinder(file):
    index = 0
    length = len(file)
    for i in range(len(AlphaB32)):
        countLetter = file.count(AlphaB32[i])
        index += countLetter * (countLetter - 1)
    return index * 1/(length*(length-1))

def IndexesBlocks(file, size):
    Index = 0
    Block = PandorasBox(file, size)
    for i in range(len(Block)):
        Index = Index + IndexMatchFinder(Block[i])
    return Index/len(Block)

def KeyTranslator(indexes, alpha):
    Letters = []
    for i in range(len(indexes)):
        Letters.append(alpha[indexes[i]])
    return Letters

def KeyFinder(file, letter_value, alpha):
    ListedFile = list(file.replace('\n', ''))
    Right = letter_value
    SplitFile =  []
    RepeatCounter = []
    MPLIM = []
    CompLST = {}

    for i in range(len(ListedFile) // letter_value + 1):
        TempraryList = []
        Left = i * letter_value

        for j in range(Left, Right):
            if j <= len(ListedFile) - 1:
                TempraryList.append(ListedFile[j])

        Right += letter_value
        SplitFile.append(TempraryList)

    for i in range(len(alpha)):
        CompLST[alpha[i]] = [0] * letter_value

    for i in range(len(SplitFile)):
        for j in range(letter_value):
            if j < len(SplitFile[i]):
                CompLST[SplitFile[i][j]][j] += 1

    for i in range(letter_value):
        RepeatsList = []
        for j in range(len(alpha)):
            RepeatsList.append(CompLST[alpha[j]][i])

        RepeatCounter.append(RepeatsList)
        MPLIM.append((RepeatCounter[i].index(max(RepeatCounter[i])) - 14) % len(alpha))
    return print(''.join(KeyTranslator(MPLIM, alpha)))
# --------------------------------------------------------------------------------------------ClosedTextIndex
# --------------------------------------------------------------------------------------------Outs
with open('Result/Idexes.txt', 'w', encoding='utf-8') as f: 
    f.write(Result)

for i in range(len(LC)):
    with open('Result/MyText' + str(LC[i]) + '.txt', 'w', encoding='utf-8') as f: 
        f.write(VigenerCipher(Keys[i], OpenText, 'encrypt'))

for i in range(1, len(AlphaB32) - 1):
    CTReult += str(i) + ' Индекс: ' + str(IndexesBlocks(CipherTextVar1, i)) + '\n'
print(CTReult)
with open('Result/CTLettersIdexes.txt', 'w', encoding='utf-8') as f: 
    f.write(CTReult)
KeyFinder(CipherTextVar1, int(input('Enter key length: ')), AlphaB32)

CloseKey = input('Введите ключ: ')
with open('Result/Var1decrypted.txt', 'w', encoding='utf-8') as f: 
        f.write(VigenerCipher(CloseKey, CipherTextVar1, 'decrypt'))
# --------------------------------------------------------------------------------------------Outs

# MPLIM - Most Popular Letters Indexes Massive