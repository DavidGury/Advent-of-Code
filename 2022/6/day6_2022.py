from collections import deque


inp = open('input.txt', 'r+').read()
start_of_packet = None
start_of_message = None
marker = deque()
letters = set()
for i, char in enumerate(inp):
    if len(letters) == 4 and start_of_packet is None:
        start_of_packet = i
    elif len(letters) == 14:
        start_of_message = i
        break
    while char in letters:
        rem = marker.popleft()
        letters.remove(rem)
    letters.add(char)
    marker.append(char)

print(f'Pt1: {start_of_packet}')
print(f'Pt2: {start_of_message}')
