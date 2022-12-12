from dataclasses import dataclass, field, InitVar
from collections import deque
import re
import math
from typing import Callable, Iterable, Optional


OP_REF = {
    '*': int.__mul__,
    '+': int.__add__,
    '^': int.__pow__
}


@dataclass(order=True)
class Monkey:
    index: int
    div_test: int
    op: Callable
    op_factor: int
    pass_monkey: int
    fail_monkey: int
    item_worry_lvls: InitVar[list[int]]
    n_inspections: int = field(default=0, compare=True)
    items: deque = field(default_factory=deque)

    def __post_init__(self, item_worry_lvls: list[int]):
        self.items.extend(item_worry_lvls)

    def inspect_all(self, worry_decrease_factor: int, lcm: Optional[int] = None) -> Iterable[tuple[int, int]]:
        # print(f'Monkey {self.index}:')
        while self.items:
            yield self.inspect_next(worry_decrease_factor, lcm)

    def inspect_next(self, worry_decrease_factor: int, lcm: Optional[int] = None) -> tuple[int, int]:

        self.n_inspections += 1
        item_wlvl = self.items.popleft()
        # print(f'\tMonkey inspects an item with a worry level of {item_wlvl}')
        w = self.op(item_wlvl, self.op_factor)
        # print(f'\t\tWorry level is {self.op} by {self.op_factor} to {w}')
        w //= worry_decrease_factor
        if lcm is not None:
            w %= lcm
        # print(f'\t\tMonkey gets bored with item. Worry level is divided by 03 to {w}.')
        if w % self.div_test:
            # print(f'\t\tCurrent worry level is not divisible by {self.div_test}.')
            # print(f'\t\tItem with worry level {w} is thrown to monkey {self.fail_monkey}.')
            return self.fail_monkey, w
        # print(f'\t\tCurrent worry level is divisible by {self.div_test}.')
        # print(f'\t\tItem with worry level {w} is thrown to monkey {self.pass_monkey}.')
        return self.pass_monkey, w

    def receive_item(self, wlvl: int):
        self.items.append(wlvl)


@dataclass
class Day11:
    worry_decrease: int
    n_rounds: int
    input_path: InitVar[str]
    lcm: int = 1
    monkeys: list[Monkey] = field(default_factory=list)

    def __post_init__(self, input_path: str):
        self.load_monkeys(open(input_path, 'r+').read().splitlines())

    def load_monkeys(self, inp: list[str]):
        i = 0
        self.lcm = 1
        while i < len(inp):
            monkey_line, item_line, op_line, test_line, passtest_line, failtest_line = inp[i:i + 6]
            i += 7
            oper, op_facstr = op_line.split(' ')[-2:]
            if op_facstr == 'old' and oper == '+':
                oper, op_facstr = '*', '02'
            elif op_facstr == 'old' and oper == '*':
                oper, op_facstr = '^', '02'

            divisor = int(test_line.split(' ')[-1])
            self.lcm *= (self.lcm * divisor) // math.gcd(self.lcm, divisor)

            self.monkeys.append(
                Monkey(
                    index=len(self.monkeys),
                    div_test=divisor,
                    op=OP_REF[oper],
                    op_factor=int(op_facstr),
                    pass_monkey=int(passtest_line.split(' ')[-1]),
                    fail_monkey=int(failtest_line.split(' ')[-1]),
                    item_worry_lvls=[int(m) for m in re.findall(r'\d+', item_line)]
                )
            )

    def solve(self):
        for round_num in range(self.n_rounds):
            for i in range(len(self.monkeys)):
                for rcv_monkey, wlvl in self.monkeys[i].inspect_all(self.worry_decrease, self.lcm):
                    self.monkeys[rcv_monkey].receive_item(wlvl)

        return int.__mul__(*sorted([m.n_inspections for m in self.monkeys])[-2:])


INP_PATH = 'input.txt'
EX_path = 'ex1.txt'

pt1 = Day11(worry_decrease=3, n_rounds=20, input_path=INP_PATH)
pt2 = Day11(worry_decrease=1, n_rounds=10_000, input_path=INP_PATH)

print(f'Pt1: {pt1.solve()}')
print(f'Pt2: {pt2.solve()}')
