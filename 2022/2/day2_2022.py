outcome_scores = {
    0: 3,  # draw
    1: 0,  # loss
    2: 6   # win
}

pt1_score = 0
pt2_score = 0
for line in map(str.strip, open('input.txt', 'r+')):
    a, b = line.split(' ')
    opp_shape = ord(a) - 65

    # pt1
    me_shape_pt1 = ord(b) - 88
    result_pt1 = (opp_shape - me_shape_pt1) % 3
    pt1_score += (me_shape_pt1 + 1) + outcome_scores[result_pt1]

    # pt2
    result_pt2 = (ord(b) - 89) * -1
    me_shape_pt2 = (opp_shape - result_pt2) % 3
    pt2_score += outcome_scores[result_pt2 % 3] + (me_shape_pt2 + 1)

print(f'Pt1: {pt1_score}')
print(f'Pt2: {pt2_score}')
