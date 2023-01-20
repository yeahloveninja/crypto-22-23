import itertools
from ops import BgramOps
from ops import MathOps
from typing import List, Tuple


class AffineCipherAttack(BgramOps):
    """Class to make an attack on affine cipher"""

    def __init__(self, file: str) -> None:
        self.file = file
        super().__init__(self.file)

        # read an encrypted text from target file
        with open(self.file, encoding='utf8') as f:
            self.encrypted_text = f.read().replace("\n", "")

    def create_system(self) -> List[tuple[str, str]]:
        """Create system of bgrams:
         /- Y* = aX* + b(mod m^2)
        |
         \- Y* = aX* + b(mod m^2)
        """
        mode_bigrams_cipher = self.top_bgrams()
        bgrams, result_system = [], []
        bgrams = list(itertools.product(self.TOP_BGRAMS, mode_bigrams_cipher))

        # iterate over bgrams and make a filtration
        for i in bgrams:
            for j in bgrams:

                # if bgrams are equal
                if i == j:  continue

                # if bgrams already exists
                elif (j, i) in result_system: continue

                # if first bgram from first pair is equal to frist bgram from second pair
                elif i[0] == j[0]: continue

                # second brams from first pair is equal to second bgram from second pair
                elif i[1] == j[1]: continue

                # otherwise add to result list
                result_system.append((i, j))

        return result_system 

    def roots(self, set_: tuple[tuple[str]]) -> List[tuple[int, int]]:
        """Get roots for each pair of bgram using this formula:
        Y* - Y** = a(X* - X**)(mod m^2)

        Return (a: int, b: int)
        """
        # Y*
        y_s = self.bigram_to_num(set_[0][0]) - self.bigram_to_num(set_[1][0])

        # Y**
        y_ss = self.bigram_to_num(set_[0][1]) - self.bigram_to_num(set_[1][1])

        a = MathOps().mod_equation(y_s, y_ss, 31 ** 2)
        if a:
            # b = (Y* - aX*)(mod m^2)
            b = (self.bigram_to_num(set_[0][1]) -\
                a * self.bigram_to_num(set_[0][0])) % 31 ** 2
            return a, b

    def get_keys(self) -> List[Tuple[int, int]]:
        """Iterate over bgram systems and find root of each pair"""
        keys = []
        system = self.create_system()
        for i in system:
            roots = self.roots(i)
            if roots:
                keys.append(roots)
        return keys

    def decrypt(self, keys: List[Tuple[int, int]]) -> List[str]:
        """Decrypt text based on key pair
        Xi = (a^-1) * (Y-b) (mod m)

        Validate decrypted text after a represent most correct text
        """
        # list of decrypted text
        decrypted = []

        # iterate over list of keys
        for k in keys:
            result_bgrams = []
            a, b = k[0], k[1]

            # calulate "a^-1" using Euclid algo
            a = MathOps().expanded_gcd(a, 31**2)

            # iterate over encrypted text with step 2 (bgram)
            for i in range(0, len(self.encrypted_text), 2):
                # Xi = (a^-1) * (Y-b) (mod m)
                x_i = (a * (
                    self.bigram_to_num(self.encrypted_text[i:i+2]) - b
                )) % (31**2)

                result_bgrams.append(self.num_to_bgram(x_i))

            # combine bgrams to solid text
            decrypted.append("".join(k for k in result_bgrams))

        return self._validate(decrypted)


if __name__ == "__main__":
    c = AffineCipherAttack("03.txt")
    rev = c.get_keys()
    print(c.decrypt(rev))
