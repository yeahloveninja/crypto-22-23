from funcs_math import *
from math import gcd

rand_prime_min: int = int('1'+'0'*255, 2)
rand_prime_max: int = int('1'*256, 2)



def rand_prime(range_min: int = rand_prime_min, range_max: int = rand_prime_max, check_iters: int = prime_check_iters) -> int:
    attempts: int = 0
    res: int
    while(True):
        attempts += 1
        res = randint(range_min, range_max)
        if (is_prime_fermat(res, check_iters)):
            #print(f"[rand_prime] attempts = {attempts}")
            return res


def gen_pq_pair() -> tuple[int, int]:
    return rand_prime(), rand_prime()


# -> p_A, q_A, p_B, q_B
# (p_A <= p_B) and (q_A <= q_B)
def gen_pq_pairs() -> tuple[int, int, int, int]:
    p_A, q_A = gen_pq_pair()
    p_B, q_B = gen_pq_pair()
    if p_A > p_B : p_A, p_B = p_B, p_A
    if q_A > q_B : q_A, q_B = q_B, q_A
    return p_A, q_A, p_B, q_B


# C = Mᵉ mod n
def encrypt(Msg: int, e_rcvr: int, n_rcvr: int) -> int:
    return mod_pow(Msg, e_rcvr, n_rcvr)


# M = Cᵈ mod n
def decrypt(C: int, d_rcvr: int, n_rcvr: int) -> int:
    return mod_pow(C, d_rcvr, n_rcvr)


# S = Mᵈ mod n
# (returns only sign)
def sign(Msg: int, d: int, n: int) -> int:
    return mod_pow(Msg, d, n)


# M == Sᵉ mod n
def verify(Msg: int, Sgn: int, e: int, n: int) -> bool:
    return Msg == mod_pow(Sgn, e, n)


# msg is (k_encrypted, S_encrypted)
#  k_encrypted = k^(e_rcvr) mod n_rcvr      (encrypt secret k)
#  S = k^(d_sndr) mod (n_sndr)              (sign secret k, 0<k<n_sndr)
#  S_encrypted = S^(e_rcvr) mod n_rcvr      (encrypt S)
def send_secret_k(k_open: int, d_sndr: int, n_sndr: int, e_rcvr: int, n_rcvr: int) -> tuple[int, int]:
    if (k_open >= n_sndr):
        print("k must be 0 < k < n_sndr")
        print(f"  n.sndr = {n_sndr}")
        print(f"  k      = {k_open}")
        return
    if (n_rcvr < n_sndr):
        print("n_rcvr must be >= n_sndr")
        print(f"  n_rcvr = {n_rcvr}")
        print(f"  n_sndr = {n_sndr}")
        print(f"  you have to gen new keys")
        return
    k_encrypted = encrypt(k_open, e_rcvr, n_rcvr)
    S = sign(k_open, d_sndr, n_sndr)
    S_encrypted = encrypt(S, e_rcvr, n_rcvr)
    #print(f"[send_secret_k]")
    #print(f"  k     : {k_open} --> {k_encrypted}")
    #print(f"  S     : {k_encrypted}")
    return (k_encrypted, S_encrypted)


# k = (k_encrypted)^(self.d) mod self.n     (decrypt key)
# S = (S_encrypted)^(self.d) mod self.n     (decrypt sign)
# k ?= S^(e_sndr) mod n_sndr                (verify with sign)
def recv_secret_k(k_encrypted: int, S_encrypted: int, e_sndr: int, n_sndr: int, d_rcvr: int, n_rcvr: int) -> bool:
    k = decrypt(k_encrypted, d_rcvr, n_rcvr)
    S = decrypt(S_encrypted, d_rcvr, n_rcvr)
    print("[recv_secret_k]")
    print(f"  decrypted k: {hex(k)}")
    return verify(k, S, e_sndr, n_sndr)


