import math

def calc_H(n:int, P: list[float]):
    if (str(n).isdigit() == False):
        return None
    if (n < 1):
        return None
    
    sum = 0
    for p in P:
        sum += p * math.log2(p)
    return round(-sum/n, 4)


def count_ngrs(text:str, n: int = 1):
    ngrs: dict[str, int] = dict()
    for i in range(len(text)-n+1):
        ngr = text[i:i+n]
        if (ngr in ngrs.keys()):
            ngrs[ngr] += 1
        else:
            ngrs[ngr] = 1
    return ngrs


# in python 3.7+ dict order is preserved
def sort_dict(bgs: dict[str, int], dsc: bool = True):
    return dict(sorted(bgs.items(), key = lambda i: int(i[1]), reverse=dsc))


# some sh1tcode
def print_ngr_info(d: dict[str, int], P: dict[str, int] = None, n: int = 10):
    ngrs = list(d.keys())[0:n]
    if (P != None):
        if (list(d.keys()) != list(P.keys())):
            print("different ngrs")
        else:
            for g in ngrs:
                print(f"'{g}'  {P[g]}  {d[g]}")
    else:
        for g in ngrs:
            print(f"'{g}'  {d[g]}")


def read_file_to_str(fname: str):
    text = ''
    with (open(fname, 'r', encoding="utf8") as f):
        text = f.read()
    return text


# calculate P for each n-gr. Input: {n-gr: amount_in_text, ...}
def calc_P(ngrs: dict[str, int]):
    P: dict[str, float] = dict()
    sum: int = 0
    for k in ngrs.keys():
        sum += ngrs[k]
    for k in ngrs.keys():
        P[k] = round(ngrs[k]/sum, 10)
    return P