from funcs import *

fname_ct = "CT.txt"
ct = read_file_to_str(fname=fname_ct)

ngrs_crs = sort_dict(count_ngrs_seq(ct))

print("====    seq ngr count    ====")
print_ngr_info(ngrs_crs, 5)





