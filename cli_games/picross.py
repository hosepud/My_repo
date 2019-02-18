from random import randint
from ansi_colors import *
def make_solved_board(height, width):
    board = []
    for i in range(height):
        row = []
        for j in range(width):            
            row.append(randint(0,1))
        board.append(row)
    return board   

def vert_horiz(board):
    vert = []
    for i in range(len(board)):
        vert.append(curr_line(board[i]))
    horiz =  []
    for i in range(len(board)):
        horiz.append(curr_line(list(map(lambda row: row[i], board))))
    return vert, horiz

def curr_line(line):
    curr = []
    ctr = 0
    for i in line:
        if i == 0 and ctr > 0:
            curr.append(ctr)
            ctr = 0
        elif i == 1:
            ctr +=1
    if ctr>0:
        curr.append(ctr)
    return curr

def elt_colored(i):
    if i == 1:
        return colored(str(i), 'fg_green')
    else:
        return str(i)
            
def print_board(board, vert, horiz):
    def print_row(row):
        for i in range(len(row)):
            print(elt_colored(row[i]), end = " ")
        print('\n', end = " ")
    def print_part_of_vert(part, longest):
        for i in range(longest):
            if i < len(part):
                print(colored(str(part[i]), 'fg_red'), end = " ")
            else:
                print(' ', end = " ")
    longest = 0
    for i in vert:
        if len(i) > longest:
            longest = len(i)
    print_horiz(horiz, longest)
    for i in range(len(board)):
        print_part_of_vert(vert[i], longest)
        print_row(board[i])

def print_horiz(horiz, tab):
    horiz = list(map(lambda x: list(reversed(x)), horiz))
    longest = 0
    for i in horiz:
        if len(i) > longest:
            longest = len(i)
    for i in range(longest-1, -1, -1):
        if i == longest-1:
            print(2*tab*' ', end = " ")
        else:
      	    print((2*tab - 1)*' ', end = " ")
        for j in horiz:
            if i<len(j):
                print(colored(str(j[i]), 'fg_yellow'), end = " ")
            else:
                print(' ', end = " ")
        print('\n', end=" ")

def hide_sol(board):
    b = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[0])):
            row.append(0)
        b.append(row)
    return b

class Picross(object):
    def __init__(self, height, width):
        self.solution = make_solved_board(height, width)
        self.current = hide_sol(self.solution)
        self.vert, self.horiz = vert_horiz(self.solution)
    def __str__(self):
        print_board(self.current, self.vert, self.horiz)
        return ''

    def mutate(self, x, y):
        if self.current[x-1][y-1]:
            self.current[x-1][y-1] = 0
        else:
            self.current[x-1][y-1] = 1
    
    def is_win(self):
        vert, horiz = vert_horiz(self.current)
        for i in range(len(vert)):
            if vert[i] != self.vert[i]:
                return False
        for i in range(len(horiz)):
            if horiz[i] != self.horiz[i]:
                return False
        return True
    
    def solve(self):
        print_board(self.solution, self.vert, self.horiz)
        return

def game():
    height = int(input('Height?: '))
    width = int(input('Width?: '))
    instance = Picross(height, width)
    print(instance)
    while True:
        try:
            x = int(input('row? '))
            y = int(input('column? '))
        except:
            print("Want solution? ")
            if input() in 'yesyYesY':
                instance.solve()
                return
            else:
                continue
        instance.mutate(x,y)
        print(instance)
        if instance.is_win():
            print('Nonogram solved.')
            return

game()
