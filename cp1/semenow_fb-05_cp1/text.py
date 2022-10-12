txt = open('Havelok_Renegat.txt', 'r', encoding='utf=8').read()


def create_txt(text):
    text_one = text.lower().replace(' ', '_').replace('\n', '_').strip()
    text_write = ''
    for i in text_one:
        if i.isalpha():
            text_write += i
        elif i == '_':
            text_write += '_'
    with open("2.txt", 'w') as file:
        file.write(text_write)
    text_write = text_write.replace('_', '')
    with open("3.txt", 'w') as file:
        file.write(text_write)
    return text_write


create_txt(txt)
