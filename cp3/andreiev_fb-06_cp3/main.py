
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

print(inverse_mod(18, 25))