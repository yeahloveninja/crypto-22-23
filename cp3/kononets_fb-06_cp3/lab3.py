alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'


def open_file(path_to_file):        # відкриваємо файл, читаємо текст
    with open(path_to_file, 'r', encoding='utf-8') as f:
        text_txt = f.read()
    my_text_enc = ''.join(i for i in text_txt if i in alphabet)
    return my_text_enc


def extended_euclid(a, n):      # пошук оберненого за розширеним алгоритмом Евкліда
    result = [0, 1]
    while a != 0 and n != 0:
        if a > n:
            result.append(a // n)
            a = a % n
        elif n > a:
            result.append(n // a)
            n = n % a
        else:
            print("Оберненого не існує :(")
    for i in range(2, len(result)-1):
        result[i] = result[i - 2] + (-result[i]) * result[i - 1]
    return result[-2]

