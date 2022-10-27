import imp


import collections

alp: str = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
alp_len: int = len(alp)
alp_dict: dict[str, int] = {alp[i]: i for i in range(len(alp))}

most_common = {'о': 0.1097, 'е': 0.0845, 'а': 0.0801, 'и': 0.0735, 'н': 0.0670, 'т': 0.0626, 'с': 0.0547, 'р': 0.0473, 'в': 0.0454, 'л': 0.0440}


def str_to_int(s: str) -> list[int]:
    return [alp_dict[i] for i in s]


def key_by_ot_and_ct_letter(ot_l: str, ct_l: str):
    return alp[(alp_dict[ct_l] - alp_dict[ot_l]) % alp_len]


# in python 3.7+ dict order is preserved
def sort_dict(d: dict[str, float], dsc: bool = True):
    return dict(sorted(d.items(), key=lambda i: float(i[1]), reverse=dsc))


def encrypt_V(ot: str, key: str) -> str:
    key_len = len(key)
    ot_ords = str_to_int(ot)
    key_ords = str_to_int(key)
    ct: str = ''
    for i in range(len(ot_ords)):
        ct += alp[(ot_ords[i] + key_ords[i % key_len]) % alp_len]
    return ct


def decrypt_V(ct: str, key: str) -> str:
    key_len = len(key)
    ct_ords = str_to_int(ct)
    key_ords = str_to_int(key)
    ot: str = ''
    for i in range(len(ct_ords)):
        ot += alp[(ct_ords[i] - key_ords[i % key_len] + alp_len) % alp_len]
    return ot


def count_in_block(s: str, offset: int, r: int) -> dict[str, int]:
    freq: dict[str, int] = {a: 0 for a in alp}
    for i in s[offset::r]:
        freq[i] += 1
    return sort_dict(freq)


def count_in_each_block(s: str, r: int) -> list[dict[str, int]]:
    res = list()
    for offset in range(r):
        res.append(count_in_block(s, offset, r))
    return res


def calc_I(freq: dict[str, int]):
    n = 0
    res = 0
    for k in freq.keys():
        n += freq[k]
        res += freq[k]*(freq[k]-1)
    res /= n*(n-1)
    return res


def calc_I_for_r(s: str, r: int, ndigits: float = 4):
    a = 0
    blocks = count_in_each_block(s, r)
    for block in blocks:
        a += calc_I(block)
    return round(a/r, ndigits)


def find_r_alg_1(s: str, max_key_len: int, Imin=0.01, Imax=0.1):
    if (max_key_len*2 > len(s)):
        max_key_len = int(len(s)/2)

    key_I: dict[int, float] = dict()

    # try keys
    for r in range(2, max_key_len+1):
        cur_I = calc_I_for_r(s, r)
        if (cur_I >= Imin and cur_I <= Imax):
            key_I[r] = cur_I
    return key_I


def top_letter_in_each_block(text: str, r: int) -> list[list[str, int, int]]:
    res = list()
    tmp_str = ''
    mc = None
    for offset in range(r):
        tmp_str = text[offset::r]
        mc = collections.Counter(tmp_str).most_common(1)[0]
        res.append([mc[0], round(mc[1]/len(tmp_str), 4)])
    return res


def gen_possible_keys(options: list[list[str]], cur_pos, last_pos):
    if (cur_pos == last_pos):
        for o in options[cur_pos]:
            yield o
    else:
        for o in options[cur_pos]:
            for n in gen_possible_keys(options, cur_pos+1, last_pos):
                yield o + n


def guess_key(ct: str, r: int):
    most_common_list = [k for k in most_common.keys()]
    key = ''
    mc_ct_letters = [l[0] for l in top_letter_in_each_block(ct, r)]
    # key letters
    for i in range(r):
        # try most common real life letters
        for mc_ot in most_common_list:
            kl = key_by_ot_and_ct_letter(mc_ot, mc_ct_letters[i])
            ot_block = decrypt_V(ct[i::r], kl)
            ok = 0
            for l in list(count_in_block(ot_block, 0, 1).keys())[0:10]:
                if (l in most_common_list):
                    ok += 1
            if(ok >= 7):
                key += kl
                break
    return key


