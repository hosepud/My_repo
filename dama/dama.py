from tkinter import *
from data import *
from PIL import Image, ImageTk

master = Tk()
master.wm_title('dama-game')
master.minsize(width = 630, height = 700)
master.maxsize(width = 630, height = 700)

w = Canvas(master, width = 630, height = 700)
w.pack()
image = Image.open('background.png').resize((700, 700))
photo = ImageTk.PhotoImage(image)
w.create_image(350, 350, image = photo)

gameTitle = Label(master, text = 'DAMA', relief = FLAT)
gameTitle.place(x = 10, y = 650)

currentStatusLabel = Label(master, text = 'red: 0 vs black: 0', relief = FLAT)
currentStatusLabel.place(x = 210, y = 650)

def adjacent(button1, button2):
    coords1 = button1.coords
    coords2 = button2.coords
    if coords1 == coords2:
        return False
    if tuple(coords1 + coords2) in connectedPoints or tuple(coords2 + coords1) in connectedPoints:
        return True
    return False

def update_damalst():
    def isTripleDama(triple):
        for button in triple:
            if button.colors == 'white':
                return False
        return True
    global damalst
    damalst = list(filter(lambda x: isTripleDama(x), damalst))[:]

def safe(button):
    for dama in damalst:
        if button in dama:
            return True
    return False

damalst = []

def dama(b):
    global buttons, damalst
    verticalTriple = [b]
    for button in buttons:
        if b.coords != button.coords:
            if button.colors == b.colors:
                    neighbours = list(filter(lambda x: x.coords[1] == button.coords[1], verticalTriple))
                    if len(neighbours) == len(verticalTriple):
                        verticalTriple.append(button)
    verticalDama = False
    if len(verticalTriple) == 3:
        verticalTriple.sort(key = lambda x: x.coords[0])
        mid = verticalTriple[1]
        left = verticalTriple[0]
        right = verticalTriple[2]
        if adjacent(left, mid) and adjacent(mid, right):
            verticalDama = True
    horizontalTriple = [b]
    for button in buttons:
        if b.coords != button.coords:
            if button.colors == b.colors:
                    neighbours = list(filter(lambda x: x.coords[0] == button.coords[0], horizontalTriple))
                    if len(neighbours) == len(horizontalTriple):
                        horizontalTriple.append(button)

    horizontalDama = False
    if len(horizontalTriple) == 3:
        horizontalTriple.sort(key = lambda x: x.coords[1])
        mid = horizontalTriple[1]
        bottom = horizontalTriple[0]
        top = horizontalTriple[2]
        if adjacent(bottom, mid) and adjacent(mid, top):
            horizontalDama = True
    if verticalDama:
        damalst.append(verticalTriple)
    if horizontalDama:
        damalst.append(horizontalTriple)    
    return horizontalDama or verticalDama

class Player(object):
    def __init__(self, color):
        self.stage = 1
        self.color = color
        self.soldiers = 0
        self.rightToKill = False
        self.put = 0

red = Player('red')
black = Player('black')
currentPlayer = red

currentPlayerLabel = Label(master, text =  currentPlayer.color, relief = FLAT)
currentPlayerLabel.place(x = 110, y = 650)
prevButton = [False, None]

def other_color(color):
    if color == 'red':
        return 'black'
    else:
        return 'red'

