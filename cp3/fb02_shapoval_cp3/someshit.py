from funcs import *

fname_ct = "CT.txt"
ct = read_file_to_str(fname=fname_ct)


# sort forbidden, least and most common bgrs
mk = read_file_to_str("mein_kampf_no_spaces.txt")
mk_bgrs = count_ngrs_crs(mk, 2)
forbidden_bgrs = []
lc_bgrs = []
mc_bgrs = []
for bgr in list(sort_dict(mk_bgrs).keys()):
    print(f"'{bgr}': {mk_bgrs[bgr]}, {mk_bgrs[bgr]/len(mk):f}")
    if(mk_bgrs[bgr] == 0):
        forbidden_bgrs.append(bgr)
    elif(mk_bgrs[bgr] <= 24):
        lc_bgrs.append(bgr)
    elif(mk_bgrs[bgr] >= 10000):
        mc_bgrs.append(bgr)
print(forbidden_bgrs)
print(lc_bgrs)
print(mc_bgrs)

