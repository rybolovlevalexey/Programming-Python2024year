n, k, d = map(int, input().split())
ans = None
variants = set()
variants.add(n)
for i in range(d):
    new_vars = set()
    for var in variants:
        if k % 2 == 0:
            for c in range(0, 10, 2):
                if int(str(var) + str(c)) % k == 0:
                    new_vars.add(int(str(var) + str(c)))
        elif k % 3 == 0:
            for c in range(sum(list(var)) % 3, 10, 3):
                if int(str(var) + str(c)) % k == 0:
                    new_vars.add(int(str(var) + str(c)))
        elif k % 5 == 0:
            for c in [0, 5]:
                if int(str(var) + str(c)) % k == 0:
                    new_vars.add(int(str(var) + str(c)))
        else:
            for c in range(0, 10):
                if int(str(var) + str(c)) % k == 0:
                    new_vars.add(int(str(var) + str(c)))
    variants = new_vars
print(list(variants)[0] if len(variants) > 0 else -1)
