
input_lines = open("F:\\Projekte\\AdventOfCode\\2023\\Day 14\\input.txt").read().splitlines()

xlen = len(input_lines[0])
ylen = len(input_lines)
# walls:
wall_pos = [{"x": i, "y": -1} for i in range(xlen)]
wall_pos += [{"x": i, "y": ylen} for i in range(xlen)]
wall_pos += [{"x": -1, "y": i} for i in range(ylen)]
wall_pos += [{"x": xlen, "y": i} for i in range(ylen)]

load_sums = []

for y in range(ylen):
    wall_pos += [{"x": x, "y": y} for x in range(xlen) if input_lines[y][x] == '#']

def count_rocks_below(wall_element):
    global xlen, ylen, input_lines
    ret = 0
    if  wall_element["x"] < 0 or wall_element["x"] >= xlen: 
        wall_element["rcount"] = 0
        return 0
    for i in range(wall_element["y"] + 1, ylen):
        if(input_lines[i][wall_element["x"]] == '#'): break
        if(input_lines[i][wall_element["x"]] == 'O'): ret += 1
    wall_element["rcount"] = ret
    return ret

def load_rocks_below(wall_element):
    c = wall_element["rcount"]
    return c* (ylen - wall_element["y"]) - (c*(c+1))//2

def load_rocks_left(wall_element):
    c = wall_element["rcount"]
    return c* (ylen - wall_element["y"])

def rotate_cw():
    global wall_pos, xlen, ylen
    wall_pos_new = [{"x": ylen - 1 - we["y"], "y": we["x"], "rcount": we["rcount"]} for we in wall_pos]
    wall_pos = wall_pos_new
    tmp = xlen
    xlen = ylen
    ylen = tmp
    
def generate():
    global input_lines, xlen, ylen, wall_pos
    input_lines = ['.' * xlen for y in range(ylen)]
    for we in wall_pos:
        # add 'OOO#' 
        if we["y"] < 0 or we["y"] >= ylen or we["x"] < 0: continue
        input_lines[we["y"]] = input_lines[we["y"]][:we["x"] - we["rcount"]] + ('O' * we["rcount"]) + ('#' if  we["x"]< xlen else '')  +  input_lines[we["y"]][we["x"]+1:]

def cycle():
    global wall_pos
    for i in range(4):
        for we in wall_pos:
            count_rocks_below(we)
        rotate_cw()
        generate()
    #print(*input_lines, sep="\n")
    #print (" ")
    load_sums.append(get_load())

def get_load():
    global wall_pos
    load_sum = 0
    for wall_element in wall_pos:
        load_sum += load_rocks_left(wall_element)
    return load_sum

itr = 0
candidate_periods = []
found = False
while(True):
    cycle()
    itr += 1
    #if(itr < 100): continue

    #print("Iteration " + str(itr))

    for secondtest_period in candidate_periods:
        if(load_sums[-1] == load_sums[-1-secondtest_period]):
            # strong suspicion!
            print("Strong suspicion for period " + str(secondtest_period))
            remember_data = "\n".join(input_lines)
            for i in range(secondtest_period):
                cycle()
                itr += 1
            compare_data = "\n".join(input_lines)
            if(remember_data == compare_data):
                # Periodicity found!
                print("Period " + str(secondtest_period) + " found after " + str(itr) + " iterations.")
                # Print 1000000000'th sum.
                cyc_pos = (1000000000-itr) % secondtest_period
                print("Result: " + str(load_sums[itr-secondtest_period + cyc_pos-1]))
                found = True
                break
    if found: break

    candidate_periods = []
    for test_period in range(1,itr//10):
        if(itr % test_period != 0): continue
        if(load_sums[-1] == load_sums[-1-test_period]):
            candidate_periods.append(test_period)
            print("Candidate period: " + str(test_period))

