import numpy as np

inp = open('input.txt', 'r+').read().splitlines()
arr = np.array([list(map(int, line)) for line in inp], dtype=np.uint8)
visible = np.full(arr.shape, False, dtype=bool)

for i in range(2):
    for j in range(2):
        max_vals = np.full((arr.shape[0],), -1, dtype=int)
        for x in range(arr.shape[1]):
            is_new_max = arr[:, x] > max_vals
            visible[:, x][is_new_max] = True
            max_vals[is_new_max] = arr[:, x][is_new_max]
            # print(max_vals)
        arr = np.flip(arr, axis=1)
        visible = np.flip(visible, axis=1)
    arr = np.transpose(arr)
    visible = np.transpose(visible)

print(f'Pt1: {np.sum(visible)}')

scenic_scores = np.full(arr.shape, 1, dtype=int)
meets_height = np.full(arr.shape, False, dtype=bool)

for n in range(9, -1, -1):
    is_n = arr == n
    meets_height[is_n] = True
    for direction in range(4):
        for y, x in np.transpose(np.where(is_n)):
            # go from left
            row = meets_height[y, :x]
            if not np.any(row):
                scenic_scores[y, x] *= row.size
                continue
            n_trees_seen = x - np.max(np.where(row)[0])
            scenic_scores[y, x] *= n_trees_seen

        is_n = np.rot90(is_n)
        meets_height = np.rot90(meets_height)
        scenic_scores = np.rot90(scenic_scores)

print(f'Pt2: {np.max(scenic_scores)}')