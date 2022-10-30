from queue import PriorityQueue
from funcs import *


fname_ct = "CT.txt"
ct = read_file_to_str(fname=fname_ct)


for a, b in try_keys(ct):
    ot = decrypt(ct, a, b)
    print(ot[:100])




#with (open(f"OText.txt", mode='w+', encoding="utf8") as f_out):
#    f_out.write(ot)

