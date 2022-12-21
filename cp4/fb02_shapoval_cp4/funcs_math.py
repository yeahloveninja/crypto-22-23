
def primes_eratosthenes(n: int):
    numbers: list = list(range(1, n+1, 2))
    for i in range(1, len(numbers)):
        if (numbers[i] != 0):
            for j in range(i + numbers[i], len(numbers), numbers[i]):
                numbers[j] = 0
    numbers[0] = 2
    return [a for a in numbers if a != 0]
known_primes_max: int = 2**8
known_primes = primes_eratosthenes(known_primes_max)



# https://www.geeksforgeeks.org/primality-test-set-2-fermet-method/  by Aanchal Tiwari
#   xⁿ mod p
'''def mod_pow(x, n, p):
    if (n<0):
        raise IOError("[mod_pow] n must be >0")

    res = 1
    x = x % p   # avoid x>=p and x<0
    
    while n > 0:
        # If n is odd, multiply 'a' with result
        if n % 2:
            res = (res * x) % p
            n = n - 1
        else:
            x = (x ** 2) % p
            # n must be even now
            n = n // 2
    return res % p'''

def mod_pow(x, y, m):
    res = 1
    x = x%m
    while y > 0:
        if y & 1:
            res = (res*x)%m
        y = y >> 1
        x = (x*x)%m
    return res


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



























