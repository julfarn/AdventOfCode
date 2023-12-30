import re
input_strings = open("F:\\Projekte\\AdventOfCode\\2023\\Day 18\\input.txt").read().splitlines()

instruction_count = len(input_strings)

regex = r"(?P<dir_old>[LDRU])\s(?P<len_old>\d+)\s\(\#(?P<len>[a-f \d]{5})(?P<dir>[a-f \d]{1})"

directions = []
distances = []
red,green,blue = [],[],[]
dirdict = ['R', 'D', 'L', 'U']
for line in input_strings:
    m = re.match(regex, line)
    directions.append(dirdict[int(m["dir"])])
    distances.append(int(m["len"], 16))

def is_convex(i):
    dirchange = directions[i] + directions[(i+1)%instruction_count]
    return dirchange in ['RD', 'DL', 'LU', 'UR']

def convex_nr(i):
    ret = -1
    if(is_convex((i-1)%instruction_count)): ret += 1
    if(is_convex(i)): ret += 1
    return ret

area = 0
ypos = 5611
for i in range(instruction_count):
    if(directions[i] == 'U'): 
        ypos -= distances[i] + convex_nr(i)
    elif(directions[i] == 'D'): 
        ypos += distances[i] + convex_nr(i)
    elif(directions[i] == 'L'): 
        area += (ypos) * (distances[i] + convex_nr(i)) 
    elif(directions[i] == 'R'): 
        area -= (ypos) * (distances[i] + convex_nr(i))


print(str(area))