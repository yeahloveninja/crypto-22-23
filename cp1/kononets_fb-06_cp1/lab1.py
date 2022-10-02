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


def pretty_text(text, value):                       # приводимо текст до потрібного нам за завданням
    if value == 1:          # ставимо пробіл?
        newline_breaks = stripped_lines(text, value)
        newline_breaks = without_punctuation(newline_breaks, value)
        return newline_breaks
    elif value == 0:        # не ставимо пробіл?
        newline_breaks = stripped_lines(text, value)
        newline_breaks = without_punctuation(newline_breaks, value)
        return newline_breaks


def frequency_of_letters(text, my_alphabet):    # рахуємо частоту зустрічаємості літер
    letters_count = {}
    for letter in my_alphabet:
        letters_count[letter] = 0               # для кожного символу(ключа) з алфавіту ставимо значення 0
    for letter in text:
        letters_count[letter] += 1              # скільки разів зустрічається стільки раз і додаємо

    letters_frequency = {}
    for letter in my_alphabet:
        letters_frequency[letter] = round((letters_count[letter])/len(text), 9)  # округлюю до 9 знаків для точності

    return letters_frequency


def bigram_frequency(text, my_alphabet, boolean_value):     # частота зустрічаємості біграм
    bigram_count = {}
    bigram_frequency_is = {}
    for letter_1 in my_alphabet:
        for letter_2 in my_alphabet:
            dict_key = letter_1 + letter_2
            bigram_count[dict_key] = 0

    if boolean_value == 1:          # H1
        i = 0
        while i < len(text) - 1:            # довжина тексту - 1 , для H1
            key = text[i] + text[i+1]       # скріплюю літери біграм
            bigram_count[key] = bigram_count[key] + 1   # підрахунок зустрічаємості кожної біграми
            i = i + 1

        for key in bigram_count.keys():
            bigram_frequency_is[key] = round(bigram_count[key]/(len(text)-1), 9)  # округлюю до 9 знаків для точності

    else:                       # H2
        if len(text) % 2 == 1:  # біграми з кроком 2
            text += "о"
        i = 0
        while i < len(text) - 1:            # усе інше аналогічно до H1
            key = text[i] + text[i+1]
            bigram_count[key] = bigram_count[key] + 1
            i = i + 2                       # окрім цієї частини, бо крок 2

        for key in bigram_count.keys():
            bigram_frequency_is[key] = round(bigram_count[key]/(len(text)/2), 9)
    return bigram_frequency_is