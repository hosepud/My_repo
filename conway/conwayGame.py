from tkinter import *
from time import sleep

root = Tk()
root.wm_title("Life")
root.minsize(width = 500, height = 500)
root.maxsize(width = 500, height = 500)
field = Canvas(root, width = 500, height = 500, bg = 'black')
field.pack()
user_pattern = {}

def create_grid(w):
    for i in range(0, 500, 10):
        w.create_line((i, 0, i, 500), width = '1', fill = 'gray')
        w.create_line((0, i, 500, i), width = '1', fill = 'gray')

def make_alive(w, x, y):
    return w.create_rectangle(x*10 - 10, y*10-10, x*10, y*10, fill = 'white')

def kill_cell(w, cell):
    w.delete(cell)

def choose_cell(event):
    global user_pattern
    x = int(event.x/10)+1
    y = int(event.y/10)+1
    if (x,y) not in user_pattern:
        user_pattern[x,y] = make_alive(field, x, y)

def get_neighbors(x, y):
    neighbors = []
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if (i,j) != (x, y):
                neighbors.append((i, j))    
    return list(filter(isValid, neighbors))

def isValid(pair):
    return (pair[0]>-100 and pair[0]<100) and (pair[1]>-100 and pair[1]<100)

def fate(x, y, neighbors, pattern):
    neighbors = list(filter(lambda pair: pair in pattern, neighbors))
    if (x,y) in pattern:
        return len(neighbors) == 3 or len(neighbors) == 2
    else:
        return len(neighbors) == 3        

def get_new_pattern(pattern):
    newPattern = {}
    surroundingCells = []
    toBeBorn = {}
    for coords in pattern:
        x = coords[0]
        y = coords[1]
        surroundingCells.extend(list(filter(lambda pair: pair not in pattern, get_neighbors(x, y))))
        if fate(x, y, get_neighbors(x,y), pattern):
            toBeBorn[x,y] = None
    surroundingCells = list(set(surroundingCells)) 

    for coords in surroundingCells:
        x = coords[0]
        y = coords[1]
        if fate(x, y, get_neighbors(x, y), pattern):
            toBeBorn[x,y] = None

    for coords in pattern:
        kill_cell(field, pattern[coords])
    toBeBorn = collect_garbage(toBeBorn)

    for cell in toBeBorn:
        newPattern[cell] = make_alive(field, cell[0], cell[1])
    return newPattern

def isVisible(pair):
    return (pair[0]>0 and pair[0]<51) and (pair[1]>0 and pair[1]<51)

def DFS_visit(s, pattern, parent):
    for v in filter(lambda neighbor: neighbor in pattern, get_neighbors(s[0],s[1])):
        if v not in parent:
            parent[v] = s
            DFS_visit(v, pattern, parent)

def print_reachables(parent):
    for key in parent:
        print(key)

def collect_garbage(pattern):
    reachables = []
    for pair in pattern:    
        if isVisible(pair):
            reachables.append(pair)
    parent = {}
    for pair in reachables:
        if pair not in parent:
            parent[pair] = None
            DFS_visit(pair, pattern, parent)
    return parent

def reset_game():
    global user_pattern
    for pair in user_pattern:
        kill_cell(field, user_pattern[pair])
    user_pattern = {}

def next_stage():
    global user_pattern 
    user_pattern = get_new_pattern(user_pattern)

if __name__ == '__main__':
    create_grid(field)
    root.bind('<Return>', lambda event: next_stage())
    root.bind('<Button-1>', choose_cell)
    root.bind('<Escape>', lambda event: reset_game())
    root.mainloop()
    
