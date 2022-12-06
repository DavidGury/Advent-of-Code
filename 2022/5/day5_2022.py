from collections import deque
import re

inp = open('input.txt', 'r+').read().splitlines()

for line_index, line in enumerate(inp):
    if not line.strip():
        break

stacks, instructions = inp[:line_index-1], inp[line_index+1:]
stack_start = ['']
for y, row in enumerate(stacks):
    for x, char in enumerate(row):
        if x % 4 != 1:
            continue
        elif char.isspace():
            continue
        stack_no = x//4 + 1
        while len(stack_start) <= stack_no:
            stack_start.append('')
        stack_start[stack_no] += char

stacks_pt1 = [deque(s) for s in stack_start]
stacks_pt2 = [deque(s) for s in stack_start]

for instr in instructions:
    n_moved, _from, _to = list(map(int, re.findall(r'\d+', instr)))
    stacks_pt2[_from].rotate(-n_moved)
    for _ in range(n_moved):
        stacks_pt1[_to].appendleft(stacks_pt1[_from].popleft())
        stacks_pt2[_to].appendleft(stacks_pt2[_from].pop())

print('Pt1:', ''.join(s.popleft() for s in stacks_pt1[1:]))
print('Pt2:', ''.join(s.popleft() for s in stacks_pt2[1:]))


