def split_string_in_half(s: str) -> tuple[str, str]:
    i_half = len(s) // 2
    return s[:i_half], s[i_half:]


def get_priority(s: str) -> int:
    return (ord(s.lower()) - 96) + (s.isupper() * 26)


inp = open('input.txt', 'r+').read().splitlines()

priority_sum_pt1 = 0
for comp_a, comp_b in map(split_string_in_half, inp):
    common_letter = (set(comp_a) & set(comp_b)).pop()
    priority_sum_pt1 += get_priority(common_letter)


priority_sum_pt2 = 0
for i in range(0, len(inp), 3):
    sack_1, sack_2, sack_3 = list(map(set, inp[i:i+3]))
    badge = ((sack_1 & sack_2) & (sack_1 & sack_3) & (sack_2 & sack_3)).pop()
    priority_sum_pt2 += get_priority(badge)


print(f'Pt1: {priority_sum_pt1}')
print(f'Pt2: {priority_sum_pt2}')