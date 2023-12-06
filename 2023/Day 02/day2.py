import re

maximum ={}
maximum["red"] = 12
maximum["green"] = 13
maximum["blue"] = 14

input_lines = open("input.txt", "r").readlines()


possible_id_sum = 0

for line in input_lines:
    is_possible = True

    this_id = int(line.split(":")[0][5:])

    entries = re.split('; |, ', line.split(": ")[1][0:-1])
    pairs = [e.split(" ") for e in entries]

    for count,color in pairs:
        if int(count) > maximum[color]:
            is_possible = False
            break

    if is_possible:
        possible_id_sum += this_id

print(str(possible_id_sum))