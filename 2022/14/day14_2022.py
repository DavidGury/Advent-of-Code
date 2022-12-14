import json
import itertools
import numpy as np
from collections import deque

inp = open('input.txt', 'r+').read().splitlines()

# Read input and create list of rock lines that need to be made
x_min = float('inf')
y_max = x_max = float('-inf')
rock_lines = []
for line in inp:
    line = json.loads('[[' + line.replace(' -> ', '], [') + ']]')
    y_vals = [y for x, y in line]
    x_vals = [x for x, y in line]
    y_max = max(max(y_vals), y_max)
    x_min = min(min(x_vals), x_min)
    x_max = max(max(x_vals), x_max)
    rock_lines.extend(itertools.pairwise(line))

Y_BUFFER = 2
X_BUFFER = y_max
ROCK, SAND, EMPTY, SAND_SOURCE = '#o.+'
SAND_Y, SAND_X = 0, 500

h = y_max + 3
w = x_max + x_min
vis = np.full((h, w), '.', dtype=str)

# Fill in rock areas
vis[SAND_Y, SAND_X] = SAND_SOURCE
for (from_x, from_y), (to_x, to_y) in rock_lines:
    from_x, to_x = from_x, to_x
    if from_y == to_y:
        vis[from_y, min(from_x, to_x):max(from_x, to_x)+1] = ROCK
    elif from_x == to_x:
        vis[min(from_y, to_y):max(from_y, to_y)+1, from_x] = ROCK


reset_from = (SAND_Y, SAND_X)
y, x = reset_from
pt1 = None
while 1:
    if y+1 == h:
        break
    left, middle, right = vis[y+1, x-1:x+2] == EMPTY
    if middle:
        y += 1
    elif left:
        y, x = y+1, x-1
    elif right:
        y, x = y+1, x+1
    else:
        vis[y, x] = SAND
        y, x = reset_from
pt1 = np.sum(vis == SAND)

vis[-1, :] = ROCK
seen = set()
q = deque([(SAND_Y, SAND_X)])
pt2 = None
while q:
    y, x = q.popleft()
    if (y, x) in seen:
        continue
    seen.add((y, x))
    vis[y, x] = SAND
    for x_ in range(x-1, x+2):
        if vis[y+1, x_] == ROCK:
            continue
        q.append((y+1, x_))
pt2 = np.sum(vis == SAND)

print(f'Pt1: {pt1}')
print(f'Pt2: {pt2}')

# print('\n'.join(''.join(line) for line in vis))
