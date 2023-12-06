import re


input_lines = open("input.txt", "r").read().splitlines()

line_regex = r"Card\s+(?P<card_nr>\d+):\s*(?P<winning_nrs>[\s\d]*)\|(?P<my_nrs>[\s\d]*)"

winning_nrs = []
my_nrs = []
line_nr = 0
points = 0
for line in input_lines:
    m = re.match(line_regex, line)
    card_nr = int(m.group("card_nr"))
    winning_nrs.append([int(nr) for nr in re.split(r"\s+", m.group("winning_nrs").strip())])
    my_nrs.append([int(nr) for nr in re.split(r"\s+", m.group("my_nrs").strip())])
    matches = 0
    for nr in my_nrs[-1]:
        if nr in winning_nrs[-1]:
            matches +=1
    if(matches == 0):
        continue
    points += pow(2,matches-1)

print(points)