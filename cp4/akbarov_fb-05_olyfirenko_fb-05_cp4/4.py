from random import randint, getrandbits
def is_prime_number(prime):
    for i in [2, 3, 5, 7, 11, 13,
              17, 19, 23, 29, 31,
              37, 41, 43, 47]:
        if prime % i == 0: return False
    k, s, d = 8, 0, prime - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    iteration = 0
    while iteration < k:
        x = randint(2, prime - 1)
        if greatest_common_divisor(x, prime) != 1: return False
        ps = modular_exponentiation(x, d, prime)
        if ps == 1 or ps == -1:
            iteration += 1
            continue
        for r in range(1, s):
            x = modular_exponentiation(x, 2, prime)
            if x == -1:
                return False
            elif x == 1:
                return True
        iteration += 1
        return False
    return True
def extended_euclidean_algorithm(num1, num2):
    if greatest_common_divisor(num1, num2) > 1: return 0
    val1, val2, list_of_nums = num2, num1, []
    while val2:
        list_of_nums.append(-(val1 // val2))
        val1, val2 = val2, val1 % val2
    for i in range(len(list_of_nums) - 1): list_of_nums.append(list_of_nums[i] * list_of_nums[-1] + list_of_nums[-2])
    return list_of_nums[-1] + num2 if list_of_nums[-1] < 0 else list_of_nums[-1]
def greatest_common_divisor(num1, num2):
    num2_2, list1 = num2, [-1]
    while list1[-1] != 0:
        list1.append(num1 - num1 // num2 * num2)
        num1, num2 = num2, list1[-1]
    return num2_2 if (list1[-1] == 0 and len(list1) == 2) else list1[-2]

def modular_exponentiation(index, d, num):
    d_bin, result = list(bin(int(d))[2:]), 1
    for i in range(len(d_bin)):
        result = ((result * (index ** int(d_bin[i]))) ** 2) % num if i != len(d_bin) - 1 else (result * (
                index ** int(d_bin[i]))) % num
    return result

def random_prime_number(size):
    while True:
        value = getrandbits(size)
        if is_prime_number(value):
            return value
def create_pair_of_prime_numbers():
    while True:
        prime1, prime2, prime3, prime4 = random_prime_number(256), random_prime_number(256), random_prime_number(256), random_prime_number(256)
        if prime1 * prime2 <= prime3 * prime4:
            return [[prime1, prime2], [prime3, prime4]]
def rsa_keys_pair(prime1, prime2):
    num = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)
    while True:
        exp = 65537
        if greatest_common_divisor(exp, phi) == 1:
            dec = extended_euclidean_algorithm(exp, phi)
            return [[dec, prime1, prime2], [exp, num]]
def encrypt_message(message, exp, num):
    return modular_exponentiation(message, exp, num)
def decrypt_message(code, dec, num):
    return modular_exponentiation(code, dec, num)
def get_message_and_signature(message, dec, num):
    return [message, modular_exponentiation(message, dec, num)]
def is_signature_verified(ms: list, exp, num):
    message, signature = ms[0], ms[1]
    return True if modular_exponentiation(signature, exp, num) == message else False
def start():
    mes = getrandbits(256)
    pairs = create_pair_of_prime_numbers()
    prime_pair1, prime_pair2 = pairs[0], pairs[1]
    keys_a = rsa_keys_pair(prime_pair1[0], prime_pair1[1])
    keys_b = rsa_keys_pair(prime_pair2[0], prime_pair2[1])
    dec1, prime1, prime2, exp1, num1 = keys_a[0][0], keys_a[0][1], keys_a[0][2], keys_a[1][0], keys_a[1][1]
    dec2, prime3, prime4, exp2, num2 = keys_b[0][0], keys_b[0][1], keys_b[0][2], keys_b[1][0], keys_b[1][1]
    code = encrypt_message(mes, exp1, num1)
    message_and_signature = get_message_and_signature(code, dec2, num2)
    decrypted_mes = decrypt_message(message_and_signature[0], dec1, num1) if is_signature_verified(message_and_signature, exp2, num2) else False
    if decrypted_mes:
        if decrypted_mes == mes: print(f'B→A: OK!')
    else:
        print(f'B→A: Failed!')
    print(f'\nprime1 = {prime1}\nprime2 = {prime2}\nprime3 = {prime3}\nprime4 = {prime4}\n\ndec1 = {dec1}\ndec2 = {dec2}\nexp = {exp1}\nnum1 = {num1}\nnum2 = {num2}')
    print(f'\nmes = {mes}\ncode = {code}\nsignature = {message_and_signature[1]}\nmes\' = {decrypted_mes}')
if __name__ == '__main__':
    start()