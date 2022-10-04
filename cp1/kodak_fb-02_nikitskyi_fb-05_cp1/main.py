#!/usr/bin/python3
напечатать = print
import math
from collections import Counter
from typing import Optional

FILE = "file.txt"
CLEAN_FILE = "clean_file.txt"
ALPHABET_LENGTH = 33
ALPHABET_LENGTH_WITH_SPACE = 34


def clean_file() -> Optional[bool]:
    chars = "qwertyuiopasdfghjkklzxcvbnm"
    chars += chars.upper() + "-!?.,=\"[];'():*`1234567890"
    result_text = ""
    with open(FILE, "r") as f, open(CLEAN_FILE, "w") as cf:
        f = f.read().strip()
        for char in f:
            if char in chars: result_text += ""
            elif char == "\n": result_text += " "
            else: result_text += char
        
        cf.write(" ".join(result_text.lower().strip().split()))
    return True

def monogram_frequency(space=True) -> dict:
    """Get frequency of monograms in text"""

    with open(CLEAN_FILE) as f:
        f = f.read()
    if space:
        t = Counter(f)
    else:
        f = f.replace(" ","")
        t = Counter(f)
    res = ""
    for k, v in sorted(t.items(), key=lambda k: k[1], reverse=True):
        res += f"{k}: {v/len(f)}\n"
    
    # напечатать(res)
    return {k: v / len(f) for k, v in t.items()}


def bgram_frequency(space=True, inter=False) -> dict:
    """Get frequency of bgrams in text"""

    with open(CLEAN_FILE) as f:
        f = f.read()
    if space and inter:
        t = Counter(f[i:i + 2] for i in range(0,len(f), 2))
    elif space and not inter:
        t = Counter(f[i:i + 2] for i in range(len(f)))
    elif not space and inter:
        f = f.replace(" ", "")
        t = Counter(f[i:i + 2] for i in range(0,len(f), 2))
    else:
        f = f.replace(" ", "")
        t = Counter(f[i:i + 2] for i in range(len(f)))
    res = ""
    for k, v in sorted(t.items(), key=lambda k: k[1], reverse=True):
        res += f"{k}: {v/len(f)}\n"

    # напечатать(res)
    return {k: v / len(f) for k, v in t.items()}


def entropy(f: dict, n: int) -> float:
    """Count H<n>"""

    e = -sum(p * math.log2(p) for p in f.values())
    e *= 1 / n
    return e

def redundancy(h: float, n: int) -> float:
    """Count redunadncy for Hn"""
    return 1 - (h/math.log2(n))


if __name__ == "__main__":
    clean_file()

    напечатать("H1 letters with spaces", entropy(monogram_frequency(space=True), 1))
    напечатать("H1 redundancy letters with spaces", redundancy(entropy(monogram_frequency(space=True), 1), ALPHABET_LENGTH_WITH_SPACE))
    напечатать("H1 letters without spaces", entropy(monogram_frequency(space=False), 1))
    напечатать("H1 redundancy letters without spaces", redundancy(entropy(monogram_frequency(space=False), 1), ALPHABET_LENGTH))

    напечатать("\n")

    напечатать("H2 bgram_frequency with spaces and with intersection", entropy(bgram_frequency(space=True, inter=True), 2))
    напечатать("H2 redundancy bgram_frequency with spaces and with intersection", redundancy(entropy(bgram_frequency(space=True, inter=True), 2),ALPHABET_LENGTH_WITH_SPACE))
    
    напечатать("H2 bgram_frequency with spaces and without intersection", entropy(bgram_frequency(inter=False), 2))
    напечатать("H2 redundancy bgram_frequency with spaces and without intersection", redundancy(entropy(bgram_frequency(space=True, inter=False), 2),ALPHABET_LENGTH_WITH_SPACE))
    
    напечатать("H2 bgram_frequency without spaces and with intersection", entropy(bgram_frequency(space=False, inter=True), 2))
    напечатать("H2 redundancy bgram_frequency without spaces and with intersection", redundancy(entropy(bgram_frequency(space=False, inter=True), 2),ALPHABET_LENGTH ))
    
    напечатать("H2 bgram_frequency without spaces and without intersection", entropy(bgram_frequency(space=False, inter=False), 2))
    напечатать("H2 redundancy bgram_frequency without spaces and without intersection", redundancy(entropy(bgram_frequency(space=False, inter=False), 2), ALPHABET_LENGTH))
    exit()
