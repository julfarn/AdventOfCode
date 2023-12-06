import re

maximum ={}
maximum["red"] = 12
maximum["green"] = 13
maximum["blue"] = 14

input_lines = open("input.txt", "r").readlines()


power_sum = 0

for line in input_lines:
    is_possible = True

    this_id = int(line.split(":")[0][5:])

    entries = re.split('; |, ', line.split(": ")[1][0:-1])
    pairs = [e.split(" ") for e in entries]

    local_maximum = {"red" : 0, "green":0, "blue":0}

    for count,color in pairs:
        if int(count) > local_maximum[color]:
            local_maximum[color] = int(count)
    
    power = local_maximum["red"] * local_maximum["green"] * local_maximum["blue"]

    if is_possible:
        power_sum += power

print(str(power_sum))