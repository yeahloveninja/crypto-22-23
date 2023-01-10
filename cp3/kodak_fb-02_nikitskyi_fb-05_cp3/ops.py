from collections import Counter
from typing import Union, List, Tuple


class MathOps(object):
    """Class which implements some math calculation logic"""

    def gcd(self, a: int, b: int) -> int:
        """Common gcd calculation"""
        if b == 0:
            return a
        else:
            return self.gcd(b, a % b)

    def expanded_gcd(self, a: int, m: int) -> Union[int, None]:
        """gcd calucation using extended Euclidean algorithm:
        https://planetcalc.ru/3311/
        """
        gcd, x, _ = self.extended_euclidean_algorithm(a, m)
        if gcd != 1:
            return None
        else:
            return x % m
    
    def extended_euclidean_algorithm(self, a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_euclidean_algorithm(b % a, a)
            return gcd, y - (b // a) * x, x
    
    def mod_equation(self, a: int, b: int, m: int) -> int:
        """Calculate mod equation"""
        # check if a and m are relatively prime
        if self.gcd(a, m) == 1:
            # use the extended Euclidean algorithm to find the modular inverse of "a"
            inverse = self.extended_euclidean_algorithm(a, m)[1]
            # multiply the inverse by "b" to find the solution
            return (inverse * b) % m
        # if a and m are not relatively prime, then the equation has no solution
        return 


class BgramOps(object):
    """Class which implements some bgrams operaion logic"""

    ALPH = "абвгдежзийклмнопрстуфхцчшщьыэюя"
    TOP_BGRAMS = ["ст", "но", "то", "на", "ен"]

    def __init__(self, file: str) -> None:
        self.file = file

    def top_bgrams(self) -> List[str]:
        """Get top 5 bgrams from target file"""
        with open(self.file, "r", encoding="utf-8") as f:
            f = f.read()
        t = Counter(f[i:i + 2] for i in range(0,len(f)-1))
        return [k[0] for k in t.most_common(5)]

    def bigram_to_num(self, bigram: str) -> int:
        """Convert bgram to number using this formula:
        Xi = x2i-1 * m + x2i
        """
        return self.ALPH.index(bigram[0]) * 31 +\
            self.ALPH.index(bigram[1])
    
    def num_to_bgram(self, num: int) -> str:
        """Convert number to bgram using reverse algorithm to bigram_to_num func
        """
        return self.ALPH[num // 31] + self.ALPH[num % 31]

    def _validate(self, to_validate: List[str]) -> str:
        """Validate texts using bgrams by checking chars frequency
        "о" -> 10.97%
        "е" -> 8.45%
        "ф" -> 0.26%
        "щ" -> 0.36
        https://ru.wikipedia.org/wiki/%D0%A7%D0%B0%D1%81%D1%82%D0%BE%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C
        """
        for text in to_validate:
            if text.count('о')/len(text) < 0.095 or text.count('е')/len(text) < 0.08:
                continue
            if text.count('ф')/len(text) > 0.004 or text.count('щ')/len(text) > 0.005:
                continue
            result_text = text
        return result_text

    def _bgram_frequency(self, text: str) -> List[str]:
        """Calucalte bgram frequency. Algorithm from 1 lab"""
        t = Counter(text[i:i + 2] for i in range(0,len(text)-1))
        total_count = sum(t.values())
        frequencies = {}
        for bigram, count in t.items():
            frequencies[bigram] = count / total_count
        return frequencies

