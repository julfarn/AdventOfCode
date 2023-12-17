
input_strings = open("F:\\Projekte\\AdventOfCode\\2023\\Day 15\\input_ex.txt").read().splitlines()

x_len = len(input_strings[0])
y_len = len(input_strings)

energized_map = [[False for x in range(x_len)] for y in range(y_len)]

beams = [{'x':-1, 'y':0, 'dir': "e"}]

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

while(len(beams)>0):
    # kill a beam if it hits an energized splitter.