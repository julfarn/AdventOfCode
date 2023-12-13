
input_lines = open("input.txt").read().splitlines()

emptylines = []
for i in range(len(input_lines)):
    if input_lines[i] =='':
        emptylines.append(i)

maps = [input_lines[:emptylines[0]]]
for i in range(1, len(emptylines)):
    maps.append(input_lines[emptylines[i-1]+1:emptylines[i]])
maps.append(input_lines[emptylines[-1]+1:])

def check_horizontal(map):
    for i in range(0,len(map[0])-1):
        found_asym = False
        for c in range(i+1, min(len(map[0]), 2*(i +1))):
            for r in range(len(map)):
                if(map[r][c] != map[r][2*i-c+1]):
                    found_asym = True
                    break
            if(found_asym): break
        if not found_asym:
            return i+1
    return 0

def check_vertical(map):
    for i in range(0,len(map)-1):
        found_asym = False
        for r in range(i+1, min(len(map), 2*(i +1))):
            for c in range(len(map[0])):
                if(map[r][c] != map[2*i-r+1][c]):
                    found_asym = True
                    break
            if(found_asym): break
        if not found_asym:
            return i+1
    return 0

summary = 0
for map in maps:
    h_sym = check_horizontal(map)
    if h_sym != 0:
        summary+= h_sym
    else:
        summary+= 100* check_vertical(map)

print(summary)