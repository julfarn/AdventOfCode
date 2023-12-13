import itertools

maze = open("input_ex.txt").read().splitlines()

link_symbols = "-|F7JL"
links = {
    "-": ["w", "e"],
    "|": ["n", "s"],
    "F": ["s", "e"],
    "7": ["w", "s"],
    "J": ["n", "w"],
    "L": ["e", "n"]
}

def out_direction(in_direction, segment):
    if links[segment][0] == opposite_direction(in_direction):
        return links[segment][1]
    elif links[segment][1] == opposite_direction(in_direction):
        return links[segment][0]
    print("error")

def opposite_direction(direction):
    if direction == 'n': return 's'
    if direction == 'e': return 'w'
    if direction == 's': return 'n'
    if direction == 'w': return 'e'
    print("error")

def follow_direction(direction, row, col):
    if direction == 'n': return [row -1, col]
    if direction == 'e': return [row, col+1]
    if direction == 's': return [row +1, col]
    if direction == 'w': return [row, col-1]
    print("error")

# Find starting position
start_pos_r = 0
start_pos_c = 0
foundstart = False
for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == 'S':
            start_pos_r = row
            start_pos_c = col
            foundstart = True
            break
    if(foundstart): break

if not foundstart: print("Could not find start!")

# Find starting segments
seg_r = []
seg_c = []
seg_dir = []

# These checks assume that the starting point does not lie on the boundary.
# check north
check_r = start_pos_r-1
check_c = start_pos_c
if(maze[check_r][check_c] in link_symbols and "s" in links[maze[check_r][check_c]]):
    seg_r.append(start_pos_r)
    seg_c.append(start_pos_c)
    seg_dir.append("n")

# check east
check_r = start_pos_r
check_c = start_pos_c+1
if(maze[check_r][check_c] in link_symbols and "w" in links[maze[check_r][check_c]]):
    seg_r.append(start_pos_r)
    seg_c.append(start_pos_c)
    seg_dir.append("e")

# check south
check_r = start_pos_r+1
check_c = start_pos_c
if(maze[check_r][check_c] in link_symbols and "n" in links[maze[check_r][check_c]]):
    seg_r.append(start_pos_r)
    seg_c.append(start_pos_c)
    seg_dir.append("s")

# check west
check_r = start_pos_r
check_c = start_pos_c-1
if(maze[check_r][check_c] in link_symbols and "e" in links[maze[check_r][check_c]]):
    seg_r.append(start_pos_r)
    seg_c.append(start_pos_c)
    seg_dir.append("w")


# Follow the maze!
steps = 0
while(steps == 0  or seg_c[0] != seg_c[1] or seg_r[0] != seg_r[1]):
    for path in [0,1]:
        seg_r[path], seg_c[path] = follow_direction(seg_dir[path], seg_r[path], seg_c[path])
        #print("Following path " + str(path) + " in direction " + str(seg_dir[path]) + 
        #      ", encountering segment " + maze[seg_r[path]][seg_c[path]] + 
        #      " at row " + str(seg_r[path]) + ", col " + str(seg_c[path]) + 
        #      ".")
        seg_dir[path] = out_direction(seg_dir[path], maze[seg_r[path]][seg_c[path]])
    steps += 1
print(steps)