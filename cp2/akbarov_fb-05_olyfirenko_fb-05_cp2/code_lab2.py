from itertools import cycle
def c_i(t):
    index = 0
    length = len(t)
    for i in range(len(al)):
        count_letter = t.count(al[i])
        index += count_letter * (count_letter - 1)
    return index * (1 / (length * (length - 1)))


def e_d(t, key):
    return ''.join(
        map(lambda argument: al[(al.index(argument[0]) + al.index(argument[1]) % 32) % 32], zip(t, cycle(key))))


def d_d(de_coded_text, key):
    return ''.join(map(lambda argument: al[(al.index(argument[0]) - al.index(argument[1]) % 32) % 32],
                       zip(de_coded_text, cycle(key))))


def split_blocks(t, length):
    our_block = []
    for i in range(length):
        our_block.append(t[i::length])
    return our_block


def ind_bl(t, size):
    our_block = split_blocks(t, size)
    index = 0
    for i in range(len(our_block)):
        index += c_i(our_block[i])
    index /= len(our_block)
    return index / len(our_block)


def c_k(t, size, letter):
    our_block = split_blocks(t, size)
    key = ""
    for i in range(len(our_block)):
        frequent = max(our_block[i],
                       key=lambda count_: our_block[i].count(count_))  # выводич что чаще всего используется
        key += al[(al.index(frequent) - al.index(letter)) % len(al)]
    return key

def main():
    with open('text_to_read.txt', 'r', encoding='utf-8') as file1:
        tx1 = file1.read()
    with open('text_to_decode_7.txt', 'r', encoding='utf-8') as file2:
        tx2 = file2.read()
    global al
    al = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    key_list = ['аб', 'ира', 'сома', 'писар', 'рнарпнгоир', 'рнпыогиртны', 'рнйгыяхзгрпм', 'вдзхьзужбъгяш',
                'квххсьпириуктж', 'ннвпосшайфздомн', 'жшпеиезэщфчбщнзй', 'здукящуаубцыхыгхж', 'юпйсимяяшяшзломмзш',
                'щыййгскфвэслнуьрсхщ', 'зцюрйонпхбяжткщсюсцъ']

    print("\nIndex start = ", c_i(tx1), "\n")
    for key in key_list:
        print("Len  = ", len(key))
        encoded_text = e_d(tx1, key)
        print("- Zah текст: ", encoded_text)
        print("- Roh текст: ", d_d(encoded_text, key))
        print("Index совпадения: ", c_i(encoded_text), "\n")

    for i in range(1, len(al)):
        print('Len key=' + str(i) + ' => Index sov=' + str(ind_bl(tx2, i)))

    for letter in 'оеаитнслвр':
        print(c_k(tx2, 15, letter))

    print("\n")
    decoded_text = d_d(tx2, 'арудазевархимаг')  # арудазевархимаг
    print("Code text: ", tx2)
    print("Encode text: ", decoded_text)
    with open(f'vid_7.txt', 'w', encoding='UTF-8') as f:
        f.write(decoded_text)

if __name__ == '__main__':
    main()