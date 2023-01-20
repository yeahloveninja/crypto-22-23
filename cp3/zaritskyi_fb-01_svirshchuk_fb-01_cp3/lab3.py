import collections
import re
from itertools import product, groupby

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

def clean_file(file):
    file = open(file, mode="r", encoding="utf-8").read()
    file = file.replace("\n","").replace('ё', 'е').replace('ъ', 'ь').lower()
    clearString = re.sub(r'[\W\s]+|[\d]+|_+', '',file).strip()
    return clearString

clearString = clean_file("lab3.txt")

def GCD(a, b):
    if (b == 0):
        return a
    return GCD(b, a % b)

def extended_euclid(a, b):
        if (b == 0):
            return a, 1, 0
        
        d, x, y = extended_euclid(b, a % b)
        return d, y, x - (a // b) * y

def inverse_modulo(a, b):
    if (GCD(a, b) != 1):
        return None
    
    return extended_euclid(a, b)[1]

def calc_linear_equation(a, b, m):
    if (GCD(a, m) == 1):        
        aInversed = inverse_modulo(a, m)
        return (aInversed * b) % m
    
    elif (GCD(a, m) > 1):
        d = GCD(a, m)
        
        if (b % d == 0):
            a1 = a / d
            b1 = b / d
            m1 = m / d
            a1Inversed = inverse_modulo(a1, m1)
            x0 = (a1Inversed * b1) % (m1)    
            solutions = []
            i = 0
            
            while i < d:
                solutions.append(x0 + i * m1)
                i += 1
            return solutions
        
        return "Рівняння не має розв'язків, оскільки b не ділиться на d"

def find_frequent_bigrams(string):
    bigrams = []
    
    for letter in range(0, len(string) - 2, 2):
        bigrams.append(string[letter] + string[letter + 1])
    
    bigramsAmount = dict(collections.Counter(bigrams))
    mostFrequentBigrams = collections.Counter(bigramsAmount).most_common(5)
    print(mostFrequentBigrams)
    return [mostFrequentBigrams[0][0], mostFrequentBigrams[1][0], mostFrequentBigrams[2][0], mostFrequentBigrams[3][0], mostFrequentBigrams[4][0]]
    

def bigrams_comparison(bigrams):
    frequentTerroristBigrams = ['ст', 'но', 'то', 'на', 'ен']
    combinations = []
    for i, j, n, k in product(bigrams, frequentTerroristBigrams, bigrams, frequentTerroristBigrams):
            if n != i and j != k:
                combinations.append([[i, j], [n, k]])
    return combinations

def find_possible_keys(bigrams):
    allKeys=[]
    m = 31
    for letters in bigrams:
        Y1 = alphabet.index(letters[0][0][0]) * m + alphabet.index(letters[0][0][1])
        X1 = alphabet.index(letters[0][1][0]) * m + alphabet.index(letters[0][1][1])
        Y2 = alphabet.index(letters[1][0][0]) * m + alphabet.index(letters[1][0][1])
        X2 = alphabet.index(letters[1][1][0]) * m + alphabet.index(letters[1][1][1])
        
        a = calc_linear_equation((X1 - X2), (Y1 - Y2), m ** 2)
        if a == "Рівняння не має розв'язків, оскільки b не ділиться на d":
            continue
        
        elif type(a) == list:
            for i in a:
                b = (Y1 - i * X1) % (m ** 2)           
                if GCD(i, m ** 2) != 1:
                    continue
                allKeys.append([int(i), int(b)])
                
        elif type(a) == int:
            b = (Y1 - a * X1) % (m ** 2)
            if GCD(a, m ** 2) != 1:
                continue
            allKeys.append([int(a), int(b)])
            
    allKeys.sort()
    allKeys = list(i for i, _ in groupby(allKeys))
    return allKeys

def decode(a, b, ciphertext):
    m = 31
    plaintext = ''
    for letter in range(0, len(ciphertext) - 2, 2):
        Y = alphabet.index(ciphertext[letter]) * m + alphabet.index(ciphertext[letter + 1])
        a1 = inverse_modulo(a, m ** 2)
        X = (a1 * (Y - b)) % (m ** 2)
        x2 = X % m
        x1 = (X - x2) // m
        plaintext = plaintext + alphabet[x1] + alphabet[x2]
    return plaintext

def correct_keys(keys,text):
    frequentTerroristLetter = ['о', 'а', 'е']
    unrealBigrams = ['аь', 'уь', 'яь', 'юь', 'еь', 'оь', 'йь', 'ыь' 'иь', 'эь', ]
    keyVariants = []
    for key in keys:
        a = key[0]
        b = key[1]
        plainText = decode(a, b, text)
    
        bigrams = []
        for letter in range(0, len(plainText) - 1):
            bigrams.append(plainText[letter] + plainText[letter + 1])
        
        status = 1
        for bigram in bigrams:
            if bigram in unrealBigrams:
                status = 0
        if status:
            print(collections.Counter(plainText).most_common(6))
            mostFrequentLetters = collections.Counter(plainText).most_common(6)
            mostFrequentLetters = [mostFrequentLetters[0][0], mostFrequentLetters[1][0], mostFrequentLetters[2][0], mostFrequentLetters[3][0], mostFrequentLetters[4][0], mostFrequentLetters[5][0]]
            if(all(letter in mostFrequentLetters for letter in frequentTerroristLetter)):
                keyVariants.append(key)
        
    print(keyVariants)
    print(decode(keyVariants[0][0], keyVariants[0][1], clearString))

possibleKeys = find_possible_keys(bigrams_comparison(find_frequent_bigrams(clearString)))
correct_keys(possibleKeys, clearString)

