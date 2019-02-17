from tkinter import *
from random import randint
from time import sleep

root = Tk()
root.config(bg = 'black')
root.wm_title('tetris')
SQUARE_SIDE = 28
SCREEN_HEIGHT = 504
SCREEN_WIDTH = 280
root.minsize(width = SCREEN_WIDTH + 100, height = SCREEN_HEIGHT)
root.maxsize(width = SCREEN_WIDTH + 100, height = SCREEN_HEIGHT)
w = Canvas(root, width = SCREEN_WIDTH + 100, height = SCREEN_HEIGHT, bg = 'black')
w.pack()
w.create_line(SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill = 'white')


score = 0
scoreLabel = Label(root, text = "Lines: " + str(score))
scoreLabel.place(x = 280, y = 0)
taken = {}
current = None
level = 150

def change_state(element, newCoords, color, state):
    for i in element.members:
        i.destroy()
    element.members = []
    for coord in newCoords:
        element.members.append(Square(coord[0], coord[1], color))
    element.state = state    

class Square(object):
    def __init__(self, newX, newY, color = 'white'):
        self.squareButton = Button(root, bg = color, activebackground = color, highlightbackground = 'grey')
        self.squareButton.place(x=newX, y=newY)
        self.x = newX
        self.y = newY
        self.alive = True
    def move(self, x, y):
        if self.alive:
            self.x = x
            self.y = y
            self.squareButton.place(x = self.x, y = self.y)
    
    def destroy(self):
        self.squareButton.destroy()
        self.alive = False

    def __nonzero__(self):
        return self.alive

