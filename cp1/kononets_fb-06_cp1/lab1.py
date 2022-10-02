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
