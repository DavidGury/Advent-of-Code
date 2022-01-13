def day01():
    '''pt1 - How many measurements are larger than the previous measurement?'''
    inp = list(map(int,inp.read().splitlines()))
    pt1 = sum([1 for i in range(1,len(inp)) if inp[i] > inp[i-1]])

    '''pt2 - moving groups of 3'''
    pt2 = sum([1 for i in range(1,len(inp)) if sum(inp[i:i+3]) > sum(inp[i-1:i+2])])

    return pt1,pt2
    

if __name__ == '__main__':
    print(day01(open('input.txt')))