class User:
    # pub: (n, e)
    # priv: d
    def __init__(self, name):
        self.name = name
        self.p: int = -1
        self.q: int = -1
        self.n: int = -1
        self.phi: int = -1
        self.e: int = -1
        self.d: int = -1

    def gen_keys(self, p, q) -> None:
        self.p = p
        self.q = q
        self.n: int = self.p * self.q
        self.phi: int = (self.p - 1) * (self.q - 1)
        while (True):
            self.e = randint(2, self.phi)
            if (gcd(self.e, self.phi) == 1):
                self.d = invert(self.e, self.phi)
                break

    def regen_n_less_than(self, others_n: int):
        while(True):
            #   Reinitializing p, q, n is cringe but let it be
            self.p, self.q = rand_prime(), rand_prime()
            self.n = self.p * self.q
            if (self.n < others_n):
                self.gen_keys(self.p, self.q)
                return

    def print_vars_hex(self):
        print(f"user {self.name}:")
        print(f"  p = {hex(self.p)}")
        print(f"  q = {hex(self.q)}")
        print(f"  n = {hex(self.n)}")
        print(f"  φ = {hex(self.phi)}")
        print(f"  e = {hex(self.e)}")
        print(f"  d = {hex(self.d)}")



# tests for https://asymcryptwebservice.appspot.com/?section=rsa
if __name__ == "__main__":
    server = User("Server")
    server.n = 0x976CE483778B2195B81D4B16372ED02592B5508F98C8B6D6C230A82FFB24E01C09BD40D9EC77A104884C4C9D2732402C537DEF3D25DF5B5CBBA9098D7DB42B95
    server.e = 0x10001
    server.print_vars_hex()

    client = User("Client")
    #client.gen_keys(rand_prime(), rand_prime())
    client.gen_keys(0xeb6c89d281e20b9334d1a574c99faed3d123fab1ac35c6e5b75e8631960a5799, 0xc4645be8e618de25bcf0ffbdc27e45b7f500afcef3acd9466ef0165144939a0d)
    client.print_vars_hex()

    msg: int = 0x1488

    msg_enc_by_client: int = encrypt(msg, server.e, server.n)
    print(f"Client encrypts msg for Server:\n    {hex(msg_enc_by_client)}")


    msg_enc_by_server: int = encrypt(msg, client.e, client.n)
    print(f"Server encrypts msg for Client:\n    {hex(msg_enc_by_server)}")

    msg_dec_by_client: int = decrypt(msg_enc_by_server, client.d, client.n)
    print(f"Client decrypts msg from Server:\n    {hex(msg_dec_by_client)}")



    signature_by_server: int = 0x176EE81AB4691EBBF4F4DAC4FFDA5F2E54AAD61B02030C8EFC28DA16FE1AEB709E0F1F403C1A6184375484C21CA51A249675454BEFBA47229B1954CF504AA69E
    print(f"Client verivies msg from Server: {verify(msg, signature_by_server, server.e, server.n)}")

    signature_by_client: int = sign(msg, client.d, client.n)
    print(f"Client signs msg: \n    {hex(signature_by_client)}")



    #client.regen_n_less_than(server.n)
    client.gen_keys(0xe08223cee541e8ae7b1b305b5af3f0227339fd9dd0647b8241059de4f8fded89, 0x9a3184beaaf621e308227ac8692e64def286cf97b8b606f4c3c4ecee54d67e5f)
    client.print_vars_hex()

    k_enc_by_client, S_by_client = send_secret_k(msg, client.d, client.n, server.e, server.n)
    print(f"Client sends secret k")
    print(f"  k_enc: {hex(k_enc_by_client)}")
    print(f"  S_enc: {hex(S_by_client)}")


    print(f"Client receives secret k")
    k_enc_by_server = int(input("  key: "), 16)
    S_by_server = int(input("  signature: "), 16)
    k_from_server = recv_secret_k(k_enc_by_server, S_by_server, server.e, server.n, client.d, client.n)
    print(f"  {k_from_server}")




