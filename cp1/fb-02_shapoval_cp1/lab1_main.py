from lab1_funcs import *


fname1 = "mein_kampf_with_spaces.txt"
fname2 = "mein_kampf_no_spaces.txt"

text1 = ''
text2 = ''

letters1: dict[str, int] = dict()
letters2: dict[str, int] = dict()

bgs1: dict[str, int] = dict()
bgs2: dict[str, int] = dict()

text1 = read_file_to_str(fname1)
text2 = read_file_to_str(fname2)

letters1 = sort_dict(count_ngrs(text1, 1))
letters2 = sort_dict(count_ngrs(text2, 1))

bgs1 = sort_dict(count_ngrs(text1, 2))
bgs2 = sort_dict(count_ngrs(text2, 2))

P_l1 = calc_P(letters1)
P_l2 = calc_P(letters2)

P_ngs1 = calc_P(bgs1)
P_ngs2 = calc_P(bgs2)



print(f"\nletters - with spaces")
print_ngr_info(letters1, P_l1)
print(f"--  H1 = {calc_H(1, [i for i in P_l1.values()])}")

print(f"\nletters - without spaces")
print_ngr_info(letters2, P_l2)
print(f"--  H1 = {calc_H(1, [i for i in P_l2.values()])}")

print(f"\nbgs - with spaces")
print_ngr_info(bgs1, P_ngs1)
print(f"--  H2 = {calc_H(2, [i for i in P_ngs1.values()])}")

print(f"\nbgs - without spaces")
print_ngr_info(bgs2, P_ngs2)
print(f"--  H2 = {calc_H(2, [i for i in P_ngs2.values()])}")

