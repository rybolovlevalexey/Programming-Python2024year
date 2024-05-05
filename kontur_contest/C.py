n, q = map(int, input().split())
bitten_lines = list()  # игреки
bitten_columns = list()  # иксы
ladyies = list()  # (x, y)

for num in range(q):
    action, x, y = input().split()
    x, y = int(x) - 1, int(y) - 1
    if action == "+":
        ladyies.append([x, y])
        if x not in bitten_columns:
            bitten_columns.append(x)
        if y not in bitten_lines:
            bitten_lines.append(y)
    else:
        del ladyies[ladyies.index([x, y])]
        if x not in list(map(lambda coord: coord[0], ladyies)):
            del bitten_columns[bitten_columns.index(x)]
        if y not in list(map(lambda coord: coord[1], ladyies)):
            del bitten_lines[bitten_lines.index(y)]

    field = list(list("*" * n) if i not in bitten_lines else list("x" * n) for i in range(n))
    for bit_col in bitten_columns:
        for i in range(n):
            field[i][bit_col]
    count = 0
    while "*" in field:
        sp = list()
        coord = [field.index("*") % n, field.index("*") // n]
        field[field.index("*")] = "*"
        sp.append(coord)
        while len(sp) > 0:
            if coord[0] + 1 < n:
                if field[coord[0] + 1 + coord[1] * n] == "*":
                    sp.append([coord[0] + 1, coord[1]])
            if coord[0] - 1 >= 0:
                if field[coord[0] - 1 + coord[1] * n] == "*":
                    sp.append([coord[0] - 1, coord[1]])

            if coord[0] - 1 >= 0 and field[coord[0] - 1 + coord[1] * n] == "*":
                sp.append([coord[0] - 1, coord[1]])
            if coord[1] + 1 < n and field[coord[0] + (coord[1] + 1) * n] == "*":
                sp.append([coord[0], (coord[1] + 1) * n])
            if coord[1] - 1 >= 0 and field[coord[0] + (coord[1] - 1) * n] == "*":
                sp.append([coord[0], (coord[1] - 1) * n])

        count += 1