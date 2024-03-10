goal1, goal2 = map(int, input().split(":"))
goal3, goal4 = map(int, input().split(":"))
flag = int(input())
first_guest = goal1 if flag == 2 else goal3
second_guest = goal2 if flag == 1 else goal4

first_goals = goal1 + goal3
second_goals = goal2 + goal4
if first_goals > second_goals or (first_goals == second_goals and first_guest > second_guest):
    print(0)
else:
    dif = second_goals - first_goals
    if flag == 1:
        first_guest += dif
        if first_guest > second_guest:
            print(dif)
        else:
            print(dif + 1)
    else:
        if first_guest > second_guest:
            print(dif)
        else:
            print(dif + 1)
