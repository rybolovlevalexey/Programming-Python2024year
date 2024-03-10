ans = 0
for i in range(int(input())):
    count = int(input())
    ans += count // 4
    count = count % 4
    if count in [0, 1, 2]:
        ans += count
    else:
        ans += 2
print(ans)
