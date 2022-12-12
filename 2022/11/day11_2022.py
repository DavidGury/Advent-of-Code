from dataclasses import dataclass, field, InitVar
from collections import deque
import re
from typing import Callable, Iterable


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

    def inspect_all(self) -> Iterable[tuple[int, int]]:
        # print(f'Monkey {self.index}:')
        while self.items:
            yield self.inspect_next()

    def inspect_next(self) -> tuple[int, int]:

        self.n_inspections += 1
        item_wlvl = self.items.popleft()
        # print(f'\tMonkey inspects an item with a worry level of {item_wlvl}')
        w = self.op(item_wlvl, self.op_factor)
        # print(f'\t\tWorry level is {self.op} by {self.op_factor} to {w}')
        w //= 3
        # print(f'\t\tMonkey gets bored with item. Worry level is divided by 3 to {w}.')
        if w % self.div_test:
            # print(f'\t\tCurrent worry level is not divisible by {self.div_test}.')
            # print(f'\t\tItem with worry level {w} is thrown to monkey {self.fail_monkey}.')
            return self.fail_monkey, w
        # print(f'\t\tCurrent worry level is divisible by {self.div_test}.')
        # print(f'\t\tItem with worry level {w} is thrown to monkey {self.pass_monkey}.')
        return self.pass_monkey, w

    def receive_item(self, wlvl: int):
        self.items.append(wlvl)


op_ref = {
    '*': int.__mul__,
    '+': int.__add__,
    '^': int.__pow__
}

monkeys = []
inp = open('input.txt').read().splitlines()
i = 0
while i < len(inp):
    monkey_line, item_line, op_line, test_line, passtest_line, failtest_line = inp[i:i+6]
    i += 7
    oper, op_facstr = op_line.split(' ')[-2:]
    if op_facstr == 'old' and oper == '+':
        oper, op_facstr = '*', '2'
    elif op_facstr == 'old' and oper == '*':
        oper, op_facstr = '^', '2'

    monkeys.append(
        Monkey(
            index=len(monkeys),
            div_test=int(test_line.split(' ')[-1]),
            op=op_ref[oper],
            op_factor=int(op_facstr),
            pass_monkey=int(passtest_line.split(' ')[-1]),
            fail_monkey=int(failtest_line.split(' ')[-1]),
            item_worry_lvls=[int(m) for m in re.findall(r'\d+', item_line)]
        )
    )

N_ROUNDS = 20

for round_num in range(N_ROUNDS):
    for i in range(len(monkeys)):
        for rcv_monkey, wlvl in monkeys[i].inspect_all():
            monkeys[rcv_monkey].receive_item(wlvl)

# for m in monkeys:
#     print(m.items)

print('Pt1:', int.__mul__(*sorted([m.n_inspections for m in monkeys])[-2:]))