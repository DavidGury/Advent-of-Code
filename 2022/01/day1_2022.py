
elf_inventories = []
cur_total = 0
for line in map(str.strip, open('input.txt', 'r').readlines()):
    if not line:
        elf_inventories.append(cur_total)
        cur_total = 0
        continue
    cur_total += int(line)
elf_inventories = sorted(elf_inventories, reverse=True)

print(f'Pt1: {elf_inventories[0]}')
print(f'Pt2: {sum(elf_inventories[:3])}')