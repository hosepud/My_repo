from random import randint, shuffle
from time import sleep
from ansi_colors import *

def make_sudoku_empty():    
    s = []
    for i in range(9):
        s.append([0]*9)
    return s

def print_2d_arr(s):
    for i in s:
        print(i)
    print('\n', end = " ")
    return

def get_square_boundries(x,y,s):
    while x%3 != 0 or x == 0:
        x+=1
    while y%3 != 0 or y == 0:
        y+=1
    return (y-3, y), (x-3, x)

def is_valid(x,y,s):
    n = s[y][x]
    if n == ' ' or n < 1:
        return False
    row = s[y]
    col = list(map(lambda row: row[x], s))
    for i in range(len(row)):
        if row[i] == n and i != x or row[i] == ' ':
            return False
    for i in range(len(col)):
        if col[i] == n and i != y or col[i] == ' ':
            return False
    y_bnds, x_bnds = get_square_boundries(x,y,s)
    ctr = 0
    for i in range(y_bnds[0], y_bnds[1]):
        for j in range(x_bnds[0], x_bnds[1]):
            if s[i][j] == n and i != y and j != x or s[i][j] == ' ':
                ctr += 1
                if ctr == 2:
                    return False
    return True

def shuffled(arr):
    n = arr[:]
    shuffle(n)
    return n

def is_solved(sudoku):
    for y in range(len(sudoku)):
        for x in range(len(sudoku[0])):
            if not is_valid(x,y,sudoku):
                return False
    return True

def make_sudoku_from_seed():
    seed = [['d', 'a', 'b', 'i', 'g', 'h', 'f', 'e', 'c'],
            ['f', 'h', 'c', 'a', 'b', 'e', 'g', 'i', 'd'],
            ['g', 'i', 'e', 'c', 'f', 'd', 'h', 'a', 'b'],
            ['e', 'b', 'f', 'h', 'd', 'g', 'i', 'c', 'a'],
            ['h', 'g', 'a', 'e', 'i', 'c', 'd', 'b', 'f'],
            ['i', 'c', 'd', 'b', 'a', 'f', 'e', 'g', 'h'],
            ['a', 'd', 'g', 'f', 'c', 'i', 'b', 'h', 'e'],  
            ['b', 'f', 'h', 'g', 'e', 'a', 'c', 'd', 'i'],
            ['c', 'e', 'i', 'd', 'h', 'b', 'a', 'f', 'g']]
    nums = shuffled(list(range(1,10)))
    keys = 'abcdefghi'
    d = {}
    for i in range(len(nums)):
        d[keys[i]] = nums[i]
    for y in range(len(seed)):
        for x in range(len(seed[0])):
            seed[y][x] = d[seed[y][x]]
    return rotated(seed)

def rotated(s):
    new_s = s
    while randint(0,1):
        new_s = []
        for x in range(len(s)):
            new_row = list(map(lambda row :row[x], s))
            new_s.append(new_row)
    return new_s

def poke_holes(solution, level):
    while level > 0:
        x = randint(0,8)
        y = randint(0,8)
        if solution[y][x] != ' ':
            solution[y][x] = ' '
            level -= 1
    return

def print_sudoku(current):
    print(' ', end = " ") 
    for x in range(len(current)):
        if x%3 == 0:
            print(' ', end = " ")
        print(colored(str(x+1),'fg_green'), end = " ")
    print('\n', end = " ")
    for y in range(len(current)):
        if y%3 == 0:
            print('  ' + '-'*25)
            print('', end = " ")
        for x in range(len(current[0])):
            if x == 0:
                print(colored(str(y+1), 'fg_green') + ' |', end = " ")
            print(current[y][x], end = " ")
            if (x+1)%3 == 0:
                print('|', end = " ") 
        print('\n', end = " ")
    print('  ' + '-'*25, end = " ")
    return

class Sudoku(object):
    def __init__(self, level):
        self.solution = make_sudoku_from_seed()
        self.current = [row[:] for row in self.solution]
        poke_holes(self.current, level)

    def is_win(self):
        return is_solved(self.current)

    def mutate(self, x, y, n):
        if n>9 or n<1:
            return
        self.current[x][y] = n
        return
    
    def __str__(self):
        print_sudoku(self.current)                          
        return ''
    
def game():
    numbers = int(input('How many numbers visible? '))
    s = Sudoku(9*9-numbers)
    print(s)
    while True:
        if s.is_win():
            print('Solved correctly.')
            return
        try:
            x = int(input("Row? "))-1
            y = int(input("Column? "))-1
            n = int(input("Number? "))
        except:
            if input("Print solution? ") in 'YESyes':
                print_sudoku(s.solution)
                return
            continue
        s.mutate(x,y,n)
        print(s)   

if __name__ == '__main__':
    game()        

 


