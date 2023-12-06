import math

number_start = []
number_len = []
number = []

gear_pos = []

input_lines = open("input.txt", "r").read().splitlines()


# Analyze Data
line_nr = 0
for line in input_lines:
    withinNumber = False
    cha_nr = 0
    for cha in line:
        if cha.isdigit():
            if not withinNumber: # A new number has been found
                number_start.append([line_nr, cha_nr])
                number_len.append(1)
                number.append(int(cha))
            else: # Further digits in a number have been found
                number_len[-1] +=1
                number[-1] = number[-1] * 10 + int(cha)
            withinNumber = True
        else:
            withinNumber = False
            if cha == '*':
                # A new gear has been found
                gear_pos.append([line_nr, cha_nr])

        cha_nr += 1
    line_nr += 1



def num_extend_left(num, r, c):
    i= c
    while(True):
        if i==0 or  not(input_lines[r][i-1].isdigit()):
            return num
        num = num + pow(10, c-i +1) * int(input_lines[r][i-1])
        i -= 1

def num_extend_right(num, r, c):
    i= c
    while(True):
        if i==len(input_lines[r])-1 or  not(input_lines[r][i+1].isdigit()):
            return num
        num = num * 10 + int(input_lines[r][i+1])
        i += 1

def gear_ratio (r,c):
    adj_nr = 0
    ratio = 1
    if(is_digit(r,c-1)):
        ratio*= num_extend_left(int(input_lines[r][c-1]),r,c-1)
        adj_nr+= 1
    if(is_digit(r,c+1)):
        ratio*= num_extend_right(int(input_lines[r][c+1]),r,c+1)
        adj_nr+= 1
    if(is_digit(r-1,c)):
        ratio*= num_extend_right(num_extend_left(int(input_lines[r-1][c]),r-1,c), r-1,c)
        adj_nr+= 1
    else:
        if(is_digit(r-1,c-1)):
            ratio*= num_extend_left(int(input_lines[r-1][c-1]),r-1,c-1)
            adj_nr+= 1
        if(is_digit(r-1,c+1)):
            ratio*= num_extend_right(int(input_lines[r-1][c+1]),r-1,c+1)
            adj_nr+= 1
    if(is_digit(r+1,c)):
        ratio*= num_extend_right(num_extend_left(int(input_lines[r+1][c]),r+1,c), r+1,c)
        adj_nr+= 1
    else:
        if(is_digit(r+1,c-1)):
            ratio*= num_extend_left(int(input_lines[r+1][c-1]),r+1,c-1)
            adj_nr+= 1
        if(is_digit(r+1,c+1)):
            ratio*= num_extend_right(int(input_lines[r+1][c+1]),r+1,c+1)
            adj_nr+= 1
    if(adj_nr != 2):
        ratio = 0
    return ratio

def is_digit(r,c):
    if r<0 or c<0 or r>= len(input_lines) or c>= len(input_lines[0]):
        return False
    return input_lines[r][c].isdigit()

def is_symbol(cha):
    return not (cha.isdigit() or cha == '.')

def check_symbol(r,c): # Is there a symbol at coordinates r=row, c=column?
    if r<0 or c<0 or r>= len(input_lines) or c>= len(input_lines[0]):
        return False
    return is_symbol(input_lines[r][c])

def is_part_number (index):
    # Check above and below
    for c in range(number_start[index][1]-1,number_start[index][1] + number_len[index] + 1):
        if check_symbol(number_start[index][0]-1, c) or check_symbol(number_start[index][0]+1, c):
            return True
    # Check left and right
    if check_symbol(number_start[index][0], number_start[index][1]-1) or check_symbol(number_start[index][0], number_start[index][1]+ number_len[index]):
        return True
    
    return False

# Sum up all Part-Numbers
part_sum = 0
for i in range(len(gear_pos)):
    
    part_sum += gear_ratio(gear_pos[i][0], gear_pos[i][1])
    #else:
     #   print(number[i])

print(part_sum)