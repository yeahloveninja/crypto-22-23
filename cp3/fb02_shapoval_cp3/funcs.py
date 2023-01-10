from funcs_math import *

alp: str = "абвгдежзийклмнопрстуфхцчшщьыэюя"
alp_len: int = len(alp)
alp_ords: dict[str, int] = {alp[i]: i for i in range(alp_len)}



# Disclaimer: It is better to have freqs for each bgr, but common min freq also seems to be OK

# >= 0.007388 in mein kampf (>= 10k)
mc_bgrs: list[str] = ['ст', 'но', 'ен', 'то', 'на', 'ни', 'ос', 'ов', 'ро', 'пр', 'ра', 'ко', 'во', 'по', 'не', 'ре', 'ес', 'ан', 'го', 'ти', 'от', 'ть', 'ит', 'ер', 'од', 'ли']
# <= 0.000010 in mein kampf ( <= 24 pcs )
lc_bgrs: list[str] = ['бж', 'жп', 'жс', 'фы', 'эс', 'гт', 'нж', 'нш', 'бш', 'жч', 'пв', 'тш', 'жр', 'нх', 'рф', 'чо', 'гш', 'цл', 'пб', 'пч', 'фг', 'цм', 'вю', 'нл', 'шм', 'ьщ', 'юш', 'гэ', 'жв', 'кш', 'юх', 'бз', 'жг', 'лф', 'шп', 'шс', 'гз', 'цг', 'цз', 'шб', 'лх', 'лш', 'рщ', 'цт', 'цэ', 'эр', 'бб', 'жт', 'мю', 'шр', 'гг', 'зю', 'кх', 'пд', 'чд', 'эш', 'бп', 'бт', 'дф', 'дю', 'зф', 'зх', 'пф', 'тю', 'ыщ', 'жм', 'жэ', 'кя', 'фю', 'цр', 'шю', 'цч', 'чп', 'чс', 'бг', 'бч', 'гц', 'жж', 'пм', 'фь', 'хю', 'чм', 'эв', 'йю', 'пг', 'пэ', 'фв', 'фм', 'фн', 'шд', 'жз', 'йщ', 'лц', 'лщ', 'мщ', 'пш', 'цх', 'цц', 'цш', 'эд', 'бф', 'кь', 'кю', 'фд', 'фп', 'фч', 'фэ', 'хь', 'цф', 'чб', 'чч', 'чэ', 'шг', 'шф', 'шц', 'шэ', 'эб', 'эз', 'эх', 'бц', 'гж', 'гф', 'гя', 'жл', 'жц', 'кы', 'пж', 'пз', 'сй', 'фб', 'фк', 'фх', 'цж', 'ця', 'чг', 'чз', 'чф', 'шз', 'шх', 'щк', 'щп', 'ыю', 'эй', 'эу', 'юй']
# 0 occurrences in mein kampf
forbidden_bgrs: list[str] = ['аы', 'аь', 'бй', 'вй', 'гй', 'гх', 'гщ', 'гы', 'гь', 'гю', 'дй', 'дщ', 'еы', 'еь', 'жй', 'жф', 'жх', 'жш', 'жщ', 'жы', 'жю', 'жя', 'зй', 'зщ', 'иы', 'иь', 'йй', 'йы', 'йь', 'кй', 'кщ', 'лй', 'мй', 'нй', 'оы', 'оь', 'пй', 'пх', 'пщ', 'пю', 'рй', 'сщ', 'тй', 'уы', 'уь', 'фж', 'фз', 'фй', 'фц', 'фш', 'фщ', 'фя', 'хй', 'хщ', 'хы', 'цй', 'цщ', 'ць', 'цю', 'чж', 'чй', 'чх', 'чц', 'чщ', 'чы', 'чю', 'чя', 'шж', 'шй', 'шч', 'шш', 'шщ', 'шы', 'шя', 'щб', 'щв', 'щг', 'щд', 'щж', 'щз', 'щй', 'щл', 'щм', 'що', 'щс', 'щт', 'щф', 'щх', 'щц', 'щч', 'щш', 'щщ', 'щы', 'щэ', 'щю', 'щя', 'ыы', 'ыь', 'ьй', 'ьы', 'ьь', 'эа', 'эе', 'эж', 'эи', 'эо', 'эц', 'эч', 'эщ', 'эы', 'эь', 'ээ', 'эю', 'эя', 'юы', 'юь', 'яы', 'яь']


def read_file_to_str(fname: str) -> str:
    text: str = ""
    with (open(fname, 'r', encoding="utf8") as f):
        text = f.read()
    return text


# all possible n-grams for specific alphabet
def gen_all_ngrs(alp: str = alp, n: int = 2, current_layer: int = 0):
    if(current_layer == n-1):
        for a in alp:
            yield a
    else:
        for a in alp:
            for g in gen_all_ngrs(alp, n, current_layer+1):
                yield a + g


# count with crosses    ("abcdef" contains "ab", "bc", "cd", "de", "ef")
def count_ngrs_crs(text: str, n: int = 2, alp: str = alp) -> dict[str, int]:
    ngrs: dict[str, int] = { ngr: 0 for ngr in gen_all_ngrs(alp, n)}
    for i in range(len(text)-n+1):
        ngrs[text[i:i+n]] += 1
    return ngrs


