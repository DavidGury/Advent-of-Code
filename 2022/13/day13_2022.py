from __future__ import annotations
from dataclasses import dataclass, field, InitVar
import json

inp = open('input.txt', 'r+').read().splitlines()


def fix_types(left: str | list, right: str | list) -> tuple[str, str] | tuple[list, list]:
    match (left, right):
        case int(), list():
            left = [left]
        case list(), int():
            right = [right]
    return left, right


def is_correct(left: str | list, right: str | list) -> bool:
    match (left, right):
        case int(), int():
            return left < right
        case list(), list():
            return compare_lists(left, right)


def compare_lists(left_list: list, right_list: list) -> bool:
    min_len = min(l_len := len(left_list), r_len := len(right_list))
    if l_len != r_len and left_list[:min_len] == right_list[:min_len]:
        return l_len < r_len

    for l_, r_ in zip(left_list, right_list):
        if l_ is None:
            return True
        elif r_ is None:
            return False

        l_elem, r_elem = fix_types(l_, r_)
        if l_elem == r_elem:
            continue
        return is_correct(l_elem, r_elem)


pt1 = 0
for i, line in enumerate(range(0, len(inp), 3)):
    a, b = list(map(json.loads, inp[line:line+2]))
    if is_correct(a, b):
        pt1 += i+1
        continue

print(f'Pt1: {pt1}')


def get_first_char(pkt: list) -> int:
    if type(pkt) == int:
        return pkt
    elif not pkt:
        return -1
    return get_first_char(pkt[0])


pdata = sorted([get_first_char(json.loads(line)) for line in inp if line.strip()] + [2, 6])
print(f'Pt2: {(pdata.index(2)+1) * (pdata.index(6)+1)}')

