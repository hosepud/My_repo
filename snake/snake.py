from tkinter import *
from random import randint
from time import sleep

root = Tk()
root.config(bg = 'black')
root.wm_title('snake')
root.minsize(width = 500, height = 600)
root.maxsize(width = 500, height = 600)
w = Canvas(root, width = 500, height = 600, bg = 'black')
w.pack()
w.create_line(0, 500, 500, 500, fill = 'white')

ctr = 0

score = 0
scoreLabel = Label(root, text = "score: " + str(score))
scoreLabel.place(x = 0, y = 550)
bestScore = 0
bestScoreLabel = Label(root, text = 'Best score: ' + str(bestScore))
bestScoreLabel.place(x = 400, y = 550)
 
def elongate():
    if snake[-1].direction == 'N':
        newMember = Member()
        newMember.memberButton.place(x = snake[-1].x, y = snake[-1].y + 25)
        newMember.x = snake[-1].x
        newMember.y = snake[-1].y + 25
        snake.append(newMember)
        newMember.direction = snake[-1].direction

    if snake[-1].direction == 'S':
        newMember = Member()
        newMember.memberButton.place(x = snake[-1].x, y = snake[-1].y - 25)
        newMember.x = snake[-1].x
        newMember.y = snake[-1].y - 25
        snake.append(newMember)
        newMember.direction = snake[-1].direction
    
    if snake[-1].direction == 'W':
        newMember = Member()
        newMember.memberButton.place(x = snake[-1].x+25, y = snake[-1].y)
        newMember.x = snake[-1].x + 25
        newMember.y = snake[-1].y
        snake.append(newMember)
        newMember.direction = snake[-1].direction
    
    if snake[-1].direction == 'E':
        newMember = Member()
        newMember.memberButton.place(x = snake[-1].x - 25, y = snake[-1].y)
        newMember.x = snake[-1].x - 25
        newMember.y = snake[-1].y
        snake.append(newMember)
        newMember.direction = snake[-1].direction            

def move(member):
    global ctr, score
    if ctr == 1:
        elongate()
    
    ctr -= 1

    if member.direction == 'N':
        member.y = (member.y - 25)%500
        member.memberButton.place(x = member.x, y = member.y) 
 
    if member.direction == 'S':
        member.y = (member.y + 25)%500
        member.memberButton.place(x = member.x, y = member.y) 

    if member.direction == 'E':
        member.x = (member.x + 25)%500
        member.memberButton.place(x = member.x, y = member.y) 
 
    if member.direction == 'W':
        member.x = (member.x - 25)%500
        member.memberButton.place(x = member.x, y = member.y)   

    if member.head:
        if member.x == food.x and member.y == food.y:
            
            ctr = len(snake)
            getNewFood()
            score += 1*5
            scoreLabel.configure(text = "score: " + str(score))

class Member(object):
    def __init__(self, head = False):
        self.memberButton = Button(root, bg = 'red', relief = FLAT, activebackground = 'red')
        self.memberButton.place(x=350, y=350)
        self.x = 350
        self.y = 350
        self.direction = 'N'
        self.head = head
        if head:
            self.memberButton.configure(bg = 'white')

foodLocations = [475, 450, 425, 400, 375, 350, 325, 300, 275, 250, 225, 200, 175, 150, 125, 100, 75, 50, 25, 0]

def getNewFood():
    xCoord = foodLocations[randint(0, len(foodLocations) - 1)]
    yCoord = foodLocations[randint(0, len(foodLocations) - 1)]
    for member in snake:
        if member.x == xCoord and member.y == yCoord:
            return getNewFood()
    food.foodButton.place(x = xCoord, y = yCoord)
    food.x = xCoord
    food.y = yCoord
    
class Food(object):
    def __init__(self):
        self.foodButton = Button(root, bg = 'yellow', relief = FLAT, activebackground = 'yellow')
        self.foodButton.place(x = 350, y = 450)
        self.x = 350
        self.y = 450

def redundantOrWrong(course):
    if course == 'S' and snake[0].direction == 'N':
        return True
    if course == 'W' and snake[0].direction == 'E':
        return True
    if course == 'N' and snake[0].direction == 'S':
        return True
    if course == 'E' and snake[0].direction == 'W':
        return True
    if course == snake[0].direction:
        return True
    
def changeCourse(course):
    global snake, score, bestScore
    if redundantOrWrong(course):
        return
    prev = snake[0].direction
    snake[0].direction = course
    move(snake[0])
    for index in range(1, len(snake)):
        temp = snake[index].direction
        snake[index].direction = prev
        prev = temp
        move(snake[index])    
    if gameOver():
        if score > bestScore:
            bestScore = score
            bestScoreLabel.configure(text = "Best Score: " + str(bestScore))
        print('YOU LOST')
        sleep(2)
        for member in snake:
            member.memberButton.destroy()
        snake = [Member(head = True)]
        elongate()
        score = 0
        scoreLabel.configure(text = "score: " + str(score))

def gameOver():
    for i in range(1, len(snake)):
        if snake[0].x == snake[i].x and snake[0].y == snake[i].y:
            return True
    return False


root.bind("<Up>", lambda event: changeCourse('N'))
root.bind("<Down>", lambda event: changeCourse(
'S'))
root.bind("<Right>", lambda event: changeCourse('E'))
root.bind("<Left>", lambda event: changeCourse('W'))
        
def task():
    global snake, score, bestScore
    move(snake[0])
    prev = snake[0].direction
    for index in range(1, len(snake)):
        temp = snake[index].direction
        snake[index].direction = prev
        prev = temp
        move(snake[index])    
    if gameOver():
        pass
        if score > bestScore:
            bestScore = score
            bestScoreLabel.configure(text = "Best Score: " + str(bestScore))
        print('YOU LOST')
        sleep(2)
        for member in snake:
            member.memberButton.destroy()
        snake = [Member(head = True)]
        elongate()
        score = 0
        scoreLabel.configure(text = "score: " + str(score))
    root.after(150, task)

if __name__ == '__main__':
    food = Food()
    snake = [Member(head = True)]
    elongate()
    getNewFood()
    root.after(150, task)
    root.mainloop()
