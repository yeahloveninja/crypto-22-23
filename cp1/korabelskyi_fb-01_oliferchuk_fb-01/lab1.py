import io
from logging.handlers import RotatingFileHandler
from math import log


file=io.open("file.txt", mode="r", encoding="utf-8")
file1=io.open("file1.txt", mode="r", encoding="utf-8")

#текст з пробілами
text0 = file.read()

#текст без пробілів
text1= file1.read()

AlphabetWithSpaces = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ь','ю','я',' ']
AlphabetWithoutSpaces = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ь','ю','я']

BigramCrossWithSpaces = [text0[i:i+2] for i in range(len(text0))] #перехресна біграма з пробілами
BigramCrossWithoutSpaces = [text1[i:i+2] for i in range(len(text1))] #перехресна біграма без пробілів
NoCrossBigramWithSpaces = [text0[i:i+2] for i in range(0,len(text0),2)] #не перехресна біграма з пробілами
NoCrossBigramWithoutSpaces = [text1[i:i+2] for i in range(0,len(text1),2)] #не перехресна біграма без пробілів

def letters(alphabet, text):
    len_text = len(text)
    #створюємо словник
    
    dictionary = {}

    #заповнення словника парою ключ - значення, де ключ - буква, значення - частота
    for i in range(len(alphabet)):
        dictionary[alphabet[i]]=text.count(alphabet[i])/len_text

    #новий словник, у якому відсортовані значення

    new_dictionary = {}
    new_values = sorted(dictionary.values(), reverse=True)

    for i in new_values:
        for k in dictionary.keys():
            if dictionary[k]==i:
                new_dictionary[k] = dictionary[k]
                break

    print(new_dictionary)

    #підрахунок ентропії Н1 беспосередньо за значенням
    h1 = 0
    for i in range(len(alphabet)):
        h = round(-dictionary.get(alphabet[i])*log(dictionary.get(alphabet[i]),2),3)
        h1 += h

    print("H1 = ", round(h1,4))

def bigram(alphabet, list_of_bigrams):
    length_of_list = len(list_of_bigrams)

    #створюємо матрицю розміров довжини алфавіту + 1
    m = len(alphabet)+1
    matrix = [0] * m
    for i in range(m):
        matrix[i] = [0] * m

    matrix[0][0]="/"

    #присвоюємо першому рядку букви
    for i in range(1, len(matrix[0])):
        matrix[0][i]=alphabet[i-1]

    #присвоюємо першому стовпчику букви
    for i in range(1, len(matrix[0])):
        matrix[i][0]=alphabet[i-1]

    #рахуємо частоту для біграм
    for i in range(1,len(matrix[0])):
        for j in range(1,len(matrix[0])):
            big = matrix[0][i]+matrix[j][0]
            matrix[i][j]= ('{:.4f}'.format(list_of_bigrams.count(big)/length_of_list))

    #виведення матриці
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if(i==0):
                print(matrix[i][j],"     ",end="")
            else: print(matrix[i][j],"",end="")
        print()


    #підраховуємо ентропію Н2 безпосередньо за значенням
    h2 = 0
    for i in range(1, len(matrix[0])):
        for j in range(1, len(matrix[0])):
            if (float(matrix[i][j])!=0):
                h2 = h2+(-float(matrix[i][j])*(log(float(matrix[i][j]),2)))

    h2=round(h2/2,4)
    print("H2=", h2)

letters(AlphabetWithSpaces, text0)
print()
letters(AlphabetWithoutSpaces, text1)
print()
bigram(AlphabetWithSpaces, BigramCrossWithSpaces)
print()
bigram(AlphabetWithSpaces, NoCrossBigramWithSpaces)
print()
bigram(AlphabetWithoutSpaces, BigramCrossWithoutSpaces)
print()
bigram(AlphabetWithoutSpaces, NoCrossBigramWithoutSpaces)