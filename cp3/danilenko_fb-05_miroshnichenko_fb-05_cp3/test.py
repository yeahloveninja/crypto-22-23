from math import gcd
f = open("13.txt")
text = f.read()
text = text.replace("\n", "")

def extended_euclid(a, b):
    """ Повертає d=НСД(x,y) і x, y такі, що ax + by = d """
    if b == 0 :
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y

def inverse(a,b):
    """Обернене за модулем"""
    k = list(extended_euclid(a,b))[1]
    return k

def solve_eq(a, b, n):
    """Розв'язування лінійних порівнянь"""
    roots = []
    d = gcd(a, n)
    if d == 1:
        roots.append((inverse(a, n) * b) % n)
    else:
        if (b % d) == 0:
            res = (inverse(int(a / d) * int(b / d) , int(n / d))) % int(n / d)
            for i in range(d):
                roots.append(res + i * int(n / d))
        else:
            roots.append(-1)
    return roots

top_bigrams = ['ст','но','то','на','ен']

alphavit = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
                   'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
letters_bi = []
for i in alphavit:
    for j in alphavit:
        letters_bi.append(i+j)

def fr_bi(t):
    """Частоти біграм (що не перетинаються) у тексті;
    повертає список з найчастішими біграмами"""
    all_off_bi_not_cross = []
    for i in range(0, len(t) - 2, 2):
        all_off_bi_not_cross.append(t[i] + t[i + 1])
    fr = {}
    for i in letters_bi:
        fr[i] = all_off_bi_not_cross.count(i)/(2 * len(all_off_bi_not_cross))
    print(fr)
    top_bi_var = []
    for i in range(5):
        k = list(sorted(fr.items(), key=lambda item:item[1], reverse=True))
        top_bi_var.append(k[i][0])
    return top_bi_var

top_bigrams_var = fr_bi(text)

def to_num(a):
    """Переведення біграми у число"""
    l = list(a)
    num = alphavit.index(l[0])*31 + alphavit.index(l[1])
    return num

def to_let(n):
    """Переведення числа у біграму"""
    x = n%31
    y = (n-x)//31
    w = []
    w.append(alphavit[y])
    w.append(alphavit[x])
    return ''.join(w)

def decrypt(t, a, b ):
    """Розшифрування тексту (t) за допомогою клуча (a,b)"""
    a1 = inverse(a,961)
    decr = []
    all_bi = []
    for i in range(0, len(t) - 2, 2):
        all_bi.append(t[i] + t[i + 1])
    for i in all_bi:
        Xi = ( a1 * (to_num(i) - b) ) % 961
        print(to_let(Xi))
        decr.append(to_let(Xi))
    return ''.join(decr)

def fr_l(text):
    all_l = list(text)
    fr = {}
    for i in letters_bi:
        fr[i] = all_l.count(i) / (2 * len(all_l))
    top_bi_var = []
    for i in range(5):
        k = list(sorted(fr.items(), key=lambda item: item[1], reverse=True))
        top_bi_var.append(k[i][0])
    return top_bi_var


def check(text):
    top_l = ('оеа')
    let_count = 0
    for let in text:
        let_count += 1
    for c in top_l:
        t = 0
        for i in text:
            if c == i:
                t += 1
        if c == 'о' and t*100/let_count < 7:
            return False
        if c == 'е' and t*100/let_count < 6:
            return False
        if c == 'а' and t*100/let_count < 6:
            return False
    return True


print(to_num('яф'))
print(top_bigrams)
print(top_bigrams_var)
keys = []
for i in range(0,4):
    for j in range (0,5):
        for n in range(0,5):
            if n==j:
                continue
            X1 = to_num(top_bigrams[j])
            X2 = to_num(top_bigrams[n])
            Y1 = to_num(top_bigrams_var[i])
            Y2 = to_num(top_bigrams_var[i+1])
            print(top_bigrams_var[i+1])
            print(X1, X2, Y1, Y2)
            a = solve_eq((X1 - X2), (Y1 - Y2), 961)
            print(a)
            for f in a:
                if f != -1:
                    k = (f,((Y1 - f*X1) % (31*31)))
                    keys.append(k)
print(keys)

result = ''
for k in keys:
    decod = decrypt(text, k[0], k[1])
    if check(decod):
        print(str(k)+'\n'+decod)
        result = decod

print(result)