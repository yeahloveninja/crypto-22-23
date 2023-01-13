from random import randint, randrange
from math import gcd
prime_check_iters = 32


def primes_eratosthenes(n: int):
    numbers: list = list(range(1, n+1, 2))
    for i in range(1, len(numbers)):
        if (numbers[i] != 0):
            for j in range(i + numbers[i], len(numbers), numbers[i]):
                numbers[j] = 0
    numbers[0] = 2
    return [a for a in numbers if a != 0]
known_primes_max: int = 2**20
known_primes = primes_eratosthenes(known_primes_max)
#print(f"primes found from 2 to {known_primes_max}: {len(known_primes)} pcs")


# a^n mod m
def mod_pow(a: int, n: int, p: int):
    res: int = 1
    a = a % p
    while (True):
        # check if lowest radix is 1
        #   (n%2 == 1) is a bit slower than (n & 00...001)
        if (n & 1):
            res *= a
            res %= p
            # seems to be a bit faster than res = (res * a) % p

        # exit if it was the last iteration
        if (n == 1):
            return res
        
        # shift n to use next radix in the next itaration
        n >>= 1
        a = (a * a) % p     # a**2 turned out to be much slower than a*a


# https://github.com/ipt-labs/crypto-22-23/blob/main/cp3/fb02_shapoval_cp3/funcs_math.py
def invert(x: int, m: int):
    #return pow(x, -1, m)
    old_m = m
    x = x % m
    
    prev = 0
    res: int = 1
    a: int = -1
    b: int = -1
    while(b != 1):
        a = m // x
        b = m % x
        m = x
        x = b
        prev, res = res, prev + res * a * (-1)
    return res % old_m


# https://www.geeksforgeeks.org/primality-test-set-2-fermet-method/  by Aanchal Tiwari
# descr: https://habr.com/ru/company/otus/blog/486116/
# Fermat's little theorem: (a in Z) and (n is prime) and (gcd(a, n)==1) ==> a^(n-1) % n = 1
def is_prime_fermat(n: int, check_iters: int = prime_check_iters) -> bool:
    # pre-calculated cases (not used here)
    if n <= known_primes_max:
        #print(f"[is_prime] {n} <= known_primes_max ", end='')
        if n in known_primes:
            #print(f"and is in known_primes")
            return True
        #print(f"but not in known_primes")
        return False    # if n is less than max known prime and not in prime list ==> it's not prime

    while check_iters > 0:
        # Pick a random number in [2..n-2]     
        a = randint(2, n - 2)
        # Fermat's little theorem
        if mod_pow(a, n - 1, n) != 1:
            return False
        check_iters -= 1
    return True


# https://gist.github.com/Ayrx/5884790
def is_prime_rabin(n: int, k: int=prime_check_iters):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def highest_power(n: int, base: int) -> int:
    p: int = 0
    while (n % base == 0):
        p += 1
        n /= base
    return p

def is_prime_mr(p: int, k: int = prime_check_iters) -> bool:
    if (p%2 == 0):
        if (p !=2):
            return False
    
    p1: int = p-1
    s: int = highest_power(p1, 2)
    d: int = int(p1 / 2**s)
    for _ in range(k):
        x: int = randint(2, p1)
        if (gcd(x, p) > 1):
            return False

        b: int = mod_pow(x, d, p)
        if (b in [p1, 1]):
            continue
        for r in range(1, s):
            b = mod_pow(b, 2, p)
            if (b == 1):
                return False
            elif (b == p1):
                break
    return True


