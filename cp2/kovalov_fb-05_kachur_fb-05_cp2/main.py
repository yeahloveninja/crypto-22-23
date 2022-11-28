from collections import Counter
#import matplotlib.pyplot as plt
#import seaborn as sns

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
letter_numb = dict(zip(alphabet, [l for l in range(32)]))
opposite_letter_numb = dict(zip([l for l in range(32)], alphabet))
signature = ["хм", "аут", "черт", "алиби", "адекватность", "некридитоспособность"]
with open("text1.txt", 'r', encoding='UTF-8') as file1:
    text = file1.read()
print(text)


def vigen(str_text, key):  # шифрование Виженером
    str_text_indexes = []
    key_indexes = []
    for l in str_text:
        if l in alphabet:  # ищу индексы букв
            letter = alphabet.index(l)
            str_text_indexes.append(letter)
    for l in key:  # ищу индексы ключа
        if l in alphabet:
            letter = alphabet.index(l)
            key_indexes.append(letter)
    len_str_text = len(str_text_indexes) # длинна текста и ключа
    len_key_indexes = len(key_indexes)
    if len_str_text % len_key_indexes == 0:  # сколько раз надо повторить ключ что б получить
        #  длинну текста
        key_indexes = key_indexes * (len_str_text // len_key_indexes)
    else:
        key_indexes = key_indexes * (len_str_text // len_key_indexes)
        diff_len = len_str_text - len(key_indexes)
        key_indexes = key_indexes + key_indexes[0:diff_len]
    sum0 = [x + y for x, y in zip(str_text_indexes, key_indexes)]  # добавляем индексы, шифрование
    for i in range(len(sum0)):
        sum0[i] = sum0[i] % 32 # 32 бо 32 буквы алфавита
    text = ""
    for i in sum0: # формирую шифрованый текст
        if i in [j for j in range(0, 33)]:
            text += alphabet[i]
    return text


# print(vigen(text, 'хм'))
def superdupersecretvigen(str_text, key): # расшифровка текста
    str_text_indexes = []
    key_indexes = []
    for l in str_text:
        if l in alphabet:
            letter = alphabet.index(l)
            str_text_indexes.append(letter)
    for l in key:
        if l in alphabet:
            letter = alphabet.index(l)
            key_indexes.append(letter)
    len_str_text = len(str_text_indexes)
    len_key_indexes = len(key_indexes)
    if len_str_text % len_key_indexes == 0:
        key_indexes = key_indexes * (len_str_text // len_key_indexes)
    else:
        key_indexes = key_indexes * (len_str_text // len_key_indexes)
        diff_len = len_str_text - len(key_indexes)
        key_indexes = key_indexes + key_indexes[0:diff_len]
    sum0 = [x - y for x, y in zip(str_text_indexes, key_indexes)]  # отнимает индексы ключа от шифрования
    for i in range(len(sum0)):
        sum0[i] = sum0[i] % 32
    text = ""
    for i in sum0:
        if i in [j for j in range(0, 33)]:
            text += alphabet[i]
    return text
# формируем шифрованый текст

def indexofsootvetstviya(text1):  # считаю по формуле с методы
    ind = 0
    chastota = Counter(text1)
    for i in chastota:
        ind += chastota[i] * (chastota[i] - 1)
    ind /= (len(text1) * (len(text1) - 1))
    return ind


textnames = ['enctext0', 'enctext1', 'enctext2', 'enctext3', 'enctext4', 'enctext5']
for i in range(len(textnames)):
    with open(f"enctext{i}.txt", 'r', encoding="utf-8") as file2:
        txtt = file2.read()
    print(f"My superdupertext{i} index ravno " + str(indexofsootvetstviya(txtt)))
print("Index of my obuchniytext: " + str(indexofsootvetstviya(text)))
# print(superdupersecretvigen('щянмбъфъьмесвмвсьсбщгхемщъжюс', 'хм'))
# for i in range(len(signature)):
# new_data = vigen(text, signature[i])
# with open(f"enctext{i}.txt", 'w', encoding="utf-8") as file2:
# file2.write(new_data)
with open("cypher.txt", 'r', encoding='UTF-8') as cypher:
    cyphertxt = cypher.read()


def minecrafttext(cyphertxt1, len_r): # делим текст на блоки
    Stevetext = []
    for i in range(len_r):
        Stevetext.append(cyphertxt1[i::len_r])
    return Stevetext


def dovzhuna_of_key(text3):
    r_index = []
    for r in range(2, 31):
        index = 0
        blocks = minecrafttext(text3, r)
        for i in range(r):
            index += indexofsootvetstviya(blocks[i])
        index /= r
        r_index.append(index)
    return r_index, r_index.index(max(r_index)) + 2 # добавил два, бо считал начиная с 2


print(dovzhuna_of_key(cyphertxt))


def popularity_letter(text):  # самая встречаемая буква
    popularityof_letters = Counter(text)
    max_popularity = max(Counter(text).values())
    for key, value in popularityof_letters.items():
        if value == max_popularity:
            return key


def searchingforakey(Steve):  # находим возможные буквы ключа
    needed_keys = []
    text_popular_letters = ["о", "е", "а", "и"]
    for i in range(len(Steve)):
        for_block = []
        cipher_popular_number = letter_numb[popularity_letter(Steve[i])]  # номер самой встречаемой буквы
        for j in text_popular_letters:
            text_popular_number = letter_numb[j]
            move = (cipher_popular_number - text_popular_number) % 32  # находим букву ключа
            for_block.append(opposite_letter_numb[move])
        needed_keys.append(for_block)
    return needed_keys

print(searchingforakey(minecrafttext(cyphertxt, 12)))

print(superdupersecretvigen(cyphertxt, "вшекспирбуря"))


#plt.figure(figsize=(10, 6))
#plt.yticks([r for r in range(31)])
#plt.xticks(rotation=20)

#sns.barplot(x=[str(r) for r in range(2, 31)], y=[0.03429321421542369, 0.03734839112182639, 0.03846786795894798, 0.032753684507439526, 0.04242249836150345, 0.032845671625834745, 0.038394305262087654, 0.037406913486166676, 0.034343106655826135, 0.03282596004503103, 0.05436955673586635, 0.032807635112857336, 0.034253133094361496, 0.03741441107403287, 0.03846816039387033, 0.0326076877752591, 0.042619239781400246, 0.03299852287693898, 0.03839407833306634, 0.03734596917614833, 0.03436346417856434, 0.03248823743567128, 0.05435416649918132, 0.032517536103743, 0.03434857665414954, 0.03762500312229972, 0.0383860390427654, 0.033132183908045974, 0.04250450051229374])

#plt.xlabel("Индекс совпадений")
#plt.ylabel("Длина ключа")
#plt.show()
#dt = pd.read_excel("lab2.xlsx")
#dt
#fig = plt.figure()
#sns.barplot(data=dt, x="Key_len", y="Index", palette='hls')
#plt.savefig('saved_figure.png')
#код с джупитера для галочки