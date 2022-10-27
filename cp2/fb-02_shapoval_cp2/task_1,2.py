from funcs import *
import matplotlib.pyplot as plt
import numpy as np

#=====================================    task 1, 2    =====================================

ot_fname: str = "mein_kampf.txt"

key: str = "уйдиизмоейдиректории"
key_lens: list[int] = [2, 3, 5, 10, 15, 20]

with (open(ot_fname, mode='r', encoding="utf8") as f_in):
    ot = f_in.read()
    ot_I = round(calc_I(count_in_block(ot, 0, 1)), 4)
    print(f"open text, I = {ot_I}")

for l in key_lens:
    with (open(f"ct_len_{l}.txt", mode='w+', encoding="utf8") as f_out):
        f_out.write(encrypt_V(ot, key[:l]))

ct_I = list()
for l in key_lens:
    with (open(f"ct_len_{l}.txt", mode='r', encoding="utf8") as f):
        ct = f.read()
        ct_I.append(round(calc_I(count_in_block(ct, 0, 1)), 4))

for i in ct_I:
    print(f"key_len = {l}, I = {i}")


#   I plot
plt.plot([0] + key_lens, [ot_I] + ct_I)
plt.xlabel("key len")
plt.ylabel("I")
plt.ylim(0.03, 0.06)
plt.xticks(list(range(0, 21, 1)))
plt.show()