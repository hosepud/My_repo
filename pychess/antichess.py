from tkinter import *
from PIL import Image, ImageTk
from os import system
from subprocess import check_output
from time import time

FLIPPED = False
HEIGHT = 720
WIDTH = 900
root = Tk()
root.maxsize(height = HEIGHT, width = WIDTH)
root.minsize(height = HEIGHT, width = WIDTH)
prev = None
adding = None
coordinates = []

nums = {'white_pawn.png':1, 'white_rook.png':5, 'white_knight.png':3, 'white_bishop.png':4, 'white_queen.png':8, 'white_king.png':2, 'black_rook.png':-5, 'black_knight.png':-3, 'black_bishop.png':-4, 'black_queen.png':-8, 'black_king.png':-2, 'black_pawn.png':-1}
class Dummy_move(object):
    def __init__(self):
        self.fr = None
        self.to = None
        self.new_x = None
        self.new_y = None
        self.old_x = None
        self.old_y = None
        self.b = None
    def fill(self, new, old):
        self.fr = old.piece
        self.to = new.piece
        self.new_x = new.x
        self.new_y = new.y
        self.old_x = old.x
        self.old_y = old.y
    
    def __str__(self):
        ret = ''
        attributes = self.__dict__
        for key in attributes:
            if isinstance(attributes[key], int):
                ret += "("+ str(int(attributes[key]/80))+" ,"+str(key) + ")"
            else:
                ret += "("+ str(attributes[key])+" ,"+str(key) + ")"
        return ret
    
LAST_MOVE = Dummy_move()

class Square(object):
    def __init__(self, xCoord, yCoord, color):
        self.square_button = Button(root, height = 5, width = 7, bg = color, command = self.move, activebackground = color)
        self.square_button.place(x = xCoord,y = yCoord)
        self.color = color
        self.x = xCoord
        self.y = yCoord
        self.piece = None
        self.photo = None

    def __repr__(self):
        return str(self.piece) + ' at ' + self.color + ' square'    
    def put_piece_pic(self, piece):
        self.piece = piece
        self.photo = ImageTk.PhotoImage(Image.open(piece))
        self.square_button.configure(image = self.photo, width = 80, height = 80)
    
    def remove_piece_pic(self):
        self.piece = None
        self.photo = None
        self.square_button.configure(image = '', width = 80, height = 80)
        self.square_button.configure(height = 5, width = 7)

    def move(self):
        global prev, adding
        if adding:
            if self.piece:
                self.remove_piece_pic()
            self.put_piece_pic(adding)
            adding = None
            return
        if self.piece is None and prev is None:
            return 
        if prev:
            LAST_MOVE.fill(self, prev)
            piece = prev.piece
            prev.remove_piece_pic()
            prev.square_button.configure(bg = prev.color, activebackground = prev.color)
            if self.piece:
                self.remove_piece_pic()
            self.put_piece_pic(piece)            
            prev = None
        else:
            prev = self
            self.square_button.configure(bg = 'green', activebackground = 'green')
    
    def flip(self):
        self.x = 560 - self.x
        self.y = 560 - self.y
        self.square_button.place(x = self.x,y = self.y)      
        
def draw_squares():
    squares = {} 
    color = False
    for i in range(8):
        for j in range(8):
            if color:
                #black
                squares[j*80, i*80] = Square(j*80, i*80, 'snow4')
            else:
                #white
                squares[j*80, i*80] = Square(j*80, i*80, 'seashell2')
            color = not color
        color = not color
    return squares

def start_position(squares):
    white_pieces = ['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight', 'white_rook']
    black_pieces = ['black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight', 'black_rook']
    vertical = 0
    for piece in white_pieces:
        squares[vertical*80, 560].put_piece_pic(piece+'.png')
        squares[vertical*80, 480].put_piece_pic('white_pawn.png')
        vertical += 1
    vertical = 0
    for piece in black_pieces:
        squares[vertical*80, 0].put_piece_pic(piece+'.png')
        squares[vertical*80, 80].put_piece_pic('black_pawn.png')
        vertical += 1

class Piece_adder(object):
    def __init__(self, piece):
        self.piece = piece
        self.adder_button = Button(root, text = self.piece, command = self.take)
        self.photo = ImageTk.PhotoImage(Image.open(piece))
        self.adder_button.configure(image = self.photo, width = 80, height = 80)
    def take(self):
        global adding
        adding = self.piece
        return

def put_adders():
    horizontal = 0
    for piece in ['white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_pawn']:
        adder = Piece_adder(piece+'.png')
        adder.adder_button.place(x = 700, y = horizontal)
        horizontal += 50
    return

def put_coordinates():
    global coordinates
    xCoord = 20
    for i in 'ABCDEFGH':
        b = Button(root, text = i)
        b.place(x=xCoord, y = 650)
        xCoord+=80
        coordinates.append(b)
    yCoord = 20
    for i in range(8,0,-1):
        b = Button(root, text = str(i))
        b.place(x = 650, y = yCoord)
        coordinates.append(b)
        yCoord+=80
    return

def put_actions():
    flip_button = Button(root, height = 5, width = 10, command = flip, text = "FLIP")
    #flip_button.place(x = 790,y = 80)

    play_AI = Button(root, height = 5, width = 10, command = AI_move, text = "AI", bg='black', fg='white')
    play_AI.place(x = 790, y=480)

    reset = Button(root, height = 5, width = 10, command = reset_board, text = "RESET")
    reset.place(x = 790, y= 170)

def reset_board():
    global FLIPPED
    new_squares = draw_squares()
    start_position(new_squares)
    for x,y in squares:
        squares[x,y] = new_squares[x,y]
    if FLIPPED:
        flip()
        FLIPPED = not FLIPPED

