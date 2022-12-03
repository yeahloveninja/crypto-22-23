import math
from typing import Tuple


def invert(x: int, m: int):
    #return pow(x, -1, m)
    
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

    return res



# ax = b (mod n)
# yield return all possible x <= n
def solve_equation(a: int, b: int, n: int) -> int:
    gcd_a_n = math.gcd(a, n)
    if(gcd_a_n == 1):
        # x = a * b^(-1)  mod n
        return ( invert(a, n) * b ) % n
    else:
        if(b % gcd_a_n != 0):
            return None
        else:
            a = a//gcd_a_n
            b = b//gcd_a_n
            n = n//gcd_a_n
            for i in range(gcd_a_n):
                yield ( invert(a, n) * b ) % n + i * n


# Y1 = (a*X1 + b) mod m**2
# Y2 = (a*X2 + b) mod m**2
# yield return all possible (a, b) pairs
def solve_equation_system(Y1: int, X1: int, Y2: int, X2: int, m: int) -> tuple[int, int]:
    #print(f"          solving equation system:")
    #print(f"            {Y1} = {X1}a + b  (mod {m})")
    #print(f"            {Y2} = {X2}a + b  (mod {m})")

    for a in solve_equation(X1 - X2, Y1 - Y2, m):
        yield (a, (Y1 - a*X1) % m)


