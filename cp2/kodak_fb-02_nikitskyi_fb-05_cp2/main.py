#!/usr/bin/env python3
from prettytable import PrettyTable
from pprint import pprint

from cipher import VigenereCipher
from ops import make_key_dict, plot, Ops


ALPH = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
TEXT_FILE = "text_clean.txt"
CIPHERTEXT_FILE = "ciphertext.txt"
DECRYPTED_CIPHERTEXT_FILE = "decrypted_ciphertext.txt"


def task1_2():
    # encrypt text with different key-length
    cipher_dict = {}
    with open(TEXT_FILE, "r") as f:
        text = f.read().strip()
        for k in list(make_key_dict(text).values()):
            cipher_dict[k] = VigenereCipher(text, k, ALPH).encrypt()

    # table output
    x = PrettyTable()
    x.field_names = ["Key Length", "Key", "Index"]
    x.add_row(["-", "-", Ops(text, ALPH).index()])  # index of clean text 
    
    # compute index for each ciphertext
    for k, v in cipher_dict.items():
        x.add_row([len(k), k, Ops(v, ALPH).index()])
        cipher_dict[k] = Ops(v, ALPH).index()
    
    # count index for default text (last column and "0" x value on the chart)
    cipher_dict[""] = Ops(text, ALPH).index()
    print(x)

    # build plot
    plot(list(map(lambda _: len(_), cipher_dict.keys())), cipher_dict.values())


def task3():
    # Get cipher key length, build plot, get variants of cipher key
    cipher_dict: dict[int, str] = {}
    result_dict: dict[int, float] = {}
    with open(CIPHERTEXT_FILE) as f:
        ciphertext = f.read().replace("\n", "").replace(" ", "")

    key_l = list(range(2, 32))
    for k in key_l:
        cipher_dict[k] = "".join(ciphertext[::k])       # r: text with each "r" el

    for k, v in cipher_dict.items():
        result_dict[k] = Ops(v, ALPH).index()       # r: frequency 
    
    # build plot and check key length
    plot(result_dict.keys(), result_dict.values())  # -> key length: 14
    key_len = int(input("Input key length based on plot: "))

    # get possible variants of cipher key
    print(Ops(ciphertext, ALPH).guess_key(key_len, depth=2))


def d():
    """Decrypt text using guessed key"""
    with open(CIPHERTEXT_FILE, "r") as f:
        ciphertext = f.read().replace("\n", "")

    with open(DECRYPTED_CIPHERTEXT_FILE, "w") as f:
        f.write(VigenereCipher(ciphertext, "экомаятникфуко", ALPH).decrypt())


if __name__ == "__main__":
    task1_2()
    task3()
    d()