def flip_coordinates():
    global FLIPPED, coordinates
    if not FLIPPED:
        string = "87654321ABCDEFGH"[::-1]  
    else:
        string = "ABCDEFGH87654321"    
    for i in range(len(coordinates)):
        b = coordinates[i]
        b.configure(text = string[i])  
        
def flip():
    global FLIPPED
    flip_coordinates()
    new_squares = {}
    for (x,y) in squares:
        cell = squares[x,y]
        cell.flip()
        new_squares[(560-x, 560-y)] = cell
    for x in range(0, 640, 80):
        for y in range(0, 640, 80):
            squares[x,y] = new_squares[x,y]
    FLIPPED = not FLIPPED

def get_color_name_piece(string):
    temp = {'ro':('Rook', 'R'), 'qu':('Queen', 'Q'), 'pa':('Pawn', 'p'), 'bi':('Bishop', 'B'),
            'kn':('Knight', 'N'), 'ki':('King', 'K')}
    if string[0] == 'w':
        color = 'white'
    else:
        color = 'black'
    for i in range(len(string)):
        if string[i] == '_':
            piece, name = temp[string[i+1] + string[i+2]]
            return color, name, piece

def write_current_board(squares):
    nums = {'white_pawn.png':1, 'white_rook.png':5, 'white_knight.png':3, 'white_bishop.png':4, 'white_queen.png':8, 'white_king.png':2, 'black_rook.png':-5, 'black_knight.png':-3, 'black_bishop.png':-4, 'black_queen.png':-8, 'black_king.png':-2, 'black_pawn.png':-1}
    memo = open("listen.txt", "r")
    if not eval(memo.read()):
        root.after(50, lambda: write_current_board(squares))
        memo.close()
        return
    memo.close()
    new_b = open("current_board.txt", "w")
    for (x,y) in squares:
        cell = squares[x,y]
        x = 560 -x
        y = 560 -y
        if cell.piece:
            value = nums[cell.piece]
            value *= -1
            tbwritten = "%s%s%s\n"%(str(int(x/80)), str(int(y/80)), str(value))     
            new_b.write(tbwritten)
        else:
            tbwritten="%s0\n"%(str(int(x/80))+str(int(y/80)))
            new_b.write(tbwritten)
    new_b.close()
    root.after(50, lambda: write_current_board(squares))

def check_en_passant():
    def is_opposite_pawn(x,y,name):
        return ((x,y) in squares) and squares[x,y].piece and (('pawn' in squares[x,y].piece) and squares[x,y].piece != name)

    message = ''
    if not(('pawn' in LAST_MOVE.fr) and (LAST_MOVE.old_y - LAST_MOVE.new_y == 2*80)):
        return '0'
    else:
        x = LAST_MOVE.new_x
        y = LAST_MOVE.new_y
        name = 'white_pawn.png'
        if LAST_MOVE.fr == 'white_pawn.png':
            name = 'black_pawn.png'    
        if is_opposite_pawn(x, y, name):
            message += str(int(x/80)) + str(int(y/80))
    return message

def stringify_last_move():
    move = ''
    if not(LAST_MOVE.fr in nums):
        return '0000'
    name = nums[LAST_MOVE.fr]
    if name < 0:
        name *= -1
    move += (str(name) + str(7-int(LAST_MOVE.new_x/80))
            +str(7-int(LAST_MOVE.new_y/80))+str(7-int(LAST_MOVE.old_y/80)))
    return move

def make_AI_move(move):
    global prev, nums
    reverse_nums = {}
    for key in nums:
        reverse_nums[nums[key]] = key
    print(move, str(move))
    move = str(move)[2:len(str(move))-1]
    print(move)
    AI_MOVE = (move.split(','))[1:]
    if len(AI_MOVE) == 4:
        x,y,new_x,new_y = [(560 - int(i)*80) for i in AI_MOVE]
        prev = squares[x,y]       
        squares[new_x,new_y].move()
    elif AI_MOVE[-1] == '7':
        x,y,new_x,new_y, foo = [(560 - int(i)*80) for i in AI_MOVE]
        prev = squares[x,y]       
        squares[new_x,new_y].move()
        squares[new_x, new_y-80].remove_piece_pic()        
    else:
        x,y,new_x,new_y,foo = [(560 - int(i)*80) for i in AI_MOVE]
        new_piece = int(AI_MOVE[4])
        if not FLIPPED:
            new_piece *= -1
        prev = squares[x,y]
        squares[new_x, new_y].move()
        squares[new_x, new_y].remove_piece_pic()
        squares[new_x, new_y].put_piece_pic(reverse_nums[new_piece]) 

def AI_move():
    global AI_MOVE, prev, nums
    b = stringify_board()
    start = time()
    AI_MOVE = str(check_output(["./IDalpha_beta", b, '3', stringify_last_move()]))
    make_AI_move(AI_MOVE)
    print("depth = ", (AI_MOVE.split(','))[0])
    print("It took: ", time() - start, " seconds.\n")

def stringify_board():
    global nums
    new_b = ''
    for (x,y) in squares:
        cell = squares[x,y]
        x = 560-x
        y = 560-y
        if cell.piece:
            value = nums[cell.piece]
            if not FLIPPED:
                value *= -1
            tbwritten = "%s%s%sA"%(str(int(x/80)), str(int(y/80)), str(value))     
            new_b += (tbwritten)
        else:
            tbwritten="%s0A"%(str(int(x/80))+str(int(y/80)))
            new_b += (tbwritten)
    return new_b
           
if __name__ == '__main__':        
    root.bind('<space>', lambda event: AI_move())
    squares = draw_squares()
    start_position(squares)
    put_adders()
    put_actions()
    put_coordinates()
    root.mainloop()