class Yellow(object):
    def __init__(self):
        self.state = 1
        self.members = []
        for x in range(3, 6):
            self.members.append(Square(x*SQUARE_SIDE, 0, 'yellow'))
        self.members.append(Square(4*SQUARE_SIDE, SQUARE_SIDE, 'yellow'))

    def state_one(self):
        members = self.members
        x = self.members[1].x
        newCoords = [(x, members[1].y-SQUARE_SIDE), (x, members[1].y), (x, members[1].y + SQUARE_SIDE), (x - SQUARE_SIDE, members[1].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'yellow', 2)

    def state_two(self):
        members = self.members
        y = members[-1].y
        xLst = [members[-1].x, members[0].x, members[0].x+SQUARE_SIDE]
        newCoords = [(members[-1].x, y), (members[0].x, y), (members[0].x+SQUARE_SIDE,y), (members[0].x, y-SQUARE_SIDE)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'yellow', 3)  

    def state_three(self):
        members = self.members
        newCoords = [(members[3].x, members[3].y), (members[1].x, members[1].y), (members[1].x, members[1].y + SQUARE_SIDE), (members[2].x, members[2].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'yellow', 4)

    def state_four(self):
        members = self.members
        newCoords = [(members[1].x - SQUARE_SIDE, members[1].y), (members[1].x, members[1].y), (members[2].x, members[2].y), (members[3].x, members[3].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'yellow', 1)

    def next_state(self):   
        if self.state == 1:
            self.state_one()    
        elif self.state == 2:
            self.state_two()
        elif self.state == 3:
            self.state_three()
        else:
            self.state_four()

class Orange(object):
    def __init__(self):
        self.state = 1
        self.members = []
        for x in range(3, 7):
            self.members.append(Square(x*SQUARE_SIDE, 0, 'orange'))

    def next_state(self):
        members = self.members
        if self.state == 1:
            newCoords = [(members[1].x, members[1].y-SQUARE_SIDE), 
                            (members[1].x, members[1].y),
                            (members[1].x, members[1].y + SQUARE_SIDE), 
                            (members[1].x, members[1].y + 2*SQUARE_SIDE)]
            if is_invalid_move(newCoords):
                return
            change_state(self, newCoords, 'orange', 2) 
        else:
            newCoords = [(members[1].x - SQUARE_SIDE, members[1].y), 
                            (members[1].x, members[1].y),
                            (members[1].x + SQUARE_SIDE, members[1].y), 
                            (members[1].x + 2*SQUARE_SIDE, members[1].y)]
            if is_invalid_move(newCoords):
                return            
            change_state(self, newCoords, 'orange', 1) 

class Red(object):
    def __init__(self):
        self.state = 1
        self.members = []
        for x in range(4, 6):
            self.members.append(Square(x*SQUARE_SIDE, 0, 'red'))
            self.members.append(Square(x*SQUARE_SIDE, SQUARE_SIDE, 'red'))

    def next_state(self):
        pass

class Cyan(object):
    def __init__(self):
        self.state = 1
        self.members = []
        for x in range(4, 6):
            self.members.append(Square(x*SQUARE_SIDE, 0, 'cyan'))
            self.members.append(Square(x*SQUARE_SIDE - SQUARE_SIDE, SQUARE_SIDE, 'cyan'))

    def state_one(self):
        newCoords = [(self.members[0].x, self.members[0].y - SQUARE_SIDE), (self.members[0].x, self.members[0].y), (self.members[0].x+SQUARE_SIDE, self.members[0].y), (self.members[0].x+SQUARE_SIDE, self.members[0].y + SQUARE_SIDE)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'cyan', 2) 
            
    def state_two(self):                  #1                            #3                          
        newCoords = [(self.members[1].x, self.members[1].y), (self.members[1].x - SQUARE_SIDE, self.members[1].y + SQUARE_SIDE), (self.members[0].x + SQUARE_SIDE, self.members[0].y+SQUARE_SIDE), (self.members[1].x, self.members[1].y + SQUARE_SIDE)]
                                                                      #2
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'cyan', 1) 

    def next_state(self):
        if self.state == 1:
            self.state_one()
        else:
            self.state_two()

class Purple(object):
    def __init__(self):
        self.state = 1
        self.members = []
        for x in range(3,6):
            self.members.append(Square(x*SQUARE_SIDE, 0, 'purple'))
        self.members.append(Square(x*SQUARE_SIDE, SQUARE_SIDE, 'purple'))
    
    def state_one(self):
        members = self.members
        newCoords = [(members[0].x + SQUARE_SIDE, members[0].y - SQUARE_SIDE),
                    (members[1].x, members[1].y),
                    (members[2].x - SQUARE_SIDE, members[2].y + SQUARE_SIDE),
                    (members[3].x - 2*SQUARE_SIDE, members[3].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'purple', 2)

    def state_two(self):
        members = self.members
        newCoords = [(members[0].x+SQUARE_SIDE, members[0].y + 2*SQUARE_SIDE),
                     (members[1].x, members[1].y + SQUARE_SIDE),
                     (members[2].x - SQUARE_SIDE, members[2].y),
                     (members[3].x, members[3].y - SQUARE_SIDE)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'purple', 3)

    def state_three(self):
        members = self.members
        newCoords = [(members[0].x - SQUARE_SIDE, members[0].y - SQUARE_SIDE), (members[1].x, members[1].y), (members[2].x + SQUARE_SIDE, members[2].y + SQUARE_SIDE), (members[3].x + 2*SQUARE_SIDE, members[3].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'purple', 4)
    
    def state_four(self):
        members = self.members
        newCoords = [(members[1].x - SQUARE_SIDE, members[3].y), (members[1].x, members[3].y), (members[1].x + SQUARE_SIDE, members[3].y),
(members[1].x + SQUARE_SIDE, members[1].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'purple', 1)
 
    def next_state(self):
        if self.state == 1:
            self.state_one()
        elif self.state == 2:
            self.state_two()
        elif self.state == 3:
            self.state_three()
        else:
            self.state_four()

class Blue(object):
    def __init__(self):
        self.state = 1
        self.members = []
        for x in range(3,6):
            self.members.append(Square(x*SQUARE_SIDE, 0, 'blue'))
        self.members.append(Square(3*SQUARE_SIDE, SQUARE_SIDE, 'blue'))
    
    def state_one(self):
        members = self.members
        newCoords = [(members[0].x + SQUARE_SIDE, members[0].y), (members[1].x, members[1].y + SQUARE_SIDE),
        (members[2].x - SQUARE_SIDE, members[2].y + 2*SQUARE_SIDE), (members[3].x, members[3].y - SQUARE_SIDE)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'blue', 2)
    
    def state_two(self):
        members = self.members
        newCoords = [(members[0].x - SQUARE_SIDE, members[0].y + SQUARE_SIDE), (members[1].x, members[1].y), (members[2].x + SQUARE_SIDE, members[2].y - SQUARE_SIDE),
                        (members[3].x + 2*SQUARE_SIDE, members[3].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'blue', 3)
    
    def state_three(self):
        members = self.members
        newCoords = [(members[0].x + SQUARE_SIDE, members[0].y - SQUARE_SIDE), 
                    (members[1].x, members[1].y), (members[2].x - SQUARE_SIDE, members[2].y+SQUARE_SIDE), 
                    (members[3].x, members[3].y+2*SQUARE_SIDE)]      
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'blue', 4)

    def state_four(self):
        members = self.members  
        newCoords = [(members[0].x - SQUARE_SIDE, members[0].y), (members[1].x, members[1].y - SQUARE_SIDE),
                        (members[2].x + SQUARE_SIDE, members[2].y - 2*SQUARE_SIDE), (members[3].x - 2*SQUARE_SIDE, members[3].y - SQUARE_SIDE)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'blue', 1)

    def next_state(self):
        if self.state == 1:
            self.state_one()
        elif self.state == 2:
            self.state_two()
        elif self.state == 3:
            self.state_three()
        else:
            self.state_four()

class Green(object):
    def __init__(self):
        self.state = 1
        self.members = []
        for x in range(3,5):
            self.members.append(Square(x*SQUARE_SIDE, 0, 'green'))
            self.members.append(Square(x*SQUARE_SIDE + SQUARE_SIDE, SQUARE_SIDE, 'green'))

    def state_one(self):
        members = self.members
        newCoords = [(members[0].x + 2*SQUARE_SIDE, members[0].y - SQUARE_SIDE), (members[1].x + SQUARE_SIDE, members[1].y - SQUARE_SIDE),
                     (members[2].x, members[2].y), (members[3].x-SQUARE_SIDE, members[3].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'green', 2)
    
    def state_two(self):
        members = self.members
        newCoords = [(members[0].x - 2*SQUARE_SIDE, members[0].y + SQUARE_SIDE), (members[1].x - SQUARE_SIDE, members[1].y + SQUARE_SIDE),
                     (members[2].x, members[2].y), (members[3].x + SQUARE_SIDE, members[3].y)]
        if is_invalid_move(newCoords):
            return
        change_state(self, newCoords, 'green', 1)

    def next_state(self):
        if self.state == 1:
            self.state_one()
        else:
            self.state_two()

def is_invalid_move(coords):
    for coord in coords:
        if (coord in taken and taken[coord]) or (coord[0] >= SCREEN_WIDTH or coord[0] < 0) or coord[1] >= SCREEN_HEIGHT:
            return True
    return False

def is_valid(members):
    return all([i[0] < SCREEN_WIDTH and i[0] >= 0 for i in members]) and all([i[1] < SCREEN_HEIGHT for i in members])

def left(element):
    newCoords = [(i.x - SQUARE_SIDE, i.y) for i in element.members]
    if is_invalid_move(newCoords):
        return
    for member in element.members:
        member.move(member.x-SQUARE_SIDE, member.y)

def right(element):
    newCoords = [(i.x + SQUARE_SIDE, i.y) for i in element.members]
    if is_invalid_move(newCoords):
        return
    for member in element.members:
        member.move(member.x+SQUARE_SIDE, member.y)

def up(element):
    return element.next_state()

def down(element):
    newCoords = []
    if is_round_over():
        make_new()        
        clear_lines()    
        return
    for member in element.members:
        newCoords.append((member.x, member.y + SQUARE_SIDE))
    if is_invalid_move(newCoords):
        return
    else:
        for member in element.members:
            member.move(member.x, member.y + SQUARE_SIDE)

def is_round_over():
    global current
    for member in current.members:
        if ((member.x, member.y + SQUARE_SIDE) in taken and taken[member.x, member.y + SQUARE_SIDE]) or (member.y + SQUARE_SIDE >= SCREEN_HEIGHT):
            return True
    return False

def kill_line(line):
    for x, y in line:
        taken[x,y].destroy()
        taken[x,y] = None

def lower_taken(y):
    global taken
    taken_arr = []
    for key in taken:
        if taken[key]:
            taken_arr.append((key, taken[key]))
    new_taken = {}
    for key, square in taken_arr:
        if key[1] <= y:
            new_taken[key[0], key[1] + SQUARE_SIDE] = square
            square.move(key[0], key[1] + SQUARE_SIDE)
        else:
            new_taken[key] = square
    taken = new_taken
    clear_lines()
        
def clear_lines():
    global score
    y_heights = [i*SQUARE_SIDE for i in range(int(SCREEN_HEIGHT/SQUARE_SIDE))[::-1]]
    x_widths = [i*SQUARE_SIDE for i in range(int(SCREEN_WIDTH/SQUARE_SIDE))]
    for y in y_heights:
        line = []
        for x in x_widths:
            if (x, y) in taken and taken[x, y]:
                line.append((x, y))
        if len(line) == int(SCREEN_WIDTH/SQUARE_SIDE):
            score += 1
            scoreLabel.configure(text = "Lines: " + str(score))
            kill_line(line)
            lower_taken(y)
  
def drop():
    while not is_round_over():
        down(current)
    make_new()
    clear_lines()

def task():
    down(current)
    root.after(level,task)  
       
def make_new():
    global current
    if current:
        for member in current.members:
            taken[member.x, member.y] = member
    current = currents[randint(0,len(currents))-1]()
    if is_game_over(current):
        for i in current.members:
            i.destroy()
        print("Score: %d" %score)
        new_game()  
  
def is_game_over(element):
    for member in element.members:
        if (member.x, member.y) in taken and taken[member.x,member.y]:
            return True
    return False

def new_game():
    global taken, score, current
    for key in taken:
        taken[key].destroy()
    taken = {}
    score = 0
    scoreLabel.configure(text = 'Lines: '+ str(score))
    current = currents[randint(0, len(currents))-1]()

currents = [Orange, Yellow, Red, Cyan, Purple, Blue, Green]
make_new()
root.bind("<Left>", lambda event: left(current))     
root.bind("<Right>", lambda event: right(current))   
root.bind("<Up>", lambda event: up(current))
root.bind("<Down>", lambda event: down(current))
root.bind("<space>", lambda event: drop())
root.after(level, task)
root.mainloop()

