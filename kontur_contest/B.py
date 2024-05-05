st = input()
if len(st) % 2 == 1 and len(set(st)) != 1:
    print(len(st) - max(st.count("1"), st.count("0")))
else:
    parts = list()  # другое представление исходной строки - (символ, сколько раз встречается)
    all_lengths = dict()  # какие бывают длины: сколько раз они встречаются
    cur_symbol: str = ""
    cur_count: int = 0

    for elem in st:
        if cur_count == 0:
            cur_count += 1
            cur_symbol = elem
        elif cur_symbol == elem:
            cur_count += 1
        else:
            if cur_count in all_lengths:
                all_lengths[cur_count] += 1
            else:
                all_lengths[cur_count] = 1
            parts.append((cur_symbol, cur_count))
            cur_symbol = elem
            cur_count = 1
    parts.append((cur_symbol, cur_count))
    if cur_count in all_lengths:
        all_lengths[cur_count] += 1
    else:
        all_lengths[cur_count] = 1

    bad_parts_couples = list()
    for target_len in all_lengths.keys():
        bad_couple = list()
        for part in parts:
            if part[1] == target_len:
                if len(bad_couple) > 0:
                    bad_parts_couples.append(bad_couple)
                    bad_couple = list()
            else:
                bad_couple.append(part)
        if len(bad_couple) > 0:
            bad_parts_couples.append(bad_couple)
            bad_couple = list()
        print(target_len, bad_parts_couples)