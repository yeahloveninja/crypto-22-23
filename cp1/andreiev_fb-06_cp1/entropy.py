import re

with open('sample_text.txt', 'r') as f:
    text = f.read()

text = re.sub(r'[^\w ]', '', text).replace("  ", " ").lower()

char_counter = {}

for char in text:
    char_counter.setdefault(char, 0)
    char_counter[char] += 1

#char_counter.pop(' ', None)
char_counter = dict(sorted(char_counter.items(), key=lambda x: x[1], reverse=True))
print(char_counter)