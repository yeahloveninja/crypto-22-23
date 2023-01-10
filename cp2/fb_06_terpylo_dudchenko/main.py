import re
import collections

with open('text1.txt', 'r', encoding='utf-8') as file1:
    note = file1.read()
    note = note.replace("\n", "")
    note = note.lower()
    note = note.replace(" ", "").replace("  ", " ")
    note = re.sub(r'[^а-яё]', '', note)
    note = note.replace("ё", "е")

with open("Variant2.txt", 'r', encoding='utf-8') as file2:
    note2 = file2.read()
    note2 = note2.replace('\n', "")

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х','ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

def Calculate_index_of_vidpovidnosti(text):
    x = dict(collections.Counter(text))
    i = []
    for key in list(x.keys()):
        i.append(x[key] * (x[key] - 1))
    I = 1 / (len(text) * (len(text) - 1)) * sum(i)
    return (I)


def Decoding(Ciphertext, kluch):
    g = 0
    text = ''
    for i in Ciphertext:
        text += alphabet[(alphabet.index(i) + 32 - alphabet.index(kluch[g])) % 32]
        g += 1
        if (g >= len(kluch)):
            g = 0
    return (text)


def Encoding(text, kluch):
    Ciphertext= ''
    g = 0
    for i in text:
        Ciphertext += alphabet[(alphabet.index(i) + alphabet.index(kluch[g])) % 32]
        g += 1
        if (g >= len(kluch)):
            g = 0
    return (Ciphertext)

def Break_into_blocks(text, r):
    bl = list()
    for i in range(r):
        bl.append('')
        j = i
        while (j < len(text)):
            bl[i] = bl[i] + text[j]
            j += r
    return bl

def Calculate_index_of_vidpovidnosti_for_echa_blocks(text, r):
    blocks = Break_into_blocks(text, r)
    ind = 0
    for i in range(len(blocks)):
        ind = ind + Calculate_index_of_vidpovidnosti(blocks[i])
    ind = ind / r
    return ind

def FindKluch(text, r, bukva):
    blocks = Break_into_blocks(text, r)
    litera = ''
    for b in blocks:
        tmp = collections.Counter(b).most_common(1)[0]
        litera += alphabet[(alphabet.index(tmp[0]) - alphabet.index(bukva)) % 32]
    print(litera)





def Task1(text):
    kluchi = ['да', 'меч', 'каша', 'клуша', 'алвфцугевс', 'ануфяригвуй', 'апенуисывфях', 'смваншйфвхзяа',
              'пвсяфцщшгртиаз', 'рсфчяьжщшфйцапж', 'дывлнкуйячтисбнэ', 'ймсекоглздшйытсна', 'напвыфтлджзщшераиц',
              'жднегкуасмиытврапйя', 'нкраимвыфячждлгшщитр']
    print("Iндекс відповідності для відкритого тексту:", Calculate_index_of_vidpovidnosti(text), "\n")
    for i in kluchi:
        print("Довжина ключа", len(i), ":", Calculate_index_of_vidpovidnosti(Encoding(text, i)))





def Task2(text):
    for i in range(2, len(alphabet)):
        print("Довжина ключа", i, ':', Calculate_index_of_vidpovidnosti_for_echa_blocks(text, i))
    for letter in 'оеа':
        FindKluch(note2, 13, letter)
    print(Decoding(text, 'последнийдозор'))
