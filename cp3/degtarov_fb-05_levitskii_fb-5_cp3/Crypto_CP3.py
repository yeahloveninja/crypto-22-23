from collections import Counter
from itertools import product
from textwrap import wrap

class Cipher:
    def __init__(self):
        self.alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
        self.n = 31
        self.nn = 961
        self.natural_bigram = ['ст', 'то', 'ен', 'но', 'пр']
        self.natural_bigram_int = [self.bigram_to_int(i) for i in self.natural_bigram]
        self.keys = []

    def gcd(self, a, b):
        if b == 0:
            return abs(a)
        else:
            return self.gcd(b, a % b)

    def build_bigrams(self, txt: str): # формування біграм
        c = Counter(wrap(txt, 2)).most_common(5)
        return [i[0] for i in c]

    def bigram_to_int(self, bigram): # біграм в числа
        return self.alphabet.index(bigram[0]) * self.n + self.alphabet.index(bigram[1])

    def int_to_bigram(self, number): # із числа в біграму
        return self.alphabet[number // self.n] + self.alphabet[number % self.n]

    def inverted_by_mod(self, a, n): # обернений по модулю
        u0, u1 = 1, 0
        if n != 0:
            while a % n:
                q = a // n
                u0, u1 = u1, u0 - q * u1
                a, n = n, a % n
        return u1

    def linear_expression_solver(self, a, b, n): # лінійне рівняння
        g = self.gcd( a, n)
        if g == 1:
            return [(self.inverted_by_mod(a, n) * b) % n]
        if b % g:
            return []
        a, b, n = map(lambda x: x % n, (a, b, n))
        if n != 0:
            answ = [(self.inverted_by_mod(a, n) * b) % n]
            for i in range(1, g):
                answ.append(answ[i - 1] + n * i)
        else:
            answ = [(self.inverted_by_mod(a, n) * b) % (n + 1)]
            for i in range(1, g):
                answ.append(answ[i - 1] + n * i)
        return answ

    def system_solver(self, x1, x2, y1, y2): # система рівнянь
        return [(i, (y1 - i * x1) % self.nn) for i in self.linear_expression_solver(x1 - x2, y1 - y2, self.nn)]

    def decrypt(self, text, a, b): # розшифрування
        answ = ''
        for i in wrap(text, 2):
            y = self.bigram_to_int(i)
            x = (self.inverted_by_mod(a, self.nn) * (y - b)) % self.nn
            answ += self.int_to_bigram(x)
        return answ

    def is_natural_text(self, txt): # перевірка результуючого тексту
        c = Counter(txt)
        _len = len(txt)
        for i in c:
            c[i] /= _len
        return c['ф'] < 0.003 and c['ц'] < 0.004 and c['щ'] < 0.006


    def get_keys(self, text): # функція перебору ключів
        encrypted_bigram = self.build_bigrams(text)
        encrypted_bigram_int = [self.bigram_to_int(i) for i in encrypted_bigram]

        for x1, y1, x2, y2 in product(self.natural_bigram_int, encrypted_bigram_int, repeat=2):
            if x1 == x2 or y1 == y2:
                continue
            for a, b in self.system_solver(x1, x2, y1, y2):
                if (a, b) in self.keys:
                    continue
                else:
                    self.keys.append((a, b))
                d_text = self.decrypt(text, a, b)
                if self.is_natural_text(d_text):
                    X1 = self.int_to_bigram(x1)
                    Y1 = self.int_to_bigram(y1)
                    X2 = self.int_to_bigram(x2)
                    Y2 = self.int_to_bigram(y2)
                    print(f""" X : {X1, X2}, Y : {Y1, Y2} 
a = {a}, b = {b}
{d_text}""")
with open("12var.txt", 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', '')

cipher = Cipher()
cipher.get_keys(text)