import re
import time
input_strings = open("F:\\Projekte\\AdventOfCode\\2023\\Day 17\\input_ex.txt").read().splitlines()

width = len(input_strings[0])
height = len(input_strings)

nodes = []

# Using A* Algorithm

open_list = []
closed_list = []
class node:
    global nodes
    x,y = 0,0
    min_dist_from_start = 0
    estimated_weight = 0
    precursor = None
    in_open = False
    in_closed = False
    loss = 0

    def __init__(self, _x, _y, _loss):
        self.y = _y
        self.x = _x
        self.loss = _loss

    # heuristic = Manhattan distance
    def heuristic(self):
        return (height-self.y) + (width -self.x) - 2
    
    def estimate_weight(self):
        self.estimated_weight = self.heuristic() + self.min_dist_from_start
    
    def add_to_open(self):
        self.in_open = True
        open_list.append(self)

    def close(self):
        l = len(open_list)
        open_list.remove(self)
        if(l == len(open_list)):
            print('error')
        self.in_open = False
        self.in_closed = True
        closed_list.append(self)

    def can_expand_up(self):
        if(self.y == 0): return False
        if(self.precursor != None 
           and self.precursor.precursor != None 
           and self.precursor.precursor.precursor != None 
           and self.precursor.precursor.precursor.y == self.y+3):
            return False
        return True
    
    def can_expand_down(self):
        if(self.y == height-1): return False
        if(self.precursor != None 
           and self.precursor.precursor != None 
           and self.precursor.precursor.precursor != None 
           and self.precursor.precursor.precursor.y == self.y-3):
            return False
        return True
    
    def can_expand_left(self):
        if(self.x == 0): return False
        if(self.precursor != None 
           and self.precursor.precursor != None 
           and self.precursor.precursor.precursor != None 
           and self.precursor.precursor.precursor.x == self.x+3):
            return False
        return True
    
    def can_expand_right(self):
        if(self.x == width-1): return False
        if(self.precursor != None 
           and self.precursor.precursor != None 
           and self.precursor.precursor.precursor != None 
           and self.precursor.precursor.precursor.x == self.x-3):
            return False
        return True
    
    def expand(self):
        self.close()
        expansion_candidates = []
        if(self.can_expand_left()): expansion_candidates.append(nodes[self.x-1][self.y])
        if(self.can_expand_up()): expansion_candidates.append(nodes[self.x][self.y-1])
        if(self.can_expand_right()): expansion_candidates.append(nodes[self.x+1][self.y])
        if(self.can_expand_down()): expansion_candidates.append(nodes[self.x][self.y+1])

        for cand in expansion_candidates:
            if cand.in_closed: continue
            
            if cand.in_open:
                if cand.min_dist_from_start > self.min_dist_from_start + cand.loss:
                    cand.min_dist_from_start = self.min_dist_from_start + cand.loss
                    cand.precursor = self
                    cand.estimate_weight()
                continue
            
            cand.add_to_open()
            cand.min_dist_from_start = self.min_dist_from_start + cand.loss
            cand.precursor = self
            cand.estimate_weight()
            


nodes = [[node(x,y, int(input_strings[y][x])) for y in range(height)] for x in range(width)]
start_node = nodes[0][0]
end_node = nodes[width-1][height-1]
start_node.add_to_open()

def print_status():
    for y in range(height):
        line = ''
        for x in range(width):
            if(nodes[x][y].in_open): line += '*'
            elif(nodes[x][y].in_closed): line += ' '
            else: line += str(nodes[x][y].loss)
        print(line)
    print(' ')
    time.sleep(0.1)

def astar():
    while len(open_list) >0:
        curr_node = min(open_list, key=lambda n: n.estimated_weight)

        if(curr_node == end_node): return

        curr_node.expand()
        #print_status()

astar()

print(end_node.min_dist_from_start)