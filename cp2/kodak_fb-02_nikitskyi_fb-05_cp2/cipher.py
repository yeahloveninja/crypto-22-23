class VigenereCipher(object):
    def __init__(self, text: str, key: str, alph: str):
        self.alph, self.alph_len = alph, len(alph)
        self.text, self.text_len = text, len(text)
        self.key, self.key_len = key, len(key)

        self.generate_key()

    def generate_key(self) -> str:
        """Generate key repeating it until it matches the length of the plaintext """
        if self.text_len == self.key_len: return self.key
        for k in range(self.text_len - self.key_len):
            self.key += self.key[k % self.key_len]
        return self.key

    def encrypt(self) -> str:
        """Ci = (Mi + Ki) mod N"""
        result: str = ""
        for k in range(len(self.text)):
            result += self.alph[(self.alph.index(self.text[k]) + self.alph.index(self.key[k])) % self.alph_len]
        return result

    def decrypt(self) -> str:
        """Mi = (Ci - Ki) mod N"""
        result: str = ""
        for k in range(len(self.text)):
            result += self.alph[(self.alph.index(self.text[k]) - self.alph.index(self.key[k])) % self.alph_len]

        return result
