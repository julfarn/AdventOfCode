import re

input_lines = open("input.txt", "r").read().splitlines()
directions = input_lines[0] # directions
input_lines = input_lines[2:]

node_regex = r"(?P<node_name>[A-Z]{3}) = \((?P<left_node>[A-Z]{3}), (?P<right_node>[A-Z]{3})\)"

# build the directed graph
digraph = {}
for line in input_lines:
    m = re.match(node_regex, line)
    digraph[m.group("node_name")] = {"L": m.group("left_node"), "R": m.group("right_node")}

# follow the path
current_node = "AAA"
step = 0
while(current_node != "ZZZ"):
    current_node = digraph[current_node][directions[step % len(directions)]]
    step += 1

print(step)