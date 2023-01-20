import re
import math
import pandas as pd
import numpy as np


def entro(dic, n):  # расчет энтропии
    entropies = []
    for k in dic.keys():  # проходим все элементы словаря
        if dic[k] != 0:
            entropies.append(abs(float(dic[k]) * math.log2(dic[k]) / n))
    return sum(entropies)  # возвращаем


def fre_of_letters(txt, alf_a):  # розрахунок частоти кожного символу
    dic = {}
    for l in alf_a:
        dic.update({l: 0})
    for i in txt:  # скільки разів кожен символ зустрічається у тексті
        dic[i] += 1
    for l in alf_a:
        dic.update({l: round(dic[l] / len(txt), 5)})  # расчет частоты
    return dic


def rozr_nadl(e, all_t):  # розрахунок надлишковості
    ans = 1 - (e / math.log2(all_t))
    return ans


def fob(txt, alf_a, cross=True):  # для розрахунка частот біграм
    dic = {}
    for l1 in alf_a:
        for l2 in alf_a:
            dic.update({l1 + l2: 0})
    if cross == True:  # для розрахунку H2 перехресної
        for i in range(len(txt) - 1):
            dic[txt[i] + txt[i + 1]] += 1  # зчитуємо
        for key in dic.keys():
            dic[key] = round(dic[key] / (len(txt) - 1), 5)  # визначаємо
    else:  # для розрахунку H2
        if len(txt) % 2 == 1:
            txt += "а"  # щоб кожній літері була пара
        i = 0
        for i in range(len(txt) - 1):
            if i % 2 == 1:
                continue
            dic[txt[i] + txt[i + 1]] += 1  # рахуємо частоту в тексті
        for key in dic.keys():
            dic[key] = round(dic[key] / (len(txt) / 2), 5)  # рахуємо ентропію в тексті
    return dic


if __name__ == '__main__':
    alf_a = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'  # визначили алфавіт
    alf_a_with_prob = alf_a + ' '  # визначили алфавіт + пробіл

    ###########################################
    file = open('TEXT_spaces.txt', encoding='utf8')  # зчитуємо текст
    text = file.read().lower().replace('\n', '')  # считываем и убираем все остальное и делаем маленькими буквами
    text = re.sub(r'[^а-яё ]', '', text)
    file.close()

    ###########################################
    print(f'===Обрахунки для тексту з пробілами===')
    ###########################################
    f1 = fre_of_letters(text, alf_a_with_prob)
    # print(f'Частота букв - {f1}')
    e_f1 = entro(f1, 1)
    print(f'H1={e_f1}')
    print(f'Надлишковість = {rozr_nadl(e_f1, len(alf_a_with_prob))}')

    f11 = fob(text, alf_a_with_prob, cross=False)
    # print(f'Частота біграм - {f11}')
    e_f11 = entro(f11, 2)
    print(f'H2={e_f11}')
    print(f'Надлишковість = {rozr_nadl(e_f11, len(alf_a_with_prob))}')

    f12 = fob(text, alf_a_with_prob, cross=True)
    # print(f'Частота перехресних біграм - {f11}')
    ef12 = entro(f12, 2)
    print(f'H2(перехресна) = {ef12}')
    print(f'Надлишковість = {rozr_nadl(ef12, len(alf_a_with_prob))}')
    ###########################################
    print(f'===Обрахунки для тексту без пробілів===')
    ###########################################
    file = open('TEXT_spaces.txt', encoding='utf8')  # зчитуємо з файлу
    text = file.read().lower().replace('\n', '')  # зчитуємо й прибираємо все інше і робимо маленькими літерами
    text = re.sub(r'[^а-яё ]', '', text)
    text = text.replace(' ', '')
    file.close()
    ###########################################
    f2 = fre_of_letters(text, alf_a)
    # print(f'Частота букв - {f2}')
    e_f2 = entro(f2, 1)
    print(f'H1={e_f2}')
    print(f'Надлишковість = {rozr_nadl(e_f2, len(alf_a))}')

    f21 = fob(text, alf_a, cross=False)
    # print(f'Частота біграм - {f21}')
    e_f21 = entro(f21, 2)
    print(f'H2={e_f21}')
    print(f'Надлишковість = {rozr_nadl(e_f21, len(alf_a))}')
    f22 = fob(text, alf_a, cross=True)
    # print(f'Частота перехресних біграм - {f21}')
    ef22 = entro(f22, 2)
    print(f'H2(перехресна) = {ef22}')
    print(f'Надлишковість = {rozr_nadl(ef22, len(alf_a))}')

    a1 = pd.DataFrame(f1.values(), index=f1.keys())  # создаем датафрейм, чтобы потом занести в файл
    # print(a1)
    a1.to_excel('H1_z_prob.xlsx')  # заносим в файл (частот)

    vva = np.array(list(f11.values()))
    a11 = pd.DataFrame(vva.reshape((34, 34)), index=f1.keys(),
                       columns=f1.keys())  # создаем датафрейм, чтобы потом занести в файл
    # print(a11)
    a11.to_excel('H2_z_prob.xlsx')  # заносим в файл (Н1)

    vva = np.array(list(f12.values()))
    a12 = pd.DataFrame(vva.reshape((34, 34)), index=f1.keys(),
                       columns=f1.keys())  # создаем датафрем, чтобы потом занести в файл
    # print(a12)
    a12.to_excel('H2_z_prob_cross.xlsx')  # заносим в файл

    #################
    a2 = pd.DataFrame(f2.values(), index=f2.keys())  # создаем датафрем, чтобы потом занести в файл
    # print(a2)

    a2.to_excel('H1_bez_prob.xlsx')  # заносим в файл
    vva = np.array(list(f21.values()))
    a21 = pd.DataFrame(vva.reshape((33, 33)), index=f2.keys(),
                       columns=f2.keys())  # создаем датафрем, чтобы потом занести в файл
    # print(a21)
    a21.to_excel('H2_bez_prob.xlsx')  # заносим в файл
    vva = np.array(list(f22.values()))
    a22 = pd.DataFrame(vva.reshape((33, 33)), index=f2.keys(),
                       columns=f2.keys())  # создаем датафрем, чтобы потом занести в файл
    # print(a22)
    a22.to_excel('H2_bez_prob_cross.xlsx')  # заносим в файл
