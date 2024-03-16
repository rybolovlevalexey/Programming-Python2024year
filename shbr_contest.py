from string import ascii_letters

correct = input()
st = input()
command = None
com_flag = False
text: list[str] = list()
index = -1
for i in range(len(st)):
    elem = st[i]
    if elem not in ascii_letters and elem not in ["<", ">"]:
        continue
    if elem == "<" and (st[i + 1:].startswith("delete") or st[i + 1:].startswith("bspace") or
                        st[i + 1:].startswith("left") or st[i + 1:].startswith("right")):
        com_flag = True
    elif elem == ">" and com_flag:
        com_flag = False
        if len(text) == 0:
            index = -1
        else:
            if command == "delete":
                if 0 <= index + 1 < len(text):
                    del text[index + 1]
            elif command == "bspace":
                if 0 <= index < len(text):
                    del text[index]
                    index -= 1
            elif command == "left":
                if index > 0:
                    index -= 1
            elif command == "right":
                if index + 1 < len(text):
                    index += 1
            command = None
    else:
        if com_flag:
            if command is None:
                command = ""
            command += elem
        else:
            index += 1
            if len(text) == 0 or len(text) == index:
                text.append(elem)
            else:
                text.insert(index, elem)

if "".join(text).lower() == correct.lower():
    print("Yes")
else:
    print("No")