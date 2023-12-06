import re


input_lines = open("input.txt", "r").read().splitlines()
firstline = input_lines[0]
input_lines = input_lines[2:]

firstline_regex = r"seeds:\s+(?P<seed_list>[\s\d]*)"
functiondef_regex = r"(?P<source>[a-z]+)-to-(?P<target>[a-z]+) map:"

# Class for piecewise affine functions whose derivative is 1 whereever it exists
class PiecewiseDiagonalFunction:
    steps = [] # List of steps
    # A single step is a list [start, height, width], meaning that
    # in the interval [start, start+width], the function is given by (identity+height)
    source = "source"
    target = "target"

    
    def step_start(self, i):
        return self.steps[i][0]
    def step_height(self, i):
        return self.steps[i][1]
    def step_width(self, i):
        return self.steps[i][2]
    def step_end(self, i):
        return self.step_start(i) + self.step_width(i)
    def step_start_height(self, i):
        return self.step_start(i) + self.step_height(i)
    def step_end_height(self, i):
        return self.step_end(i) + self.step_height(i)

    def __init__(self, s, t):
        self.source = s
        self.target = t
        self.steps = []

    def add_step(self, start, height, width):
        self.steps.append([start, height, width])

    # sort must be called before evaluating.
    def sort(self):
        s = [step for step in self.steps if step[1] != 0]
        self.steps = s
        self.steps.sort(key= lambda step: step[0])
    
    # computes f(x)
    # supposes that steps are sorted!
    def ev(self, x):
        if(len(self.steps) == 0 or self.steps[0][0] > x):   # Identity function outside of steps
            return x
        for i in range(len(self.steps)):
            if(self.steps[i][0] > x):                       # Identity function outside of steps
                return x
            if (self.steps[i][0] + self.steps[i][2] > x):    # Height of step within a step
                return x+self.steps[i][1]
        return x
    
    
    # returns self o f
    def circ(self, f):
        comp = PiecewiseDiagonalFunction(f.source, self.target)

        f_i = 0
        interval_start = 0
        for f_i in range(len(f.steps)):
            # interval before the step
            interval_end = f.step_start(f_i)
            if interval_end > interval_start:
                comp.steps += self.stepchunk(interval_start, interval_end)

            # interval within the step self.steps[this_i][0], self.steps[this_i][1]
            chunk = self.stepchunk(f.step_start_height(f_i), f.step_end_height(f_i))
            for step in chunk:
                comp.add_step(step[0]-f.step_height(f_i), step[1]+f.step_height(f_i), step[2]) # Real composition happening here

            interval_start = f.step_end(f_i)

        # do something in the open interval.
        comp.steps += self.stepchunk_onlysteps(interval_start)

        comp.sort()

        return comp
    
    # returns list of steps in interval [inter_a,inter_b] as a list with entries [pre_a, height, width] (i.e. a step); 
    # also turns gaps into steps
    def stepchunk(self, inter_a, inter_b):
        ret = []
        laststepend = 0
        for i in range(len(self.steps)):
            # check region before step
            if(laststepend<inter_b and self.step_start(i) > inter_a): # any intersection
                tar_a = max(inter_a, laststepend)
                tar_b = min(inter_b, self.step_start(i))
                if(tar_b - tar_a > 0):
                    ret.append([tar_a,0,tar_b-tar_a])

            # check step
            if(self.step_start(i)<inter_b and self.step_end(i) > inter_a): # any intersection
                tar_a = max(inter_a, self.step_start(i))
                tar_b = min(inter_b, self.step_end(i))

                if(tar_b - tar_a > 0):
                    ret.append([tar_a,self.step_height(i),tar_b-tar_a])
            laststepend = self.step_end(i)

        # check region after all steps
        if(laststepend<inter_b):
            tar_a = max(inter_a, laststepend)
            tar_b = inter_b
            if(tar_b - tar_a > 0):
                    ret.append([tar_a,0,tar_b-tar_a])

        return ret
    
    # returns list of ONLY steps in interval [inter_a, infinity] as a list with entries [pre_a, height, width] (i.e. a step); 
    def stepchunk_onlysteps(self, inter_a):
        ret = []
        for i in range(len(self.steps)):
            # check step
            if(self.step_end(i) > inter_a): # any intersection
                tar_a = max(inter_a, self.step_start(i))
                tar_b = self.step_end(i)

                if(tar_b - tar_a > 0):
                    ret.append([tar_a,self.step_height(i),tar_b-tar_a])

        return ret
    
    # returns local minima  within the interval [a,b]
    def local_minima(self, a, b):
        minima = [a]
        prevheight = 0
        prevstepend = -1
        for i in range(len(self.steps)):
            if(self.step_start(i) - prevstepend > 1 and a <= prevstepend < b): # gap before step, if gap exists
                if prevheight>0: # gap start is minimum
                    minima.append(self.step_end(i))
                prevheight = 0

            if(a <= self.step_start(i) < b and self.step_height(i)<prevheight): # minimum of step
                minima.append(self.step_start(i))
            prevstepend = self.step_end(i)
            prevheight = self.step_height(i)

        return minima


 
functions = []   


# Composes functions from the list together to obtain a function from source s to target t
# Assumes there is only ever one function for a given source.
def compose(s, t, fun = None):
    if s== t:
        return fun
    f = next(fn for fn in functions if fn.source == s)
    if(fun == None):
        return compose(f.target, t, fun= f)
    return compose(f.target, t, fun= f.circ(fun))
    

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
        functions.append(PiecewiseDiagonalFunction(m.group("source"), m.group("target")))
        continue              
    # new step
    splits = line.split(" ")
    functions[-1].add_step(int(splits[1]),int(splits[0])-int(splits[1]),int(splits[2])) # in file, target comes before source
functions[-1].sort()


comp = compose("seed", "location")  # Composition of all functions
loc_minima = []
for i in range(int(len(seeds)/2)):      # List of all local minima within the seed ranges
    loc_minima += comp.local_minima(seeds[2*i], seeds[2*i]+seeds[2*i+1])

min_values = [comp.ev(x) for x in loc_minima] # List of the values of all local minima
print(min(min_values)) # Print the value of the absolute minimum within seed ranges