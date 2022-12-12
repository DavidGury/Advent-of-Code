from dataclasses import dataclass, field


@dataclass
class Day10Pt1:
    x: int = 1
    cycle: int = 0
    increment: int = 40
    measure_at: int = 20
    end: int = 220
    signal: int = 0

    def __post_init__(self):
        self.process_cycle(val=0)

    @property
    def is_done(self) -> bool:
        return self.cycle >= self.end

    def print_signal(self):
        print(f'Pt1: {self.signal}')

    def process_cycle(self, val: int = 0):
        if self.is_done:
            return

        self.x += val
        self.cycle += 1
        if self.cycle == self.measure_at:
            self.record_signal()

    def record_signal(self):
        self.signal += self.cycle * self.x
        self.measure_at += self.increment


@dataclass
class Day10Pt2:
    x: int = 1
    cycle: int = 0
    end: int = 240
    crt: list[str] = field(default_factory=list)
    crt_row: str = ''

    @property
    def is_done(self) -> bool:
        return len(self.crt) == 6

    def print_crt(self) -> None:
        print('Pt2:')
        for line in self.crt:
            print(''.join(line))
        print()

    def process_cycle(self, val: int = 0):
        if self.is_done:
            return
        self.crt_row += '#' if self.x - 1 <= len(self.crt_row) <= self.x + 1 else ' '
        print(self.crt_row[-1])
        if len(self.crt_row) == 40:
            self.crt.append(self.crt_row)
            self.crt_row = ''

        self.x += val
        self.cycle += 1


pt1 = Day10Pt1()
pt2 = Day10Pt2()
for line in open('input.txt', 'r+').read().splitlines():
    pt1.process_cycle(val=0)
    pt2.process_cycle(val=0)
    if line.startswith('addx'):
        v = int(line.split()[1])
        pt1.process_cycle(v)
        pt2.process_cycle(v)
    if pt1.is_done and pt2.is_done:
        break

pt1.print_signal()
pt2.print_crt()
