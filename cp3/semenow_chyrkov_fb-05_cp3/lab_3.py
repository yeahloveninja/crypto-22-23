from collections import Counter
import math
import re


def top_five_bigrs(text):
    test = re.findall('\w\w', text)
    res = Counter(test)
    counter = 0
    for i in res.values():
        counter += i
    for i in res:
        res[i] = float(res[i]/counter)
    dct = dict(res)
    sorted_dict = {}
    sorted_keys = sorted(dct, key=dct.get)
    for w in reversed(sorted_keys):
        sorted_dict[w] = dct[w]
    res = []
    for row in list(sorted_dict.keys())[:5]:
        res.append(row)
    return res


def evclid_extended(first_number, second_number):
    if first_number == 0:
        return second_number, 0, 1
    else:
        div, koef_x, koef_y = evclid_extended(second_number % first_number, first_number)
    return div, koef_y - (second_number // first_number) * koef_x, koef_x


def mod_inverse(first_number, second_number):
    return list(evclid_extended(first_number, second_number))[1]


def sys_of_eq(koef_a, koef_b, m):
    solutions = []
    mod = math.gcd(koef_a, m)
    if mod != 1:
        if koef_b % mod != 0:
            solutions.append(False)
        else:
            root = (mod_inverse(int((koef_a / mod) * (koef_b / mod)),int((m / mod))) % (m / mod))
            for i in range(mod):
                solutions.append(root + i * int(m / mod))
    else:
        solutions.append((mod_inverse(koef_a, m) * koef_b) % m)
    return solutions


def bigram_to_num(bigr):
    return alphabet.index(list(bigr)[0])*len_alphabet + alphabet.index(list(bigr)[1])


def num_to_bigram(n):
    x = n % len_alphabet
    y = (n - x) // len_alphabet
    return f'{alphabet[y]}{alphabet[x]}'


def decipher(text, first_key, second_key):
    inversed_first_key = mod_inverse(first_key, len_alphabet ** 2)
    ans = ''
    all_bigrams = re.findall(r'\w\w', text)
    for k in all_bigrams:
        deciphered_letter = (inversed_first_key * (bigram_to_num(k) - second_key)) % len_alphabet ** 2
        ans += num_to_bigram(deciphered_letter)
    return ans


def check_bigrams(text, bigrams):
    bigrams = bigrams.split(',')
    for i in bigrams:
        if i in text:
            return False
    return True


def main(text):
    p = 0
    while p < 4:
        for l in range(0, 5):
            for m in range(0, 5):
                if m == l:
                    continue
                x_one = bigram_to_num(freq_bigrams_static[l])
                y_one = bigram_to_num(top_five_bigrs(text)[p])
                x_two = bigram_to_num(freq_bigrams_static[m])
                y_two = bigram_to_num(top_five_bigrs(text)[p+1])
                roots = sys_of_eq((x_one - x_two), (y_one - y_two), len_alphabet ** 2)
                for root in roots:
                    if root is not False:
                        key = root, (y_one - root * x_one) % (len_alphabet ** 2)
                        deciphered_text = decipher(text, key[0], key[1])
                        if check_bigrams(deciphered_text, wrong_bigrams):
                            print(f'Decifred text is:\n{deciphered_text}\n'
                                  f'Key for deсifred text is:\n{key[0]} {key[1]}')
                            return
                            
        p += 1


txt = open("utf8.txt", encoding='utf-8').read().replace('\n', '')
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
len_alphabet = len(alphabet)
freq_bigrams_static = ['ст', 'но', 'то', 'на', 'ен']
wrong_bigrams = 'аь,бй,бф,гщ,еь,жй,жц,жщ,жы,уь,фщ,хы,хь,цщ,цю,чф,чц,чщ,чы,чю,шщ,шы,шю,щг,щж,щл,щх,щц,щч,щш,щы,щю,щя,ыь,ьы,эа,эж,эи,эо,эу,эщ,эы,эь,эю,эя,юы,юь,яы,яь,ьь,гг'

if __name__ == "__main__":
    main(txt)