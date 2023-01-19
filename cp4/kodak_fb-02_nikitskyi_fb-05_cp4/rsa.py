import pprint
import random
import math
from math import isqrt
from typing import List, Union, Tuple

def miller_rabin_test(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_random_prime(start=None, stop=None, length=None):
    if start is None and stop is None and length is None:
        raise ValueError("At least one of 'start', 'stop', or 'length' must be provided")
    if length is not None:
        start = 10**(length - 1)
        stop = (10**length) - 1
    if start >= stop:
        raise ValueError("'start' must be less than 'stop'")
    if start <= 1:
        raise ValueError("'start' must be greater than 1")
    if stop <= 2:
        raise ValueError("'stop' must be greater than 2")
    candidate = random.randint(start, stop)
    if candidate % 2 == 0:
        candidate += 1
    while not miller_rabin_test(candidate):
        candidate += 2
        if candidate >= stop:
            candidate = start
    return candidate


def expanded_gcd(a: int, m: int) -> Union[int, None]:
    """gcd calucation using extended Euclidean algorithm:
    https://planetcalc.ru/3311/
    """
    gcd, x, _ = extended_euclidean_algorithm(a, m)
    if gcd != 1:
        return None
    else:
        return x % m


def extended_euclidean_algorithm(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean_algorithm(b % a, a)
        return gcd, y - (b // a) * x, x



class DecryptionError(Exception):
	pass


class RSAAlgorithm(object):
	def __init__(self):
		self.p = generate_random_prime(2**255, 2**256)
		self.q = generate_random_prime(2**255, 2**256)
		
		self.__generate_key_pair_rsa()

	def __generate_key_pair_rsa(self) -> bool:
		"""RSA needs a public key (n, e) and private key (d).
			This method:
			- calculate "n"
			- caluclate the indicator of Euler
			- select random "e" to gcd(e, euler_func(n)) = 1
			- caluclate the modular inverse "d" (d = e^-1 mod (euler_func(n)))
		"""
		self.n = self.p * self.q
		euler_func = (self.p-1) * (self.q-1)
		self.e = random.randint(2, euler_func-1)

		while math.gcd(self.e, euler_func) != 1:
			self.e = random.randint(2, euler_func-1)
		self.d = expanded_gcd(self.e, euler_func) % euler_func

		return True
	
	@staticmethod
	def encrypt(M: int, e: int, n: int) -> int:
		"""Encrypt message M: C = M^e mod(n)"""
		return pow(M, e, n)
	
	@staticmethod
	def decrypt(C: int, d: int, n: int) -> int:
		"""Decrypt message C: M = C^d mod(n)"""
		return pow(C, d, n)
	
	@staticmethod
	def __verify(M: int, S: int, e: int, n: int) -> bool:
		"""Verify signature. If "M == S^e mod (n)", everything if fine"""
		return M == pow(S, e, n)

	def signature(self, M: int) -> int:
		"""Calculate signature S: S = M^d mod(n)"""
		return pow(M, self.d, self.n)

	def send_key(self, key: int, e_receiver: int, n_receiver: int) -> Tuple[int, int]:
		k_encrypted = self.encrypt(key, e_receiver, n_receiver)
		s_encrypted = self.encrypt(self.signature(key), e_receiver, n_receiver)
		return k_encrypted, s_encrypted
	
	def receive_key(self, key: int, signature: int, e_sender: int, n_sender: int):
		k_decrypted = self.decrypt(key, self.d, self.n)
		s_decrypted = self.decrypt(signature, self.d, self.n)
		
		
		if self.__verify(k_decrypted, s_decrypted, e_sender, n_sender):
			return k_decrypted

		raise DecryptionError("Message cannot be decrypted!")
	

if __name__ == "__main__":

	# Create instance of RSA class for each client	
	client_a = RSAAlgorithm()
	client_b = RSAAlgorithm()

	print(f"""
client_a info:\n
[+] public key:
	e: {client_a.e}
	n: {client_a.n}

[+] secret key:
	p: {client_a.p}
	q: {client_a.q}
	d: {client_a.d}\n

client_b info:\n
[+] public key:
	e: {client_b.e}
	n: {client_b.n}

[+] secret key:
	p: {client_b.p}
	q: {client_b.q}
	d: {client_b.d}
""")

	# Generate some message
	message = 22832213371488666777
	key = random.randint(0, client_a.n)

	print("Message:", message)
	print("Started k:", key)

	# Send key through signature creation, key and signature encryption 
	encrypted_key, encrypted_signature = client_a.send_key(key, client_b.e, client_b.n)
	print("Encrypted key:", encrypted_key)
	print("Encrypted signature:", encrypted_signature)
	
	print("\n")

	# encrypt message
	encrypted_message = client_a.encrypt(message, client_a.e, client_a.n)

	print("Encrypted message:", encrypted_message)

	
	# client b receives the key
	print(client_b.receive_key(encrypted_key, encrypted_signature, client_a.e, client_a.n))

	# if client_b received the key and validation was succeful
	decrypted_message = client_b.decrypt(encrypted_message, client_a.d, client_a.n)
	print("Decrypted message:", decrypted_message)

