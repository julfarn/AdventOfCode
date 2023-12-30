import re
input_strings = open("F:\\Projekte\\AdventOfCode\\2023\\Day 17\\input_ex.txt").read().splitlines()

width = len(input_strings[0])
height = len(input_strings)

lossmap = [[int(c) for c in line] for line in input_strings]

# Using A* Algorithm

# heuristic = Manhattan distance
def heuristic(y,x):
    return (height-y) + (width -x) - 2

open_list = [{'x':0, 'y':0, 'g': 0, 'f': width + height-2, 'p': (0,0)}]
closed_list = []

def expand_node(node):
    expansion_candidates = []
    if(node['x'] > 0): expansion_candidates.append((node['y'], node['x']-1))
    if(node['y'] > 0): expansion_candidates.append((node['y']-1, node['x']))
    if(node['x'] < width-1): expansion_candidates.append((node['y'], node['x']+1))
    if(node['y'] < height-1): expansion_candidates.append((node['y']+1, node['x']))

    for cand in expansion_candidates:
        if cand in closed_list: continue # Not true, closed list will also contain weights.
        
        if cand