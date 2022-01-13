import re


def day02(inp):
    depth_1 = 0
    xpos_1 = 0
    aim_2 = 0
    depth_2 = 0
    hpos_2 = 0
    
    for line in inp:
        d,N = line.split(' ')
        N = int(N)
        if d == 'forward':
            xpos_1 += N
            hpos_2 += N
            depth_2 += N*aim_2
        elif d == 'down':
            depth_1 += N
            aim_2 += N
        elif d == 'up':
            depth_1 -= N
            aim_2 -= N
    Pt1 = depth_1*xpos_1
    Pt2 = hpos_2*depth_2
    
    return Pt1,Pt2
    
    
if __name__ == '__main__':
    day02(open('input.txt'))