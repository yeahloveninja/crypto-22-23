from random import randint
from funcs_math import *
import multiprocessing as mp
from main import rand_prime_min, rand_prime_max


def eratosthenes(n: int):
    numbers: list = list(range(1, n+1, 2))
    for i in range(1, len(numbers)):
        if (numbers[i] != 0):
            for j in range(i + numbers[i], len(numbers), numbers[i]):
                numbers[j] = 0
    numbers[0] = 2
    return [a for a in numbers if a != 0]



#primes = eratosthenes(2**24)
#print(primes[len(primes)-1])
#print(len(primes))



def compare_prime_checkers(pid: int):
    rounds = 1
    while(True):
        for _ in range(10**6):
            r = randint(rand_prime_min, rand_prime_max)
            t1 = is_prime_fermat(r)
            t2 = is_prime_rabin(r)
            if (t1 != t2):
                print(f"\n{t1}, {t2}: {r}")
        print(f"{pid}.{rounds} ", end='')
        rounds += 1


if __name__ == "__main__":
    pss: list = [mp.Process(target=compare_prime_checkers, args=(i,)) for i in range(16)]
    for p in pss:
        p.start()
    for p in pss:
        p.join()




