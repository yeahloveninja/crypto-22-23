alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'


def open_file(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as f:
        text_txt = f.read()
    my_text_enc = ''.join(i for i in text_txt if i in alphabet)
    return my_text_enc


