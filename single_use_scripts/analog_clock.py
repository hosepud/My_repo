from tkinter import *
from math import sin, cos, pi, sqrt
import datetime

root = Tk()
root.maxsize(height = 400, width = 400)
root.minsize(height = 400, width = 400)
canvas = Canvas(root, width = 400, height = 400)
canvas.pack()
clock = canvas.create_oval((25,25,375,375))
hour_line = canvas.create_line((200,200, 200, 50), fill = 'blue', width = 5)
minute_line = canvas.create_line((200,200,200, 50), fill = 'red', width = 5)
seconds_line = canvas.create_line((200,200,200,50), fill = 'green', width = 5)

def get_clock_coords():
    coords = [3,2,1] + list(range(12,3,-1))
    for i in range(0, 12):
        coords[i] = (coords[i], (cos(i*pi/6)*sqrt(175)*12+200, -sin(i*pi/6)*sqrt(175)*12+200))
    return coords

def put_numbers(numbers):
    for num,coords in numbers:
        canvas.create_text(coords, text = str(num))
    return numbers

def get_time():
    clock = datetime.datetime.now().__str__().split(' ')[1].split(':')
    return clock[0], clock[1], clock[2].split('.')[0]


def put_hour_arrow(hour, minute, numbers):
    global hour_line
    if int(hour) > 12:
        hour = str(int(hour) - 12)
    for index in range(len(numbers)):
        i = numbers[index]
        if str(i[0]) == hour:
            coords = [i[1][0], i[1][1]]
            inc = int(minute)/60.0
            coords[0] = cos((index - inc)*pi/6)*sqrt(120)*12 + 200
            coords[1] = -sin((index - inc)*pi/6)*sqrt(120)*12 + 200
            canvas.delete(hour_line)
            hour_line = canvas.create_line((200,200) + tuple(coords), fill = 'blue', width = 5)     
    return

def put_minute_arrow(minute):
    global minute_line
    angle = ((float(minute)-15)/60)*2*pi
    x = cos(angle)*sqrt(175)*12 + 200
    y = sin(angle)*sqrt(175)*12 + 200
    canvas.delete(minute_line)
    minute_line = canvas.create_line((200,200)+(x,y), fill = 'red', width = 5)
    return

def put_seconds_arrow(second):
    global seconds_line
    angle = ((float(second)-15)/60)*2*pi
    x = cos(angle)*sqrt(175)*12 + 200
    y = sin(angle)*sqrt(175)*12 + 200
    canvas.delete(seconds_line)
    seconds_line = canvas.create_line((200,200)+(x,y), fill = 'green', width = 5)
    return

def show_time(coords):
    hour, minute, second = get_time()
    put_hour_arrow(hour, minute,coords)
    put_minute_arrow(minute)
    put_seconds_arrow(second)
    root.after(950, lambda: show_time(coords))

if __name__ == '__main__':
    coords = get_clock_coords()
    put_numbers(coords)
    root.after(1, lambda: show_time(coords))
    root.mainloop()
