
def ext_gcd(a, b):
    if a == 0:
        x = 0
        y = 1
        return (b, x, y)
    else:
        gcd, y, x = ext_gcd(b % a, a)
        x = x - (b // a) * y
        return (gcd, x, y)

def inverse_mod(a, m):
    gcd, x, y = ext_gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        print("Inverse doesn't exist")
        return

# ax = b mod n 
def solve_mod_eq(a, b, n):
    d = ext_gcd(a, n)[0]
    if d == 1:
        return (inverse_mod(a, n) * b) % n
    elif d > 1:
        if b % d != 0:
            return 
        else:
            a, b, n = a // d, b // d, n // d
            root = solve_mod_eq(a, b, n)
            return [root + (i * n) for i in range(d)]

