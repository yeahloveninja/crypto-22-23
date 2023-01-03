from collections import Counter
import matplotlib.pyplot as plt


MAX_RELATIVE_FREQUENCY_RU = "о"


class Ops(object):
    """Operations with texts"""
    def __init__(self, text: str, alph: str) -> None:
        self.text, self.text_len = text, len(text)
        self.alph = alph

    def index(self) -> float:
        """Count chars in text -> compute index"""
        self.count()
        i = 0
        for k in self.chr_count.values():
            i += k * (k - 1)
        return i / (self.text_len * (self.text_len - 1))

    def count(self) -> dict[str, int]:
        """Count chars in text"""
        self.chr_count: dict[str, int] = {k: 0 for k in self.alph}
        for k in self.text:
            self.chr_count[k] += 1
        return self.chr_count
    
    def guess_key(self, key_len: int, depth: int = 2) -> list[str]:
        """Guess cipher key"""
        key_variables, possible_keys = [], [""] * depth
        for k in range(key_len):
            key_variables.append("".join(self.text[k::key_len]))

        for k in key_variables:
            b = {
                k: v for k, v in sorted(Counter(k).items(), key=lambda item: item[1], reverse=True)
            }
            sorted_chars = list(b.keys())   # chars sorted by frequency
            for i in range(depth):
                possible_keys[i] += self.alph[
                    (self.alph.index(sorted_chars[i]) - self.alph.index(MAX_RELATIVE_FREQUENCY_RU)) % \
                        len(self.alph)
                ]
        return possible_keys


def make_key_dict(text: str) -> dict[int, str]:
    """Make 15 keys for ecryption using frist 2,3,4,5,10-21 letters"""
    return {k: text[:k] for k in [*range(2, 6), *range(10, 21)]}


def plot(x: list, y: list) -> None:
    fig, ax = plt.subplots()
    xx = range(len(x))

    ax.bar(xx, y, 0.8, color='g', align='center')
    ax.set_xticks(xx)
    _ = ax.set_xticklabels(x)

    plt.show()