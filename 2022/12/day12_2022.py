from dataclasses import dataclass, field, InitVar
import heapq
import re


def can_step(cur_char: str, next_char: str) -> bool:
    if next_char == 'E':
        next_char = 'z'
    if cur_char == 'S':
        cur_char = 'a'
    if cur_char.isupper() or ord(cur_char) + 1 >= ord(next_char):
        return True
    return False


@dataclass
class Day12:
    start_chars: InitVar[str]
    input_path: InitVar[str]
    q: list[tuple[int, tuple[int, int]]] = field(default_factory=list)
    _map: list[str] = field(init=False)

    def __post_init__(self, start_chars: str, input_path: str):
        self._map = open(input_path, 'r+').read().splitlines()
        for char in start_chars:
            for r in re.finditer(char, ''.join(self._map)):
                y, x = divmod(r.start(), len(self._map[0]))
                heapq.heappush(self.q, (0, (y, x)))

    def find_shortest_path(self):
        h, w = len(self._map), len(self._map[0])
        seen = set()
        while self.q:
            n_steps, (y, x) = heapq.heappop(self.q)
            if self._map[y][x] == 'E':
                return n_steps
            if (y, x) in seen:
                continue
            seen.add((y, x))

            for _y, _x in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]:
                if not (0 <= _y < h and 0 <= _x < w):
                    continue
                if can_step(self._map[y][x], self._map[_y][_x]):
                    heapq.heappush(self.q, (n_steps + 1, (_y, _x)))

        return 'No valid path'


pt1 = Day12(start_chars='S', input_path='input.txt')
pt2 = Day12(start_chars='Sa', input_path='input.txt')

print(f'Pt1: {pt1.find_shortest_path()}')
print(f'Pt2: {pt2.find_shortest_path()}')