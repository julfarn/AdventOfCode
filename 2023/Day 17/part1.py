import heapdict
import time
input_strings = open("F:\\Projekte\\AdventOfCode\\2023\\Day 17\\input_ex.txt").read().splitlines()

width = len(input_strings[0])
height = len(input_strings)
max_streak = 3

nodes = []

# Using A* Algorithm
largenr = 10000000000
open_list = heapdict.heapdict()
closed_list = []

def nodeindex(dir, streak):
    return dir + 4*streak

class node:
    global nodes
    x,y = 0,0
    min_dist_from_start = 0
    estimated_weight = 0
    in_open = False
    in_closed = False
    loss = 0
    is_solution = False
    reachedfrom = -1
    precursor = None

    def reachedfromdir(self):
        return self.reachedfrom % 4

    def streak(self):
        return (self.reachedfrom // 4) +1

    def __init__(self, _x, _y, _loss, _reachedfrom):
        self.y = _y
        self.x = _x
        self.loss = _loss
        self.reachedfrom = _reachedfrom

    # heuristic = Manhattan distance
    def heuristic(self):
        return (height-self.y) + (width -self.x) - 2
    
    def estimate_weight(self):
        self.estimated_weight = self.heuristic() + self.min_dist_from_start
    
    def add_to_open(self):
        self.in_open = True
        open_list[self] = self.estimated_weight
        if self.in_closed:
            closed_list.remove(self)
            self.in_closed = False

    def close(self):
        #l = len(open_list)
        #open_list.remove(self)
        #if(l == len(open_list)):
        #    print('error')
        self.in_open = False
        self.in_closed = True
        closed_list.append(self)

    def can_expand_up(self):
        if(self.y == 0): return False
        if(self.reachedfromdir() == 0): return False
        if(self.reachedfromdir() == 2 and self.streak() == max_streak):
            return False
        return True
    
    def can_expand_down(self):
        if(self.y == height-1): return False
        if(self.reachedfromdir() == 2): return False
        if(self.reachedfromdir() == 0 and self.streak() == max_streak):
            return False
        return True
    
    def can_expand_left(self):
        if(self.x == 0): return False
        if(self.reachedfromdir() == 3): return False
        if(self.reachedfromdir() == 1 and self.streak() == max_streak):
            return False
        return True
    
    def can_expand_right(self):
        if(self.x == width-1): return False
        if(self.reachedfromdir() == 1): return False
        if(self.reachedfromdir() == 3 and self.streak() == max_streak):
            return False
        return True
    
    def set_solution(self):
        self.is_solution = True
        if self.precursor != None:
            self.precursor.set_solution()
    
    def neighbor_i(self, neighborreachedfromdir):
        if(neighborreachedfromdir != self.reachedfromdir()):
            return neighborreachedfromdir
        return self.reachedfrom + 4
    
    def expand(self):
        self.close()
        expansion_candidates = []
        if(self.can_expand_left()): expansion_candidates.append(nodes[self.x-1][self.y][self.neighbor_i(1)])
        if(self.can_expand_up()): expansion_candidates.append(nodes[self.x][self.y-1][self.neighbor_i(2)])
        if(self.can_expand_right()): expansion_candidates.append(nodes[self.x+1][self.y][self.neighbor_i(3)])
        if(self.can_expand_down()): expansion_candidates.append(nodes[self.x][self.y+1][self.neighbor_i(0)])

        for cand in expansion_candidates:
            if cand.in_closed: continue
            
            if cand.in_open:
                if cand.min_dist_from_start > self.min_dist_from_start + cand.loss:
                    cand.min_dist_from_start = self.min_dist_from_start + cand.loss
                    cand.estimate_weight()
                    open_list[cand] = cand.estimated_weight
                    cand.precursor = self
                continue
            
            cand.min_dist_from_start = self.min_dist_from_start + cand.loss
            cand.estimate_weight()
            cand.add_to_open()
            cand.precursor = self
            

nodes = [[[node(x,y, int(input_strings[y][x]), rf) for rf in range(4*(max_streak))] for y in range(height)] for x in range(width)]
start_node = node(0,0, int(input_strings[0][0]), -4)
nodes[0][0].append(start_node)
end_nodes = nodes[width-1][height-1]
start_node.add_to_open()

def print_status():
    for y in range(height):
        line = ''
        for x in range(width):
            interesting = False
            for rf in range(4*(max_streak)):
                if(nodes[x][y][rf].is_solution): 
                    line += 'o'
                    interesting = True
                    break
                #if(nodes[x][y][rf].in_open): 
                #    line += '*'
                #    interesting = True
                #    break
            if not interesting: line += str(nodes[x][y][rf].loss)
        print(line)
    print(' ')
    time.sleep(0.1)

def astar():
    while len(open_list) > 0:
        curr_node, estweight = open_list.popitem()

        if(curr_node in end_nodes): break

        curr_node.expand()
        #print_status()
        print("Best weight estimate: " + str(estweight))
    curr_node.set_solution()
    return curr_node

end_node = astar()

print_status()

print(end_node.min_dist_from_start)