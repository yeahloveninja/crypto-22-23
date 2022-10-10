from funcs import *

#=====================================    task 1, 2    =====================================

ot_fname: str = "mein_kampf.txt"

key: str = "уйдиизмоейдиректории"
key_lens: list[int] = [2, 3, 5, 10, 15, 20]

with (open(ot_fname, mode='r', encoding="utf8") as f_in):
    ot = f_in.read()
    print(f"open text, I = {round(calc_I(count_in_block(ot, 0, 1)), 4)}")

for l in key_lens:
    with (open(f"ct_len_{l}.txt", mode='w+', encoding="utf8") as f_out):
        f_out.write(encrypt_V(ot, key[:l]))

for l in key_lens:
    with (open(f"ct_len_{l}.txt", mode='r', encoding="utf8") as f):
        ct = f.read()
        print(f"key_len = {l}, I = {round(calc_I(count_in_block(ct, 0, 1)), 4)}")

