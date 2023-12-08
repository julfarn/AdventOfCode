import re
import math

input_lines = open("input.txt", "r").read().splitlines()
directions = input_lines[0] # directions
input_lines = input_lines[2:]

node_regex = r"(?P<node_name>[A-Z]{3}) = \((?P<left_node>[A-Z]{3}), (?P<right_node>[A-Z]{3})\)"

# build the directed graph
digraph = {}
current_nodes = []
for line in input_lines:
    m = re.match(node_regex, line)
    digraph[m.group("node_name")] = {"L": m.group("left_node"), "R": m.group("right_node")}
    if m.group("node_name").endswith('A'):
        current_nodes.append(m.group("node_name"))

# follow the path
steps = [0] * len(current_nodes)
for i in range(len(current_nodes)):
    while(not current_nodes[i].endswith('Z')):
        current_nodes[i] = digraph[current_nodes[i]][directions[steps[i] % len(directions)]]
        steps[i] += 1

mult = steps[0]
for i in range(1, len(current_nodes)):
    mult = math.lcm(mult, steps[i])

print(mult)