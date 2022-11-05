from random import randint
import os
from Change_Symbols import Change_Symbols
from Crypto import Letters_Amount

log = "" #Рядок, куди записується все, що відбувається в програмі, і занесеться у файл

def File_Update(path):
    if os.path.exists(path):
        os.remove(path)

def alpa(alpha): #Створює словник, де ключ - буква алфавіту, значення - порядковий номер букви
    alp = {}
    ind = 0
    for l in alpha:
        alp[l] = ind
        ind += 1

    return alp

def keys(n, alpha): #Створює рандомний ключ заданої довжини
    i = 0
    key = ""
    while i < n:
        key += alpha[randint(0,31)]
        i += 1
    return key


def Viginer_Encrypt(p_text, key, alpha): #Зашифрування тексту шифром Віженера
    print("key:  ", key)
    alp = alpa(alpha)

    c_text = ""
    i = 0
    while i < len(p_text):
        id = (alp[p_text[i]] + alp[key[i%len(key)]]) % len(alpha)
        c_text += alpha[id]
        i += 1

    return c_text

def Viginer_Decrypt(c_text, key, alpha): #Розшифровка тексту із шифром Віжінера
    print("key: ", key)
    alp = alpa(alpha)

    p_text = ""
    i = 0
    while i < len(c_text):
        id = (alp[c_text[i]] - alp[key[i%len(key)]]) % len(alpha)
        p_text += alpha[id]
        i += 1

    return p_text

def index(text, alpha): #Рахує індекс відповідності
    id = 0

    for l in alpha:
        sum = 0
        for w in text:
            if w == l:
                sum += 1

        id = id + sum*(sum-1)

    if len(text) > 1:
        id = id/(len(text)*(len(text)-1))

    return id

def grouper(txt, n): #Розбиває текст на блоки заданої довжини
    x = []
    i = 0

    while i < n:
        x.append("")
        i += 1

    for id in range(0, len(txt)):
        x[id%n] += txt[id]

    return x


def key_analysis(letter, alpha, popular): #Знаходить потенційну літеру ключа, шляхом маніпуляцій з найпопулярнішою літерою алфавіту і найбільш популярною літерою в блоці зашифрованого тексту
    id = (alpha.index(letter) - alpha.index(popular)) % len(alpha)
    return alpha[id]


def Viginer_Analise(c_text, alpha, popular, log, begin=2, end=None):
    if end is None:
        end = len(alpha) + 1

    log = log + "Index of cipher text: " + str(index(c_text, alpha)) + "\n"

    strk1 = ""
    r = []

    for i in range(begin, end):
        ind = []
        blocks = grouper(c_text, i) #разбиваємо текст на блоки
        for bl in blocks:
            ind.append(index(bl, alpha)) #індекс відповідності для блоку
        r.append(sum(ind)/len(ind)) #середнє значення індексу відповідності для блоків заданої довжини
        strk1 = strk1 + "index forlength blocks " + str(i) + ";" + str(sum(ind)/len(ind)) + "\n"

    log = log + strk1

    potential = {}
    for ri in r:
        if ri > 0.05:
            potential[ri] = r.index(ri) + begin #потенційна довжина ключа

    log = log + "Potential length of key\n" + str(potential) + "\n"

    period = True
    for ri in potential:
        if potential[ri] % list(potential.values())[0] != 0:
            period = False

    if period:
        period_key = list(potential.values())[0]
        print("length of key: ", period_key)
        log = log + "length of key: " + str(period_key) + "\n"
    else:
        print("Program cann't find regularity. You need analyse it by yourself")
        print(potential)
        period_key = input("Input length of key: ")
        log = log + "custom length of key: " + str(period_key) + "\n"

    blocks = grouper(c_text, period_key)
    list_keys = []
    for i in range(0,len(popular)):
        list_keys.append("")

    for bl in blocks:
        l = list(dict(Letters_Amount(bl, alpha)).keys())[0]
        for i in range(0, len(list_keys)):
            list_keys[i] += key_analysis(l, alpha, popular[i]) #Список потенційних ключів

    log = log + "List of potential keys\n" + str(list_keys) + "\n\n\nDecrypted first block\n"
    for el in list_keys:
        #print(Viginer_Decrypt(c_text[0:16], el, alpha))
        log = log + "key:  " + el + "\n      " + Viginer_Decrypt(c_text[0:period_key], el, alpha) + "\n" #Розшифрування перших n символів тексту, де n - довжина ключа

    path = os.getcwd()+r'\decrypt.txt' #Шлях до розшифрованого тексту
    #hack_key = list_keys[0]
    hack_key = "делолисоборотней" #Ключ!!!!
    with open(path, 'w') as d:
        d.write(Viginer_Decrypt(c_text, hack_key, alpha)) #Розшифровка тексту прямо у файл

    log = log + "\n\nWe hack Vigenere cipher\nKey: " + hack_key + "\n"
    with open(log_path, 'w') as logi:
        logi.write(log) #Запис логів у файл


if __name__ == '__main__':
    print("start proga")
    alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    popular = "оеаин"
    key_len = (2,3,4,5,randint(10,20)) #Множина яка складаються з цифр, які ми будемо використовувати як довжину ключа

    path = os.getcwd() +r'\plain.txt' #Шлях до відкритого тексту
    res_path = os.getcwd() + r'\result.txt' #Шлях до зашифрованого тексту різними ключами
    cip_path = os.getcwd() + r'\cipher.txt' #Шлях до зашифрованого тексту з варіанта
    log_path = os.getcwd() + r'\log.txt' #Шлях до логів програми
    File_Update(res_path) #Очистити файл для зашифрованого тексту різними ключами
    File_Update(log_path) #Очистити файл із логами

    print("Modifying file")
    log = log + "modifying file\n"
    mod_path = Change_Symbols(path, False)
    with open(mod_path, 'r') as f:
        text = f.read()
        f.seek(0)
    log = log + "\n\n\nindex for plain text: " + str(index(text, alpha)) + '\n'

    print("encryption")
    log = log + "Encryption\n"
    for k in key_len:
        key = keys(k, alpha) #отримуємо ключ
        result = Viginer_Encrypt(text, key, alpha) #отримуємо зашифрований текст
        log = log + "index for cipher text wih key " + key + ": " + str(index(result, alpha)) + "\n"
        with open(res_path, 'a') as res: #записуємо результат у файл
            res.write("key: "+key+"\n"*2)
            res.write(result+"\n"*2)

    print("Decryption")
    log = log + "\n\n\n\nDecryption\n"
    cip_mod = Change_Symbols(cip_path, False)
    with open(cip_mod, 'r') as f:
        cipher = f.read()
        f.seek(0)
    Viginer_Analise(cipher, alpha, popular, log) #Зламуємо шифр

    print('the end')
