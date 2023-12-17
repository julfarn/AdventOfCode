
input_lines = open("F:\\Projekte\\AdventOfCode\\2023\\Day 14\\input.txt").read().splitlines()

# North wall:
wall_pos = [{"x": i, "y": -1} for i in range(len(input_lines[0]))]

for y in range(len(input_lines)):
    wall_pos += [{"x": x, "y": y} for x in range(len(input_lines[y])) if input_lines[y][x] == '#']

def count_rocks_below(wall_element):
    ret = 0
    for i in range(wall_element["y"] + 1, len(input_lines)):
        if(input_lines[i][wall_element["x"]] == '#'): break
        if(input_lines[i][wall_element["x"]] == 'O'): ret += 1
    return ret

def load_rocks_below(wall_element):
    c = count_rocks_below(wall_element)
    return c* (len(input_lines) - wall_element["y"]) - (c*(c+1))//2

load_sum = 0
for wall_element in wall_pos:
    load_sum += load_rocks_below(wall_element)

print(load_sum)