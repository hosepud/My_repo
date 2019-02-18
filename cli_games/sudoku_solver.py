from ansi_colors import *
from sys import argv

class Cell(object):
    def __init__(self, coords, domain, sudoku, value=None):
        self.coords = coords
        self.domain = domain[:]
        self.value = value
        self.sudoku = sudoku
    
    def copy(self):
        return Cell(coords, domain, sudoku, value)

    def get_square_boundries(self):
        x = self.coords[0]
        y = self.coords[1]
        if x % 3 == 0:
            x += 3
        else:
            while x%3 != 0:
                x+=1
        if y%3 == 0:
            y+=3
        else:
            while y%3 != 0:
                y+=1
        return (y-3, y), (x-3, x)
    
    def reduce_affecteds(self, val):
        affecteds = self.get_affected()
        for var in affecteds:
            try:
                var.domain.remove(val)
            except:
                pass
        return

    def get_affected(self):
        x = self.coords[0]
        y = self.coords[1]
        s = self.sudoku
        y_bnds, x_bnds = self.get_square_boundries()
        vars_affected = []
        for i in range(y_bnds[0], y_bnds[1]):
            for j in range(x_bnds[0], x_bnds[1]):
                if (j,i) != (x,y):
                        vars_affected.append(s[i][j])
        row = list(filter(lambda x: x != self, s[y]))
        vars_affected += row
        col = list(filter(lambda x: x != self, list(map(lambda row: row[x], s))))
        vars_affected += col
        return vars_affected

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if(self.value):
            return str(self.value)
        else:
            return str(0)

def adj(v, sudoku):
    x = v.coords[0] 
    y = v.coords[1]
    next_states = []
    for val in v.domain:
        new = copy_sudoku(sudoku)
        new[y][x].value = val
        new[y][x].reduce_affecteds(val)
        if not is_invalid(sudoku):
           next_states.append(new)
    return next_states

def is_invalid(sudoku):
    for y in range(9):
        for x in range(9):
            if sudoku[y][x].value is None and sudoku[y][x].domain == []:
                return True
    return False

def copy_sudoku(sudoku):
    new = []
    for y in range(9):
        row = []
        for x in range(9):
            row.append(Cell((x,y), sudoku[y][x].domain, new, sudoku[y][x].value))
        new.append(tuple(row))
    return tuple(new)
    
def make_empty_sudoku():
    s = []
    for y in range(9):
        row = []
        for x in range(9):
            row.append(Cell((x,y), list(range(1,10)), s, None))
        s.append(tuple(row))
    return tuple(s)

def is_solved(sudoku):
    for y in range(9):
        for x in range(9):
            if sudoku[y][x].value == None:
                return False
    return True

def most_constrained(sudoku):
    ans = Cell((10,10), list(range(10)), sudoku, None)
    for y in range(9):
        for x in range(9):
            if len(sudoku[y][x].domain) < len(ans.domain) and sudoku[y][x].value is None:
                ans = sudoku[y][x]
    return ans


def DFS_iter(start):
    S = []
    S.append(start)
    visited = {}
    while S:        
        current = S.pop()
        if is_solved(current):
            return current
        if current not in visited:
            v = most_constrained(current)
            visited[current] = None
            adjacent = adj(v, current)
            for u in adj(v, current):
                if u not in visited:
                    S.append(u)
        
    return

def load_from_file(fname):
    f = open(fname, "r")
    new = []
    grid = []
    row = []
    for i in f.read():
        if not(i in ' \n , \b'):
            row.append(int(i))
        if len(row) == 9:
            grid.append(tuple(row))
            row = []
        if(len(grid) == 9):
            break
    f.close()
    grid = tuple(grid)
    for y in range(9):
        row = []
        for x in range(9):
            if grid[y][x]:
                row.append(Cell((x,y), list(range(1,10)), new, grid[y][x]))
            else:
                row.append(Cell((x,y), list(range(1,10)), new, None))
        new.append(tuple(row))
    for y in range(9):
        for x in range(9):
            if new[y][x].value:
                new[y][x].reduce_affecteds(new[y][x].value)
    return tuple(new)

def make_diabolical():
    grid = []
    new = []
    grid.append((8,0,0,0,0,0,0,0,0))
    grid.append((0,0,3,6,0,0,0,0,0))
    grid.append((0,7,0,0,9,0,2,0,0))
    grid.append((0,5,0,0,0,7,0,0,0))
    grid.append((0,0,0,0,4,5,7,0,0))
    grid.append((0,0,0,1,0,0,0,3,0))
    grid.append((0,0,1,0,0,0,0,6,8))
    grid.append((0,0,8,5,0,0,0,1,0))
    grid.append((0,9,0,0,0,0,4,0,0))
    grid = tuple(grid)
    for y in range(9):
        row = []
        for x in range(9):
            if grid[y][x]:
                row.append(Cell((x,y), list(range(1,10)), new, grid[y][x]))
            else:
                row.append(Cell((x,y), list(range(1,10)), new, None))
        new.append(tuple(row))
    for y in range(9):
        for x in range(9):
            if new[y][x].value:
                new[y][x].reduce_affecteds(new[y][x].value)
    return tuple(new)

def print_sudoku(current):
    print(' ', end = " ") 
    for x in range(len(current)):
        if x%3 == 0:
            print(' ', end = " ")
        print(colored(str(x+1),'fg_green'), end = " ")
    print('\n', end = " ")
    for y in range(len(current)):
        if y%3 == 0:
            print('  ' + '-'*25, end = "\n ")
        for x in range(len(current[0])):
            if x == 0:
                print(colored(str(y+1), 'fg_green') + ' |', end = " ")
            print(current[y][x], end = " ")
            if (x+1)%3 == 0:
                print('|', end = " ")
        print('\n', end = " ")
    print('  ' + '-'*25, end = " ") 
    print('\n', end = " ")
    return
           
if __name__ == "__main__":
	filename = argv[1]
	print(filename, "Loaded with success")
	g = load_from_file(filename)
	print_sudoku(g)
	print("_________________________________________________________\n")
	print_sudoku(DFS_iter(g))

