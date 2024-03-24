n, t = map(int, input().split())
lower_bound = sum(list(map(int, input().split())))
upper_bound = sum(list(map(int, input().split())))

if lower_bound <= t <= upper_bound:
    print("YES")
else:
    print("NO")