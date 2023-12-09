import re

input_lines = open("input_ex.txt", "r").read().splitlines()


def is_zero_function(fun):
    for e in fun:
        if e != 0: return False
    return True

# derive a function; fun is a list of length n; returns a list of length n-1
def derive(fun):
    d_fun = []
    for i in range(1, len(fun)):
        d_fun.append(fun[i]-fun[i-1])
    return d_fun

def calculate_derivative_tower(fun):
    d_tow = [fun]
    while not is_zero_function(fun): 
        d_fun = derive(fun)
        d_tow.append(d_fun)
        fun = d_fun
    return d_tow

def extrapolate_tower(tow):
    if(len(tow) == 1):
        tow[0].append(0)
        return
    
    extrapolate_tower(tow[1:])
    tow[0].append(tow[0][-1]+tow[1][-1])

def extrapolate(fun):
    tow = calculate_derivative_tower(fun)
    extrapolate_tower(tow)
    fun.append(tow[0][-1])

sum = 0

# read file
for line in input_lines:
    fun_str = line.split(' ')
    fun = [int(f_s) for f_s in fun_str]
    extrapolate(fun)
    sum += fun[-1]


print(sum)