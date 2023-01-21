import random
import math


class MillerTest:
    def __init__(self, num, k=8):
        self.num = num
        self.k = k

    def test_number(self):
        if self.num == 2 or self.num == 3:
            return True
        if self.num % 2 == 0:
            return False
        r, s = 0, self.num - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        for _ in range(self.k):
            a = random.randrange(2, self.num - 1)
            x = pow(a, s, self.num)
            if x == 1 or x == self.num - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, self.num)
                if x == self.num - 1:
                    break
            else:
                return False
        return True


class PrimaryNumber:
    def __init__(self, bits):
        self.bits = bits

    def find_number(self):
        print("Not primary numbers\n")
        while True:
            prim_number = (random.randrange(2 ** (self.bits - 1), 2 ** self.bits))
            if not MillerTest(prim_number).test_number():
                print(f"{prim_number}")
            else:
                return prim_number


class KeyGenerator:
    def __init__(self):
        pass

    def generate_keys(self):
        keys = []
        for _ in range(4):
            key = PrimaryNumber(256).find_number()
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys


class EvclidExtended:
    def __init__(self, first_number, second_number):
        self.first_number = first_number
        self.second_number = second_number

    def extended_evclid(self):
        if self.first_number == 0:
            return self.second_number, 0, 1
        else:
            div, koef_x, koef_y = EvclidExtended(self.second_number % self.first_number,
                                                 self.first_number).extended_evclid()
        return div, koef_y - (self.second_number // self.first_number) * koef_x, koef_x


class ModInverse:
    def __init__(self, first_number, second_number):
        self.first_number = first_number
        self.second_number = second_number

    def inverse_mod(self):
        return list(EvclidExtended(self.first_number, self.second_number).extended_evclid())[1]


class RSAKeyPair:
    def __init__(self, first_key, second_key):
        self.first_key = first_key
        self.second_key = second_key

    def rsa_pair(self):
        res = []
        n = self.first_key * self.second_key
        oiler = (self.first_key - 1) * (self.second_key - 1)
        e = random.randrange(2, oiler - 1)
        while math.gcd(e, oiler) != 1:
            e = random.randrange(2, oiler - 1)
        d = ModInverse(e, oiler).inverse_mod() % oiler
        res.append(d)
        res.append(n)
        res.append(e)
        return res


class Encrypting:
    def __init__(self, m, e, n):
        self.m = m
        self.e = e
        self.n = n

    def enc_msg(self):
        return pow(self.m, self.e, self.n)


class Decryption:
    def __init__(self, c, d, n):
        self.c = c
        self.d = d
        self.n = n

    def dec_msg(self):
        return pow(self.c, self.d, self.n)


class DigitalSign:
    def __init__(self, m, d, n):
        self.m = m
        self.d = d
        self.n = n

    def sign(self):
        return pow(self.m, self.d, self.n)


class SignCheck:
    def __init__(self, m, s, e, n):
        self.m = m
        self.s = s
        self.e = e
        self.n = n

    def sign_check(self):
        if self.m == pow(self.s, self.e, self.n):
            print("Success")
        else:
            print("Fail")
        return self.m == pow(self.s, self.e, self.n)


class KeySend:
    def __init__(self, k, d, e_1, n_1, n):
        self.k = k
        self.d = d
        self.e_1 = e_1
        self.n_1 = n_1
        self.n = n

    def send_key(self):
        k_1 = Encrypting(self.k, self.e_1, self.n_1).enc_msg()
        s = DigitalSign(self.k, self.d, self.n).sign()
        s_1 = Encrypting(s, self.e_1, self.n_1).enc_msg()
        return k_1, s_1


class KeyReceiving:
    def __init__(self, key_1, s_1, d_1, n_1, e, n):
        self.key_1 = key_1
        self.s_1 = s_1
        self.d_1 = d_1
        self.n_1 = n_1
        self.e = e
        self.n = n

    def receive_key(self):
        key = Decryption(self.key_1, self.d_1, self.n_1).dec_msg()
        s = Decryption(self.s_1, self.d_1, self.n_1).dec_msg()
        if SignCheck(key, s, self.e, self.n).sign_check():
            return True, key
        else:
            return False, 0


n = int("AB377B7E3A23BFA837930FD72C3C2DBEB9D96D74D9CF3472F4D44B53FF273CD3", 16)
print(f'n: {n}')
e = int("10001", 16)
print(f'e: {e}')
msg = int("54321", 16)
print(f'Message: {msg}')
encrypted_msg = Encrypting(msg, e, n).enc_msg()
print(f"Ciphertext: {hex(encrypted_msg)}")
sign = int("31EFEFBE9C0994E2F9144A5900D5F58936CE58346D4E4C3F006101000AB6A15F", 16)
print(f"Sign is: {sign}")
SignCheck(msg,sign,e,n).sign_check()