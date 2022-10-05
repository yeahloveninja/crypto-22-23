import io
import re
import math
import xlsxwriter

def dict_count(alp, text): #Count symbols and sort dict
    symbols_dict = {}
    for symbol in alp:
        symbols_dict[symbol] = text.count(str(symbol)) # рахуємо кількість символів в тексті
    sorted_symbols_dict = sorted(symbols_dict.items(), key=lambda x: x[1], reverse=True)
    # сортуємо значення елементів словаря за спаданням, на виході отримуємо двовимірний список
    print("[+]Найчастіші 10 елементів: ", sorted_symbols_dict[0:10])
    return sorted_symbols_dict

def bigramStep(text, step): #Set bigram step and count quantity
    bigrams = []
    for j in range(0, len(text) - step, step):
        bigrams.append(text[j] + text[j + 1])
    bigrams = list(set(bigrams))
    bigram_freq = dict_count(bigrams, text)
    return bigram_freq

def frequencyCount_nWrite(filename, column1, column2, sortedSymb, text): #Count frequency and write to .xlsx file
    all_symbols_count = len(text)
    workbook = xlsxwriter.Workbook(filename+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', column1)
    worksheet.write('B1', column2)
    freqList = []
    i = 2
    for a in sortedSymb:
        symbol_frequency = int(a[1])/all_symbols_count
        freqList.append(symbol_frequency)
        worksheet.write('A'+str(i), "'" + str(a[0]) + "'")
        worksheet.write('B'+str(i), symbol_frequency)
        i+=1
    workbook.close()
    return freqList

def H(freqs, divider): #Count Entropy
    h = []
    for freq in freqs:
        if freq != 0:
            h.append(-freq*math.log(freq, 2))
        else:
            h.append(freq)
    H = sum(h)/divider
    return H

def R(H, alph): #Count Surplus
    R = 1 - (H/math.log2(len(alph)))
    return R

def main():
    with io.open("komediya.txt", encoding='utf-8') as file:
        komediya = file.read()
    komediya = re.sub("[^А-Яа-я ]", "", komediya)   # видаляємо всі символи крім зазначених
    komediya = re.sub(" +", " ", komediya)          # виадаляємо повторні пробіли
    komediya2 = re.sub(" +", "", komediya)          # виадаляємо всі пробіли
    komediya = komediya.lower()                     # переводимо всі символи в нижній регістр
    komediya2 = komediya2.lower()

    f = open('komediya_clear.txt', 'w')
    f.write(komediya)
    f.close()
    f = open('komediya_clearw_Space.txt', 'w')
    f.write(komediya2)
    f.close()

    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "
    alphabet2 = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    H1wSpace = H(frequencyCount_nWrite('symbolsFreqwSpace','Symbol','Frequency',dict_count(alphabet, komediya),komediya),1) #H1 with SPACES
    H1w_oSpace = H(frequencyCount_nWrite('symbolsFreqw_oSpace','Symbol','Frequency',dict_count(alphabet2, komediya2),komediya2),1) #H1 with NO SPACES
    H2wSpaceStep1 = H(frequencyCount_nWrite('bigramsStep1FreqwSpace','Bigram','Frequency',bigramStep(komediya, 1),komediya),2) #H2 Step=1 with SPACES
    H2w_oSpaceStep1 = H(frequencyCount_nWrite('bigramsStep1Freqw_oSpace','Bigram','Frequency',bigramStep(komediya2, 1),komediya2),2) #H2 Step=1 with NO SPACES
    H2wSpaceStep2 = H(frequencyCount_nWrite('bigramsStep2FreqwSpace','Bigram','Frequency',bigramStep(komediya, 2),komediya),2) #H2 Step=2 with SPACES
    H2w_oSpaceStep2 = H(frequencyCount_nWrite('bigramsStep2Freqw_oSpace','Bigram','Frequency',bigramStep(komediya2, 2),komediya2),2) #H2 Step=2 with NO SPACES

    R_H1wSpace = R(H1wSpace, alphabet)
    R_H1w_oSpace = R(H1w_oSpace, alphabet2)
    R_H2wSpaceStep1 = R(H2wSpaceStep1, alphabet)
    R_H2w_oSpaceStep1 = R(H2w_oSpaceStep1, alphabet2)
    R_H2wSpaceStep2 = R(H2wSpaceStep2, alphabet)
    R_H2w_oSpaceStep2 = R(H2w_oSpaceStep2, alphabet2)

    xlsxFile = xlsxwriter.Workbook('EntropyAndSurplus.xlsx')
    worksheetHR = xlsxFile.add_worksheet()
    worksheetHR.write('A1', 'Name')
    worksheetHR.write('B1', 'H')
    worksheetHR.write('C1', 'R')
    worksheetHR.write('A2', 'Letters with spaces')
    worksheetHR.write('B2', H1wSpace)
    worksheetHR.write('C2', R_H1wSpace)
    worksheetHR.write('A3', 'Letters with out spaces')
    worksheetHR.write('B3', H1w_oSpace)
    worksheetHR.write('C3', R_H1w_oSpace)
    worksheetHR.write('A4', 'Bigrams with spaces and step 1')
    worksheetHR.write('B4', H2wSpaceStep1)
    worksheetHR.write('C4', R_H2wSpaceStep1)
    worksheetHR.write('A5', 'Bigrams with out spaces and step 1')
    worksheetHR.write('B5', H2w_oSpaceStep1)
    worksheetHR.write('C5', R_H2w_oSpaceStep1)
    worksheetHR.write('A6', 'Bigrams with spaces and step 2')
    worksheetHR.write('B6', H2wSpaceStep2)
    worksheetHR.write('C6', R_H2wSpaceStep2)
    worksheetHR.write('A7', 'Bigrams with out spaces and step 2')
    worksheetHR.write('B7', H2w_oSpaceStep2)
    worksheetHR.write('C7', R_H2w_oSpaceStep2)
    xlsxFile.close()

main()