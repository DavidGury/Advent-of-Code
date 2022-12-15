from dataclasses import dataclass, field, InitVar
import re
import numpy as np


@dataclass
class Day15:
    input_path: InitVar[str]
    sensors_beacons: list[tuple[tuple[int, int], tuple[int, int]]] = field(init=False)
    y_level: int

    def __post_init__(self, input_path: str):
        self.sensors_beacons = self.read_input(input_path)

    @staticmethod
    def read_input(fpath: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        sb = []
        for line in open(fpath, 'r+').read().splitlines():
            sx, sy, bx, by = list(map(int, re.findall(r'-?\d+', line)))
            sb.append(((sx, sy), (bx, by)))

        return sb

    def solve(self) -> int:
        locs = set()
        rm_locs = set()
        for (sx, sy), (bx, by) in self.sensors_beacons:
            mh_dist = abs(sx-bx) + abs(sy-by)
            y_diff = abs(sy - self.y_level)
            if mh_dist < y_diff:
                continue
            if by == self.y_level:
                rm_locs.add(bx)
            x_dist = mh_dist - y_diff
            locs |= set(range(sx - x_dist, sx + x_dist + 1))
        locs -= rm_locs

        return len(locs)


@dataclass
class Day15Pt2(Day15):
    max_loc: int
    y_level = None

    def get_arrays(self):
        sy_vals = []
        sx_vals = []
        dists = []
        for (sx, sy), (bx, by) in self.sensors_beacons:
            sy_vals.append(sy)
            sx_vals.append(sx)
            dists.append(abs(sy-by) + abs(sx-bx))

        return np.array(sy_vals), np.array(sx_vals), np.array(dists)

    @staticmethod
    def get_sat_oor(y_coord, x_coord, r):
        N, S, W, E = y_coord - r - 1, y_coord + r + 1, x_coord - r - 1, x_coord + r + 1

        coords = [  # min_y, max_y, y_dir, min_x, max_x, x_dir for each border quadrant
            [N, y_coord, 1, x_coord, E, 1],  # N -> E
            [y_coord, S, 1, x_coord, E, -1],  # E -> S
            [y_coord, S, -1, W, x_coord, -1],  # S -> W
            [N, y_coord, -1, W, x_coord, 1]  # W -> N
        ]

        for min_y, max_y, y_dir, min_x, max_x, x_dir in coords:
            y_clips = [max(0, -min_y), max(0, max_y - 40_000_000)][::y_dir]
            x_clips = [max(0, -min_x), max(0, max_x - 40_000_000)][::x_dir]
            start_clip = max(y_clips[0], x_clips[1])
            end_clip = max(y_clips[0], x_clips[1])

            ya, yb = [min_y, max_y][::y_dir]
            xa, xb = [min_x, max_x][::x_dir]

            for y, x in zip(range(ya + start_clip, yb + 1 - end_clip), range(xa + start_clip, xb + 1 - end_clip)):
                yield y, x

    def solve(self):
        sy_vals, sx_vals, mh_dists = self.get_arrays()
        for sy, sx, mh in zip(sy_vals, sx_vals, mh_dists):
            for y, x in self.get_sat_oor(sy, sx, mh):
                if not (0 <= y <= self.max_loc and 0 <= x <= self.max_loc):
                    continue
                dists_from_sats = np.abs(sy_vals-y) + np.abs(sx_vals-x)
                if np.all((mh_dists - dists_from_sats) < 0):
                    return x*4_000_000+y


pt1 = Day15('input.txt', y_level=2_000_000)
pt2 = Day15Pt2('input.txt', y_level=0, max_loc=4_000_000)

print(f'Pt1: {pt1.solve()}')
print(f'Pt2: {pt2.solve()}')



