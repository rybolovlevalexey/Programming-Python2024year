import string

st = input()
flags = [False, False, False, False]
if len(st) >= 8:
    flags[0] = True
for elem in st:
    if elem in "1234567890":
        flags[1] = True
    if elem.isupper() and elem in string.ascii_letters:
        flags[2] = True
    if elem.islower() and elem in string.ascii_letters:
        flags[3] = True
print("YES" if all(flags) else "NO")
