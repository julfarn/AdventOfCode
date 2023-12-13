import itertools

input_lines = open("input_ex.txt").read().splitlines()

x = []
y = []

for r in range(len(input_lines)):
    for c in range(len(input_lines[r])):
        if(input_lines[r][c] == '#'):
            x.append(c)
            y.append(r)
x.sort()
y.sort()

# expand universe
def shiftafter(array, i):
    for j in range(len(array)):
        if(array[j] > i): array[j]+= 1

for c in range(len(input_lines[0])):
    if not len(input_lines[0])-1-c in x:
        shiftafter(x, len(input_lines[0])-1-c)

for r in range(len(input_lines)):
    if not len(input_lines)-1-r in y:
        shiftafter(y, len(input_lines)-1-r) 
        
# get sum of distances
sum_x, sum_y = 0, 0
for i in range(1,len(x)):
    sum_x += i * x[i] - (len(x)) * x[i-1] + i * x[i-1]
    sum_y += i * y[i] - (len(y)) * y[i-1] + i * y[i-1]

print(sum_x + sum_y)
