import re #операції з регулярними виразами

def change_sym(file_name, space = True):
    with open(file_name, encoding="utf8") as f:
        text = f.read()
        f.close()
        
    newtext = text.lower()
    #print(newtext)
    if (space == True):
        readytext = re.sub(r'[^абвгдеёжзийклмнопрстуфхцчшщъыьэюя ]', '', newtext)
    else:
        readytext = re.sub(r'[^абвгдеёжзийклмнопрстуфхцчшщъыьэюя]', '', newtext)
    #print(readytext)

    write_to_file = open('text_after.txt', 'w')
    write_to_file.write(readytext)
    write_to_file.close()

if __name__ == '__main__':
    change_sym('initial_text.txt', False)