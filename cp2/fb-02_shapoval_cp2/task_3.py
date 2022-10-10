from funcs import *


# =======================================    task 3    ======================================

ct_fname: str = "CText.txt"


with (open(ct_fname, mode='r', encoding="utf8") as f_in):
    ct = f_in.read()


# fing key len with best I
#print(sort_dict(alg_1(ct, 30, 0.035, 0.06)))

# most common letters in CT
#most_common_ct_letters = top_letter_in_each_block(ct, 20)
#for l in most_common_ct_letters:
#    print(f"{l[0]}: {l[1]}")

key = find_key(ct, 20)
print(key)

with (open(f"OText.txt", mode='w+', encoding="utf8") as f_out):
    f_out.write(decrypt_V(ct, key))