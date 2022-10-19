from funcs import *
import matplotlib.pyplot as plt


# =======================================    task 3    ======================================

ct_fname: str = "CText.txt"


with (open(ct_fname, mode='r', encoding="utf8") as f_in):
    ct = f_in.read()


# fing key len with best I
key_len_I = find_r_alg_1(ct, 30, 0.0, 0.06)
plt.bar(list(key_len_I.keys()), list(key_len_I.values()))
plt.xticks(list(range(2, 31)))
plt.ylim(0.03, 0.06)
plt.show()

print(sort_dict(key_len_I))



# most common letters in CT
most_common_ct_letters = top_letter_in_each_block(ct, 20)
for l in most_common_ct_letters:
    print(f"{l[0]}: {l[1]}")

key = guess_key(ct, 20)
print(key)

with (open(f"OText.txt", mode='w+', encoding="utf8") as f_out):
    f_out.write(decrypt_V(ct, key))


