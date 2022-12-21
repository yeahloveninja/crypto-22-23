def eratosthenes(n: int):
    numbers: list = list(range(1, n+1, 2))
    for i in range(1, len(numbers)):
        if (numbers[i] != 0):
            for j in range(i + numbers[i], len(numbers), numbers[i]):
                numbers[j] = 0
    numbers[0] = 2
    return [a for a in numbers if a != 0]



primes = eratosthenes(2**24)
#print(primes[len(primes)-1])
print(len(primes))
