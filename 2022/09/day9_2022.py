from dataclasses import dataclass, field, InitVar


inp = open('input.txt', 'r+').read().splitlines()


@dataclass
class Rope:
    size: int
    directions: dict[str, tuple[int, int]] = field(init=False)
    knot_locs: list[tuple[int, int]] = field(init=False)
    seen: set[tuple[int, int]] = field(init=False)

    def __post_init__(self):
        self.knot_locs = [(0, 0) for i in range(self.size)]
        self.seen = {(0, 0)}
        self.directions = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }

    @property
    def n_tail_locs(self) -> int:
        return len(self.seen)

    def direct(self, d: str):
        self.move(*self.directions[d])

    def move(self, y_move: int, x_move: int):
        y, x = self.knot_locs[0]
        self.knot_locs[0] = (y + y_move, x + x_move)
        self.update_knot_pos(1)

    def update_knot_pos(self, knot_index: int):
        if knot_index == self.size:
            return self.log_tail_pos()

        py, px = self.knot_locs[knot_index-1]
        y, x = self.knot_locs[knot_index]

        y_diff, x_diff = abs(py-y), abs(px-x)

        if y_diff < 2 and x_diff < 2:
            return

        self.knot_locs[knot_index] = (y + min(1, max(-1, py-y)), x + min(1, max(-1, px-x)))
        self.update_knot_pos(knot_index+1)

    def log_tail_pos(self):
        self.seen.add(self.knot_locs[-1])


pt1_rope = Rope(size=2)
pt2_rope = Rope(size=10)
for d, n in map(str.split, inp):
    for step in range(int(n)):
        pt1_rope.direct(d)
        pt2_rope.direct(d)

print(f'Pt1: {pt1_rope.n_tail_locs}')
print(f'Pt2: {pt2_rope.n_tail_locs}')