# count without crosses    ("abcdef" contains "ab", "cd", "ef")
def count_ngrs_seq(text: str, n: int = 2, alp: str = alp):
    ngrs: dict[str, int] = { ngr: 0 for ngr in gen_all_ngrs(alp, n)}
    for i in range(0, len(text)//n*n, n):
        ngrs[text[i:i+n]] += 1
    return ngrs


# just some sh1tcode for printing
def print_ngr_info(d: dict[str, int], n: int = 10):
    ngrs = list(d.keys())[0:n]
    for g in ngrs:
        print(f"'{g}'  {d[g]}")


def ngr_to_int(ngr: str, alp_len: int = alp_len, alp_ords: dict[str, int] = alp_ords) -> int:
    res: int = 0
    ngr_len = len(ngr)
    for i in range(ngr_len):
        res += alp_ords[ngr[i]] * alp_len**(ngr_len-i-1)
    return res


def int_to_ngr(n: int, ngr_len: int = 2, alp: str = alp):
    alp_len = len(alp)
    res = ""
    for i in range(ngr_len - 1, -1, -1):
        res += alp[ int(n / (alp_len**i)) ]
        n = n % (alp_len**i)
    return res


# in python 3.7+ dict order is preserved
def sort_dict(bgs: dict[str, int], dsc: bool = True) -> dict[str, int]:
    return dict(sorted(bgs.items(), key=lambda i: int(i[1]), reverse=dsc))


# gen pairs of most common OT bgrs and CT bgrs
def gen_all_possible_keys(ct: str, top_n_ct: int = 5, top_n_ot: int = 5) -> tuple[int, int]:
    ct_bgrs_seq = sort_dict(count_ngrs_seq(ct, 2))
    top_bgrs_ct: list[str] = list(ct_bgrs_seq.keys())[0:top_n_ct]
    top_bgrs_ot: list[str] = mc_bgrs[0:top_n_ot]

    m2 = alp_len**2

    # possible pairs of ct bgrs: 5*5-5
    for Y1 in top_bgrs_ct:
        Y1_code = ngr_to_int(Y1)
        #print(f"\nY1 = {Y1} = {Y1_code}")

        for Y2 in top_bgrs_ct:
            if Y1 == Y2:
                continue
            Y2_code = ngr_to_int(Y2)
            #print(f"  Y2 = {Y2} = {Y2_code}")

            # possible pairs of ot bgrs: 4!
            for X1 in range(top_n_ot-1):
                X1_code = ngr_to_int(top_bgrs_ot[X1])
                #print(f"    X1 = {top_bgrs_ot[X1]} = {X1_code}")

                for X2 in range(X1+1, top_n_ot):
                    X2_code = ngr_to_int(top_bgrs_ot[X2])
                    #print(f"      X2 = {top_bgrs_ot[X2]} = {X2_code}")

                    for s in solve_equation_system(Y1_code, X1_code, Y2_code, X2_code, m2):
                        yield s


# convert CT str bgr to int code; OT bgr code = a⁻¹ * (CT_bgr - b) mod m²
def decrypt_bgr(bgr_ct: str, a: int, b: int, alp: str = alp) -> str:
    m2: int = len(alp)**2
    ngr_ct_code = ngr_to_int(bgr_ct)
    #print(f"  {invert(a, m2)}")
    ngr_ot_code = (invert(a, m2) * (ngr_ct_code - b)) % m2
    return int_to_ngr(ngr_ot_code, 2)


# split text in bgrs and decrypt each of them
def decrypt(ct: str, a: int, b: int, n: int = 2, alp: int = alp) -> str:
    m2: int = len(alp)**2
    ot: str = ""
    for i in range(0, len(ct)//n*n, n):
        ot += decrypt_bgr(ct[i:i+n], a, b)
    return ot


# check if decrypted text seems to be valid.
def check_text(text: str) -> bool:
    bgrs_count = count_ngrs_seq(text)
    bgrs_total: int = len(text)//2


    # Idk why i use exactly these numbers to compare freqs.
    # Just tolerance to take into account that texts arent identical
    
    # max score - point if text's bgrs occurency frequences 100% corresponds to theoretical
    max_score = len(mc_bgrs) + len(lc_bgrs) + len(forbidden_bgrs)
    counter = 0
    
    # check most common bgrs 
    for mc_bgr in mc_bgrs:
        if bgrs_count[mc_bgr]/bgrs_total >= 0.0017:
            counter += 1

    # check least common bgrs
    for lc_bgr in lc_bgrs:
        if bgrs_count[lc_bgr]/bgrs_total <= 0.0002:
            counter += 1

    # check bgrs with 0 occurences in "Mein campf"
    for fb_bgr in forbidden_bgrs:
        if bgrs_count[fb_bgr]/bgrs_total <= 0.00001:
            counter += 1


    if counter/max_score > 0.75:
        #print(counter)
        return True
    else:
        return False


# go through potential keys, decrypt CT and ckeck if it seems to be valid
def try_keys(ct: str) -> tuple[int, int]:
    for a, b in gen_all_possible_keys(ct):
        ot = decrypt(ct, a, b)
        if (check_text(ot)):
            print(f"****    {a}, {b}    ****")
            yield (a, b)
