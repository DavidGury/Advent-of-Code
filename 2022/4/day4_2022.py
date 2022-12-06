import re

complete_overlap = 0
any_overlap = 0
for line in open('input.txt', 'r+').readlines():
    a1, a2, b1, b2 = list(map(int, re.findall(r'\d+', line)))
    if (a1 == min(a1, b1) and a2 == max(a2, b2)) or (b1 == min(a1, b1) and b2 == max(a2, b2)):
        complete_overlap += 1
    if a1 <= b1 <= a2 or b1 <= a1 <= b2:
        any_overlap += 1

print(f'Pt1: {complete_overlap}')
print(f'Pt2: {any_overlap}')


