from collections import Counter
import math

alphabet_without_spaces = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

with open("03.txt", encoding='utf8') as file:
    file_to_decrypt = file.read()
encrypted_text = ''.join(i for i in file_to_decrypt if i in alphabet_without_spaces)

mode_bigrams = ['ст', 'но', 'то', 'на', 'ен']
mode_letters = ['о', 'а', 'е']


def my_gcd(a, b):  # пошук НСД
    if b == 0:
        if a < 0:
            return -a
        else:
            return a
    else:
        return my_gcd(b, a % b)


def my_expanded_gcd(a, m):  # обчислення оберненого за розширеним алгоритмом Евкліда
    ans = [0, 1]
    while a != 0 and m != 0:
        if a > m:
            ans.append(a // m)
            a = a % m
        elif m > a:
            ans.append(m // a)
            m = m % a
        else:
            print('Inverse does not exist')
    for i in range(2, len(ans) - 1):
        ans[i] = ans[i - 2] + (-ans[i]) * ans[i - 1]
    return ans[-2]


def my_mod_equation(a, b, m):  # розв'язування рівняння
    a, b = a % m, b % m  # шукаємо лишок
    d = my_gcd(a, m)  # НСД  a і m
    ans = []
    if d == 1:  # якщо НСД 1
        ans.append((my_expanded_gcd(a, m) * b) % m)  # то тільки один корінь
        return ans
    else:
        if b % d != 0:  # немає коренів
            return ans
        else:
            a, b, m = a // d, b // d, m // d  # буде d коренів
            ans.append((my_mod_equation(a, b, m)[0]))
            for i in range(1, d):
                ans.append(ans[-1] + m)
            return ans  # всі корені


def my_bigrams_frequency(txt):  # частота біграм
    c = Counter()
    frequency = {}
    alph = alphabet_without_spaces
    for letter1 in alph:
        for letter2 in alph:
            bigram = letter1 + letter2
            c[bigram] = 0
    for i in range(len(txt) - 1):  # до останньої літери
        bigram = txt[i] + txt[i + 1]
        c[bigram] += 1  # рахуємо скільки разів зустрічається біграма
    for bigram in c.keys():
        frequency[bigram] = c[bigram] / sum(c.values())  # частота кожної біграми
    d = list(sorted(frequency.items(), key=lambda item: item[1], reverse=True))[:5]
    sort = []
    for i in range(len(d)):
        sort.append(d[i][0])
    return sort  # 5 найчастіших біграм


def bigram_to_num(bigram):  # переводимо біграму в число
    num = alphabet_without_spaces.index(bigram[0]) * 31 + alphabet_without_spaces.index(bigram[1])
    return num


def make_set(txt):  # робимо систему рівнянь з біграм
    mode_bigrams_cipher = my_bigrams_frequency(txt)  # найчастіші біграми в ШТ
    bigrams = []
    math_statement = []
    for i in mode_bigrams:
        for j in mode_bigrams_cipher:
            bigrams.append((i, j))  # система (біграма ВТ, біграма ШТ)
    for bigram1 in bigrams:
        for bigram2 in bigrams:
            if bigram1 == bigram2:  # якщо біграми одинакові
                continue
            elif (bigram2, bigram1) in math_statement:  # або така система біграм вже є
                continue
            elif bigram1[0] == bigram2[0]:  # або перші біграми однакові
                continue
            elif bigram1[1] == bigram2[1]:  # або другі біграми однакові
                continue  # пропускаємо
            math_statement.append((bigram1, bigram2))  # система (біграма ВТ, біграма ШТ)
    return math_statement


def my_roots(set):  # знаходимо корені системи рівнянь
    roots = []
    sub1 = bigram_to_num(set[0][0]) - bigram_to_num(set[1][0])  # різниця перших біграм системи
    sub2 = bigram_to_num(set[0][1]) - bigram_to_num(set[1][1])  # різниця других біграм системи
    a = my_mod_equation(sub1, sub2, 31 ** 2)  # формула (2)
    for dig in a:
        if my_gcd(dig, 31) != 1:
            continue
        b = (bigram_to_num(set[0][1]) - dig * bigram_to_num(set[0][0])) % 31 ** 2  # знаходимо b за формулою
        roots.append((dig, b))
    return roots  # корені (а, b)


def to_reveal(txt):  # підбираємо ключі для системи біграм
    k = []
    system = make_set(txt)  # робимо систему біграм
    for i in system:
        roots = my_roots(i)  # знаходимо корені рівняння для кожної системи
        if len(roots) != 0:
            for j in range(len(roots)):
                k.append(roots[j])
    return k  # ключ для системи біграм


def H(txt):  # обраховуємо ентропію тексту
    total = 0
    frequency = Counter(txt)
    for i in frequency.values():
        i /= len(txt)
        if i > 0:
            total += i * math.log2(i)
    h = -total
    return h


def my_decryption(txt, revealed_keys):  # функція для дешифрування
    deciphered = []
    a, b = revealed_keys[0], revealed_keys[1]  # ключі системи біграм
    for i in range(0, len(txt) - 1, 2):
        x = (my_expanded_gcd(a, 31 ** 2) * (bigram_to_num(txt[i:i + 2]) - b)) % (31 ** 2)  # формула дешифрування
        deciphered.append(alphabet_without_spaces[x // 31] + alphabet_without_spaces[x % 31])  # заповнюємо ВТ літерами
    decrypted = ''.join(i for i in deciphered)
    return decrypted  # ВТ


def is_correct(revealed_keys, txt):  # знаходимо пару правильних ключів
    for i in revealed_keys:
        deciphered = my_decryption(txt, i)  # розшифровуємо текст
        d = list(sorted(Counter(deciphered).items(), key=lambda item: item[1], reverse=True))
        sorted_d = []
        for j in range(len(d)):
            sorted_d.append(d[j][0])  # найчастіші літери в розшифрованому тексті
        if sorted_d[0] not in mode_letters:  # пропускаємо якщо це не найчастіші літери в дійсності
            continue
        h_theor = 4.35  # теоретичне значення ентропії для рос. мови
        h = H(my_decryption(txt, i))  # ентропія розшифрованого тексту
        if (h > h_theor - 0.2) and (h < h_theor + 0.2):  # перевіряємо чи приближена вона по значенню до теор.
            return i
    return -1


print(my_bigrams_frequency(encrypted_text))
a_b = is_correct(to_reveal(encrypted_text), encrypted_text)
print(a_b)
print(to_reveal(encrypted_text))
decrypt = my_decryption(encrypted_text, a_b)
print(decrypt)
name = open('decrypted.txt', 'w', encoding='utf8')
name.write(decrypt)
