import re
import math


input_lines = open("input.txt", "r").read().splitlines()

time_line_regex = r"Time:\s+(?P<time_list>[\s\d]*)"
distance_line_regex = r"Distance:\s+(?P<dist_list>[\s\d]*)"

def winning_bounds(t_max,d_prev):
    d_prev+=1
    lower = math.ceil(0.5 * (t_max - math.sqrt(t_max*t_max - 4.0 * d_prev)))
    upper = math.floor(0.5 * (t_max + math.sqrt(t_max*t_max - 4.0 * d_prev)))
    return [lower, upper]
    

# Read File
time_str =  re.sub('\s+', ' ', re.match(time_line_regex, input_lines[0]).group("time_list")).split(" ")
times = [int(t) for t in time_str]
dist_str =  re.sub('\s+', ' ', re.match(distance_line_regex, input_lines[1]).group("dist_list")).split(" ")
dists = [int(d) for d in dist_str]

possible_wins = 1
for i in range(len(times)):
    bounds = winning_bounds(times[i], dists[i])
    possible_wins *= bounds[1]-bounds[0]+1

print(possible_wins)