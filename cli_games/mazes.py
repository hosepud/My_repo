from random import randint, shuffle
from time import sleep
from ansi_colors import *

def cons(a, b):
    return lambda m: m(a,b)

def car(pair):
    return pair(lambda x, y: x)
def cdr(pair):
    return pair(lambda x,y: y)

def print_scheme_list(lst):
    while lst:
        print(car(lst), end = " ")
        lst = cdr(lst)
    return

def scheme_list(val):
    return cons(val, None)

def shuffled(tup):
    new = []
    for i in tup:
        new.append(i)
    shuffle(new)
    return tuple(new)

def make_board(height, width):
    board = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(Cell())
        board.append(row)
    return board

def print_board(board):
    def print_row(row):
        for i in range(len(row)):
            print(row[i], end = " ")
        print('\n', end = " ")
    for i in range(len(board)):
        print_row(board[i])

class Cell(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None

def get_adjacent(coords):
    x = coords[0]
    y = coords[1]
    return [('up',x,y-1),('left',x-1, y),('right',x+1, y),('down',x, y+1)]

def break_wall(coords1, coords2, direction, board):
    dirs = {'left':'right', 'right':'left', 'up':'down', 'down':'up'}
    c1 = get_cell(coords1, board)
    c2 = get_cell(coords2, board)
    c1.__dict__[direction] = coords2
    c2.__dict__[dirs[direction]] = coords1
    return

def is_valid(coords, board):
    x = coords[0]
    y = coords[1]
    return (x<len(board[0]) and y<len(board)) and (x>-1 and y>-1)
 
def get_cell(coords, board):
    return board[coords[1]][coords[0]]

def DFS_visit(coords, board, visited):
    adj = shuffled(get_adjacent(coords))
    for v in adj:
        v_coords = (v[1], v[2])
        v_dir = v[0]
        if (v_coords not in visited) and is_valid(v_coords, board):                    
            break_wall(coords, v_coords, v_dir, board)    
            visited[v_coords] = coords
            DFS_visit(v_coords, board, visited)

def print_maze(board):
    maze = [[]]
    for i in range(len(board[0])):
        maze[0].append(' ')
        maze[0].append('_')
    maze[0].append('\n')
    for y in range(1,len(board)+1):
        maze.append([])
        for x in range(len(board[0])):
            maze[y].append('|')
            maze[y].append('_')
        maze[y].append('|')
        maze[y].append('\n') 

    for y in range(len(board)):
        for x in range(0, len(board[0])):
            cell = get_cell((x,y), board)
            curr = maze[y+1]
            if cell.left:
                curr[x*2] = ' '
            if cell.down:
                curr[x*2+1] = ' '
    for row in maze:
        print(''.join(row), end = " ")
    print('\n', end = " ")

def solve_DFS(start, end, board, visited):
    cell = get_cell(start, board)
    adj = [cell.left, cell.right, cell.down, cell.up]
    for v in adj:
        if v and (v not in visited):    
            visited[v] = start
            solve_DFS(v, end, board, visited)
    return visited

def make_maze(height, width):
    b = make_board(height, width)
    DFS_visit((0,0), b, {(0, 0):None})
    return b    

def solve(start, end, board):
    v = solve_DFS(start, end, b, {(0,0):None})
    path = scheme_list(end)
    while v[end]:
        path = cons(v[end], path)
        end = v[end]
    print_scheme_list(path)

def print_maze_w_numbers(board):
    maze = [[]]
    for i in range(len(board[0])):
        maze[0].append(' ')
        maze[0].append('_')
    maze[0].append('\n')
    for y in range(1,len(board)+1):
        maze.append([])
        for x in range(len(board[0])):
            maze[y].append('|')
            maze[y].append('_')
        maze[y].append('|')
        maze[y].append('\n') 

    for y in range(len(board)):
        for x in range(0, len(board[0])):
            cell = get_cell((x,y), board)
            curr = maze[y+1]
            if cell.left:
                curr[x*2] = ' '
            if cell.down:
                curr[x*2+1] = ' '
    print('  ', end = " ")
    for i in range(len(board[0])):
        if i%10 == 0 and i > 0:
            print(colored('X', 'fg_red'), end = " ")
        else:
            print(i%10, end = " ")
    print('\n', end = " ")
    ind = '  '
    for i in range(len(maze)):   
        if (i-1)%10 == 0 and i-1 > 0:
            ind = colored('X ', 'fg_red')
        elif i == 0:
            pass
        else:
            ind = str((i-1)%10) + ' '
        print(ind + ''.join(maze[i]), end = " ")
    print('\n', end = " ")

b = make_maze(20,20)
#print_maze(b)
print_maze_w_numbers(b)
solve((0,0), (19,19), b)
