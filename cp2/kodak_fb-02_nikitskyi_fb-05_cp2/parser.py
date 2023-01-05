#!/usr/bin/env python3
s = "\n.;:,-"

with open("ciphertext_bad.txt", "r") as r:
  a = r.read().strip()
  
with open("ciphertext.txt", "w") as f:
  a = a.replace(" ", "").replace("ё", "е")
  for k in range(len(s)):
    if s[k] in a:
      a = a.replace(s[k], "")
  f.write(a.lower())
