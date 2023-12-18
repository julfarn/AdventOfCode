
input_strings = open("C:\\Users\\p1ux211\\AoC\\2023\\Day 16\\input.txt").read().splitlines()

x_len = len(input_strings[0])
y_len = len(input_strings)

def reflect(beam,mirror):
    if beam['dir'] == 'n':
        if mirror == '/': beam['dir'] = 'e'
        elif mirror == '\\': beam['dir'] = 'w'
    elif beam['dir'] == 'e':
        if mirror == '/': beam['dir'] = 'n'
        elif mirror == '\\': beam['dir'] = 's'
    elif beam['dir'] == 's':
        if mirror == '/': beam['dir'] = 'w'
        elif mirror == '\\': beam['dir'] = 'e'
    elif beam['dir'] == 'w':
        if mirror == '/': beam['dir'] = 's'
        elif mirror == '\\': beam['dir'] = 'n'

def propagate(beam):
    if beam['dir'] == 'n': beam["y"]-=1
    if beam['dir'] == 's': beam["y"]+=1
    if beam['dir'] == 'e': beam["x"]+=1
    if beam['dir'] == 'w': beam["x"]-=1

def split(beam):
    if beam['dir'] == 'n' or beam['dir'] == 's':
        beam['dir'] = 'e'
        return {'x': beam['x'], 'y': beam['y'], 'dir': 'w'}
    elif beam['dir'] == 'e' or beam['dir'] == 'w':
        beam['dir'] = 'n'
        return {'x': beam['x'], 'y': beam['y'], 'dir': 's'}
    
def kill_condition(beam, e_map):
    # kill a beam if it leaves the map
    if not (0 <= beam['x'] < x_len and 0 <= beam['y'] < y_len):
        return True
    # kill a beam if it hits an energized splitter.
    if e_map[beam['y']][beam['x']] and input_strings[beam['y']][beam['x']] in '-|':
        return True
    return False

def energized_sum(start_beam):
    energized_map = [[False for x in range(x_len)] for y in range(y_len)]
    beams = [start_beam]

    while(len(beams)>0):
        # propagate first
        for beam in beams:
            propagate(beam)
        # kill beams
        beams[:] = [beam for beam in beams if not kill_condition(beam, energized_map)]
        
        # energize, reflect and split
        for beam in beams:
            energized_map[beam['y']][beam['x']] = True
            if input_strings[beam['y']][beam['x']] in '\\/':
                reflect(beam, input_strings[beam['y']][beam['x']])
                continue
            if (input_strings[beam['y']][beam['x']] == '-' and beam['dir'] in 'sn') or (input_strings[beam['y']][beam['x']] == '|' and beam['dir'] in 'ew'):
                beams.append(split(beam))
                #print('A beam was split at (' + str(beam['x']) + ', '+ str(beam['y']) + ').')

    e_sum = 0
    for l in energized_map:
        for e in l:
            if e: e_sum+=1
    return e_sum

max_e_sum = 0
for xstart in range(x_len):
    print('Checking xstart = ' + str(xstart))
    e_sum = energized_sum({'x':xstart, 'y':-1, 'dir': "s"})
    if(e_sum>max_e_sum):
        max_e_sum = e_sum
    e_sum = energized_sum({'x':xstart, 'y':y_len, 'dir': "n"})
    if(e_sum>max_e_sum):
        max_e_sum = e_sum
for ystart in range(y_len):
    print('Checking ystart = ' + str(ystart))
    e_sum = energized_sum({'x':-1, 'y':ystart, 'dir': "e"})
    if(e_sum>max_e_sum):
        max_e_sum = e_sum
    e_sum = energized_sum({'x':x_len, 'y':ystart, 'dir': "w"})
    if(e_sum>max_e_sum):
        max_e_sum = e_sum
print(max_e_sum)
