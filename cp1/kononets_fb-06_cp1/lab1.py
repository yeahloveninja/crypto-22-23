alphabet_with_gap = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def without_punctuation(string, value):             # прибираємо усі зайві знаки
    text_punctuation = ""
    if value == 1:
        text_punctuation = alphabet_with_gap
    elif value == 0:
        text_punctuation = alphabet
    for p in string:
        if p not in text_punctuation:
            # банальна заміна символа у строчці
            string = string.replace(p, '')
    return string


def stripped_lines(text, value):                   # робимо єдиний текст якщо текст починається з нової строчки
    with open(text, "r", encoding="utf-8") as file:
        newline_breaks = ""
        for line in file:
            if value == 1:                         # ставимо пробіл?
                stripped_line = line.strip() + " "
            elif value == 0:                        # не ставимо пробіл?
                stripped_line = line.strip()
            newline_breaks += stripped_line.lower()
        return newline_breaks