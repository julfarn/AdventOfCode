import heapdict
import time
input_strings = open("F:\\Projekte\\AdventOfCode\\2023\\Day 17\\input_ex.txt").read().splitlines()

width = len(input_strings[0])
height = len(input_strings)
max_streak = 6

nodes = []

# Using A* Algorithm
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
    
    def set_solution(self):
        self.is_solution = True
        if self.precursor != None:
            self.precursor.set_solution()
    
    def neighbor_i(self, neighborreachedfromdir):
        if(neighborreachedfromdir != self.reachedfromdir()):
            return neighborreachedfromdir
        return self.reachedfrom + 4
    
    def get_neighbor(self, dir, dist):
        xdist,ydist = 0,0
        if dir%2 == 0: 
            xdist = 0
            ydist = -(dir-1) * dist
        else:
            ydist = 0
            xdist = -dist if dir == 1 else dist
        
        xpos = self.x + xdist
        ypos = self.y + ydist

        if xpos < 0: return None
        if xpos >= width: return None
        if ypos < 0: return None
        if ypos >= height: return None

        return nodes[xpos][ypos][self.neighbor_i(dir)]
    
    def get_loss(self, dir, dist):
        if dir%2 == 0: 
            xdist = 0
            ydist = -(dir-1) 
        else:
            ydist = 0
            xdist = -1 if dir == 1 else 1

        l = 0
        xpos = self.x
        ypos = self.y
        while dist != 0:
            xpos += xdist
            ypos += ydist
            l += nodes[xpos][ypos][0].loss
            dist -= 1
        return l

    def expand(self):
        self.close()

        for dir in range(3):
            if dir == (self.reachedfromdir() +2) % 4: continue # don't go backwards
            cand = None
            l = 0
            if dir == self.reachedfromdir(): # continue in same direction
                if self.streak() == max_streak: continue # don't go in a straight line for too long
                # follow direction, no streak.
                cand = self.get_neighbor(dir, 1)
                if(cand == None): continue # end of grid
                l = self.get_loss(dir, 1)
            else:
                # change direction
                cand = self.get_neighbor(dir, 4) # immediately take four steps
                if(cand == None): continue # end of grid
                l = self.get_loss(dir, 4)

            if cand.in_closed: continue
            
            if cand.in_open:
                if cand.min_dist_from_start > self.min_dist_from_start + l:
                    cand.min_dist_from_start = self.min_dist_from_start + l
                    cand.estimate_weight()
                    open_list[cand] = cand.estimated_weight
                    cand.precursor = self
                continue
            
            cand.min_dist_from_start = self.min_dist_from_start + l
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
    i= 0
    while True:
        i+=1
        curr_node, estweight = open_list.popitem()

        if(curr_node in end_nodes): break

        curr_node.expand()
        #print_status()
        if i % 1000 == 0:
            print("Best weight estimate: " + str(estweight))
    curr_node.set_solution()
    return curr_node

end_node = astar()

print_status()

print(end_node.min_dist_from_start)