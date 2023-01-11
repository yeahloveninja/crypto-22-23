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









def compare_prime_checkers(pid: int):
    for _ in range(200):
        r = randint(rand_prime_min, rand_prime_max)
        t1 = is_prime_fermat(r)
        t2 = is_prime_rabin(r)
        t3 = is_prime_mr(r, 128)
        if (t1 != t2 or t2 != t3 or t1 != t3):
            print(f"pid {pid}    {t1}, {t2}, {t3}: {r}")
    print(f"--==  pid {pid} finished  ==--")


if __name__ == "__main__":
    pss: list = [mp.Process(target=compare_prime_checkers, args=(i,)) for i in range(4)]
    for p in pss:
        p.start()
    for p in pss:
        p.join()





