import re


input_lines = open("input_ex.txt", "r").read().splitlines()
firstline = input_lines[0]
input_lines = input_lines[2:]

firstline_regex = r"seeds:\s+(?P<seed_list>[\s\d]*)"
functiondef_regex = r"(?P<source>[a-z]+)-to-(?P<target>[a-z]+) map:"

class LightningFunction:
    steps = []
    source = "source"
    target = "target"

    def __init__(self, s, t):
        self.source = s
        self.target = t
        self.steps = []

    def add_step(self, start, height, width):
        self.steps.append([start, height, width])
        #self.sort()

    # sort must be called before evaluating.
    def sort(self):
        self.steps.sort(key= lambda step: step[0])
    
    # computes f(x)
    def ev(self, x):
        if(len(self.steps) == 0 or self.steps[0][0] > x):   # Identity function outside of steps
            return x
        for i in range(len(self.steps)):
            if(self.steps[i][0] > x):                       # Identity function outside of steps
                return x
            if (self.steps[i][0] + self.steps[i][2] > x):    # Height of step within a step
                return x+self.steps[i][1]
        return x
 
functions = []   

# Composes functions from the list together to obtain a function from source s to target t, and evaluates composition on x
# Assumes there is only ever one function for a given source.
def evaluate_composed(x, s, t):
    if s== t:
        return x
    f = next(fn for fn in functions if fn.source == s)
    return evaluate_composed(f.ev(x), f.target, t)
    

# Read Seeds
seeds_str =  re.match(firstline_regex, firstline).group("seed_list").split(" ")
seeds = [int(seed) for seed in seeds_str]


# Read Functions from file.
for line in input_lines:
    if len(line) == 0:              # finished a function
        functions[-1].sort()
        continue
    if line[0].isalpha() :          # new function
        m = re.match(functiondef_regex, line)
        functions.append(LightningFunction(m.group("source"), m.group("target")))
        continue              
    # new step
    splits = line.split(" ")
    functions[-1].add_step(int(splits[1]),int(splits[0])-int(splits[1]),int(splits[2])) # in file, target comes before source
functions[-1].sort()

# Get all Location values
locations = [evaluate_composed(seed, "seed", "location") for seed in seeds]
print(min(locations))