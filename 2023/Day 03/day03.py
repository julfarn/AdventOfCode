
number_start = []
number_len = []
number = []

symbol_pos = []

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
            if cha != '.':
                # A new symbol has been found
                symbol_pos.append([line_nr, cha_nr])

        cha_nr += 1
    line_nr += 1

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
for i in range(len(number)):
    if is_part_number(i):
        part_sum += number[i]
    #else:
     #   print(number[i])

print(part_sum)