class myButton(object):
    def __init__(self, master, xCoord, yCoord):
        self.button = Button(master, relief = FLAT, command = self.callback, bg = 'white', activebackground = 'white', overrelief = SUNKEN)
        self.button.place(x = xCoord, y = yCoord)
        self.colors = 'white'
        self.coords = [xCoord, yCoord]

    def stage_one(self, currentColor):
        global red, black, currentPlayer, prevButton, currentPlayerLabel, currentStatusLabel
        if self.colors == 'white':
            self.button.configure(bg = currentColor, activebackground = currentColor)
            self.colors = currentColor
            currentPlayer.soldiers += 1
            currentPlayer.put += 1
            if currentPlayer.put >= 9:
                currentPlayer.stage = 2
            if dama(self):
                currentPlayer.rightToKill = True
                currentStatusLabel.config(text = currentColor + ' removes an enemy!')
                update_damalst()
                return
            if currentColor == 'red':
                currentPlayer = black
            else:
                currentPlayer = red
            
            currentStatusLabel.config(text = 'red: ' + str(red.soldiers) + ' vs ' + 'black: ' + str(black.soldiers))
            update_damalst()

    def stage_two(self, currentColor):
        global red, black, currentPlayer, prevButton, currentStatusLabel, currentPlayerLabel   
        if not prevButton[0]:
            currentPlayerLabel.config(text = currentColor + '\'s turn')
            if self.colors == currentColor:
                self.colors = 'white'
                self.button.configure(bg = 'white', activebackground = 'white')
                prevButton[0] = True
                prevButton[1] = self
        else:
            if self.coords != prevButton[1].coords and self.colors == 'white' and adjacent(self, prevButton[1]):
                currentPlayerLabel.config(text = other_color(currentColor)  + '\'s turn')
                self.button.configure(bg = currentColor, activebackground = currentColor)
                self.colors = currentColor
                prevButton = [False, None]
                if dama(self):
                    currentPlayer.rightToKill = True
                    currentStatusLabel.config(text = currentColor + ' removes an enemy!')
                    return
                if currentColor == 'red':
                    currentPlayer = black
                else:
                    currentPlayer = red
            elif self.coords == prevButton[1].coords:
                currentPlayerLabel.config(text = currentColor  + '\'s turn')
                self.button.configure(bg = currentColor, activebackground = currentColor)
                self.colors = currentColor
                prevButton = [False, None]
            elif not adjacent(self, prevButton[1]):
                currentPlayerLabel.config(text = currentColor + '\'s turn') 
            elif self.colors != 'white':
                currentPlayerLabel.config(text = currentColor + '\'s turn')               
            else:
                currentPlayerLabel.config(text = currentColor + '\'s turn')
                prevButton = [False, None]
            
            currentStatusLabel.config(text = 'red: ' + str(red.soldiers) + ' vs ' + 'black: ' + str(black.soldiers))
            update_damalst()

    def stage_three(self, currentColor):
        global red, black, currentPlayer, prevButton, currentStatusLabel, currentPlayerLabel            
        if not prevButton[0]:
            currentPlayerLabel.config(text = currentColor + '\'s turn')
            if self.colors == currentColor:
                self.colors = 'white'
                self.button.configure(bg = 'white', activebackground = 'white')
                prevButton[0] = True
                prevButton[1] = self
        else:
            if self.coords != prevButton[1].coords and self.colors == 'white':
                currentPlayerLabel.config(text = other_color(currentColor) + '\'s turn')
                self.button.configure(bg = currentColor, activebackground = currentColor)
                self.colors = currentColor
                prevButton = [False, None]
                if dama(self):
                    currentStatusLabel.config(text = currentColor + ' removes an enemy!')
                    currentPlayer.rightToKill = True
                    return
                if currentColor == 'red':
                    currentPlayer = black
                else:
                    currentPlayer = red
            elif self.coords == prevButton[1].coords:
                currentPlayerLabel.config(text = currentColor + '\'s turn')
                self.button.configure(bg = currentColor, activebackground = currentColor)
                self.colors = currentColor
                prevButton = [False, None]
            elif self.colors != 'white':
                currentPlayerLabel.config(text = currentColor + '\'s turn')               
            else:
                currentPlayerLabel.config(text = currentColor + '\'s turn')
                prevButton = [False, None]
            
            currentStatusLabel.config(text = 'red: ' + str(red.soldiers) + ' vs ' + 'black: ' + str(black.soldiers))
            update_damalst()
        
    def announce_victory(self, color):
        victory = Tk()
        victory.wm_title('GAME OVER')
        victoryLabel = Label(victory, text = color + ' WIN!!!!!', relief = FLAT)
        victoryLabel.pack()
        victory.mainloop()

    def kill(self, currentColor):
        global red, black, currentPlayer, prevButton, currentPlayerLabel, currentStatusLabel, buttons
        potentialVictims = list(filter(lambda x: x.colors == other_color(currentColor), buttons))
        if all([safe(i) for i in potentialVictims]):
            if currentColor == 'red':
                currentPlayer = black
            else:
                currentPlayer = red
            currentStatusLabel.config(text = 'red: ' + str(red.soldiers) + ' vs ' + 'black: ' + str(black.soldiers))
            return
        if self.colors != 'white' and self.colors != currentColor and not safe(self):
            self.button.configure(bg = 'white', activebackground = 'white')
            self.colors = 'white'
            if currentColor == 'red':
                currentPlayer = black
                black.soldiers -= 1 
                if black.soldiers == 3 and black.put >= 9:
                    black.stage = 3
                if black.soldiers == 2 and black.put >= 9:
                    self.announce_victory('RED')
                red.rightToKill = False
            else:
                currentPlayer = red
                red.soldiers -= 1
                if red.soldiers == 3 and red.put >= 9:
                    red.stage = 3
                if red.soldiers == 2 and red.put >= 9:
                    self.announce_victory('BLACK')
                black.rightToKill = False
            currentStatusLabel.config(text = 'red: ' + str(red.soldiers) + ' vs ' + 'black: ' + str(black.soldiers))
            update_damalst()

    def callback(self):
        global red, black, currentPlayer, prevButton, currentPlayerLabel, currentStatusLabel
        if currentPlayer.color == 'red':
            otherPlayer = black
        else:
            otherPlayer = red
        currentColor = currentPlayer.color
        stage = currentPlayer.stage
        right = currentPlayer.rightToKill
        if right:
            self.kill(currentColor)
            currentPlayerLabel.config(text = other_color(currentColor) + '\'s turn')
        else:
            if stage == 1:
                currentPlayerLabel.config(text = other_color(currentColor) + '\'s turn')
                self.stage_one(currentColor)
            if stage == 2:
                self.stage_two(currentColor)
            if stage == 3:
                self.stage_three(currentColor)

def new_game():
    global buttons, red, black, currentPlayer, prevButton, currentPlayerLabel, currentStatusLabel
    red.soldiers = 0
    red.put = 0
    black.soldiers = 0
    black.put = 0   
    currentPlayer = red
    prevButton = [False, None]
    currentStatusLabel.config(text = 'red: ' + str(red.soldiers) + ' vs ' + 'black: ' + str(black.soldiers))
    for mybutton in buttons:
        mybutton.button.configure(bg = 'white', activebackground = 'white')

newGameButton = Button(master, command = new_game, text = 'New game')
newGameButton.place(x = 410, y = 640)    
                                             
buttons = []

def start():
    global buttons
    for coord in pointCoords:
        button = myButton(master, coord[0], coord[1])
        buttons.append(button)
    for coord in lineCoords:
        line = w.create_line(coord, width = '5', fill = 'black')


start()

master.mainloop()
