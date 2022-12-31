import RSA
import random

size = int(input("\n☼ Enter size value of prime number in bits:\n"
                 ">>> "))
p, q, p1, q1 = [1, 1, 0, 0]
while p * q > p1 * q1:
    p, q = RSA.generate_prime_pair(size)
    p1, q1 = RSA.generate_prime_pair(size)

print(f"[x]► Pair of prime numbers for user A\n"
      f"\t p = {p}\n"
      f"\t q = {q}\n")
print(f"[x]► Pair of prime numbers for user B\n"
      f"\tp1 = {p1}\n"
      f"\tq1 = {q1}\n\n")


e, n, d = RSA.GenerateKeyPair(p, q)
print(f"[***]► Generation RSA key pair for user A\n"
      f"• Public key of user A:\n"
      f"\t e = {e}\n"
      f"\t n = {n}\n"

      f"• Secret key of user A:\n"
      f"\t d = {d}\n"
      f"\t p = {p}\n"
      f"\t q = {q}\n")

e1, n1, d1 = RSA.GenerateKeyPair(p1, q1)
print(f"[***]► Generation RSA key pair for user B\n"
      f"• Public key of user B:\n"
      f"\te1 = {e1}\n"
      f"\tn1 = {n1}\n"

      f"• Secret key of user B:\n"
      f"\td1 = {d1}\n"
      f"\tp1 = {p1}\n"
      f"\tq1 = {q1}\n")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("=" * 45, "\n", "+" * 45, "\n", "=" * 45, "\n", sep="")
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


M = random.randrange(1, n)
print(f"Message --→ {M} \n")


B_encrypt_text_for_A = RSA.Encrypt(M, e, n)
print("* User B encrypt message for user A: ", B_encrypt_text_for_A)
sign_by_B = RSA.Sign(B_encrypt_text_for_A, d1, n1)
print("[]> Digital signature of user B: ", sign_by_B)

A_encrypt_text_for_B = RSA.Encrypt(M, e1, n1)
print("* User A encrypt message for user B: ", A_encrypt_text_for_B)
sign_by_A = RSA.Sign(A_encrypt_text_for_B, d, n)
print("[]> Digital signature of user A: ", sign_by_A)


A_decrypt_text_from_B = RSA.Decrypt(B_encrypt_text_for_A, d, n)
if RSA.Verify(B_encrypt_text_for_A, sign_by_B, e1, n1):
    print("")
    print("[*] User A decrypt message from user B after successful signature verification: ", A_decrypt_text_from_B)
else:
    print("")
    print("[!] Unsuccessful verification of digital signature.")

B_decrypt_text_from_A = RSA.Decrypt(A_encrypt_text_for_B, d1, n1)
if RSA.Verify(A_encrypt_text_for_B, sign_by_A, e, n):
    print("[*] User B decrypt message from user A after successful signature verification: ", B_decrypt_text_from_A)
    print("")
else:
    print("[!] Unsuccessful verification of digital signature.")
    print("")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("=" * 45, "\n", "+" * 45, "\n", "=" * 45, "\n", sep="")
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


K = random.randrange(1, n)
print(f"Key --→ {K}\n")


A_gen_K1, A_gen_S1 = RSA.SendKey(K, e1, n1, d, n)
print(f"> User A forms message (K1, S1) ↔ ({A_gen_K1}, {A_gen_S1}) and sends it to user B")
print(f"> User B using own secret key finds shared key ↓")
RSA.ReceiveKey(A_gen_K1, A_gen_S1, d1, n1, e, n)

B_gen_K1, B_gen_S1 = RSA.SendKey(K, e, n, d1, n1)
print(f"> User B forms message (K1, S1) ↔ ({B_gen_K1}, {B_gen_S1}) and sends it to user A")
print(f"> User A using own secret key finds shared key ↓")
RSA.ReceiveKey(A_gen_K1, A_gen_S1, d1, n1, e, n)
