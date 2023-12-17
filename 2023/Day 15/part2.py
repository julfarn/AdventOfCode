
input_strings = open("F:\\Projekte\\AdventOfCode\\2023\\Day 15\\input.txt").read().replace('\n', '').split(',')

def hash(s):
    cuva = 0
    for c in s:
        cuva += ord(c)
        cuva *= 17
        cuva %= 256
    return cuva

boxes = [[] for i in range(256)]

def i_of_label(box, label):
    for lens_i in range(len(box)):
        if(box[lens_i][0] == label): return lens_i
    return -1

for s in input_strings:
    if("-" in s):
        label = s[:-1]
        box_id = hash(label)
        i = i_of_label(boxes[box_id], label)
        if i>= 0:
            del boxes[box_id][i]
    else:
        s_split = s.split('=')
        label = s_split[0]
        box_id = hash(label)
        val = int(s_split[1])
        i = i_of_label(boxes[box_id], label)
        if i>= 0:
            boxes[box_id][i][1] = val
        else:
            boxes[box_id].append([label, val])

foc_pow_sum = 0
for box_i in range(len(boxes)):
    for lens_i in range(len(boxes[box_i])):
        foc_pow = 1
        foc_pow *= box_i+1
        foc_pow *= lens_i +1
        foc_pow *= boxes[box_i][lens_i][1]

        foc_pow_sum += foc_pow

print(foc_pow_sum)