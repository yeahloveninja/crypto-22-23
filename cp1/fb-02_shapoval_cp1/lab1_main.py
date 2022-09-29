from lab1_funcs import *

fname1 = "mein_kampf_with_spaces.txt"
fname2 = "mein_kampf_no_spaces.txt"

text1: str = read_file_to_str(fname1)
text2: str = read_file_to_str(fname2)


letters1: dict[str, int] = sort_dict(count_ngrs_cross(text1, 1))
letters2: dict[str, int] = sort_dict(count_ngrs_cross(text2, 1))

bgrs1_crs: dict[str, int] = sort_dict(count_ngrs_cross(text1, 2))
bgrs2_crs: dict[str, int] = sort_dict(count_ngrs_cross(text2, 2))

bgrs1_seq: dict[str, int] = sort_dict(count_ngrs_seq(text1, 2))
bgrs2_seq: dict[str, int] = sort_dict(count_ngrs_seq(text2, 2))


P_l1: dict[str, float] = calc_P(letters1)
P_l2: dict[str, float] = calc_P(letters2)

P_ngs1_crs: dict[str, float] = calc_P(bgrs1_crs)
P_ngs2_crs: dict[str, float] = calc_P(bgrs2_crs)

P_ngs1_seq: dict[str, float] = calc_P(bgrs1_seq)
P_ngs2_seq: dict[str, float] = calc_P(bgrs2_seq)


print(f"\nletters - with ' '")
print_ngr_info(letters1, P_l1)
print(f"--  H1 = {calc_H(1, [i for i in P_l1.values()])}")

print(f"\nletters - without ' '")
print_ngr_info(letters2, P_l2)
print(f"--  H1 = {calc_H(1, [i for i in P_l2.values()])}")

print(f"\nbgs, crs - with ' '")
print_ngr_info(bgrs1_crs, P_ngs1_crs)
print(f"--  H2 = {calc_H(2, [i for i in P_ngs1_crs.values()])}")

print(f"\nbgs, crs - without ' '")
print_ngr_info(bgrs2_crs, P_ngs2_crs)
print(f"--  H2 = {calc_H(2, [i for i in P_ngs2_crs.values()])}")

print(f"\nbgs, seq - with ' '")
print_ngr_info(bgrs1_seq, P_ngs1_seq)
print(f"--  H2 = {calc_H(2, [i for i in P_ngs1_seq.values()])}")

print(f"\nbgs, seq - without ' '")
print_ngr_info(bgrs2_seq, P_ngs2_seq)
print(f"--  H2 = {calc_H(2, [i for i in P_ngs2_seq.values()])}")

