#!/usr/bin/env python

from tkinter import *
from PIL import Image, ImageTk
from os import listdir, path
import imghdr
import sys

indeces = [0]
directory = sys.argv[1]
WIDTH = 800
HEIGHT = 600
PICTURE_HEIGHT = 160
TEXT_HEIGHT = 20
MARGIN = 10

master = Tk()
master.wm_title('thumbpy')
master.configure(bg = "black")
master.minsize(width = WIDTH+100, height = HEIGHT)
master.maxsize(width = WIDTH+100, height = HEIGHT)
w = Canvas(master, width = WIDTH, height = HEIGHT, bg = "black")
w.place(x=0, y=0)

image_shown = {}
texts = {}    
photos = {}

def put_pic(image_name, x, y):
    image = Image.open(directory + image_name)
    size = new_size(image.size)
    while size[0] > WIDTH:
        size = (int(size[0]/2), int(size[1]/2))
    if size[0] + x >= WIDTH:
        return False
    photo = ImageTk.PhotoImage(image.resize(size))
    photos[x,y] = photo
    image_shown[x,y] = w.create_image(x, y, image = photo, anchor = NW)
    texts[x,y] = w.create_text(x, y+PICTURE_HEIGHT, text = image_name, anchor = NW, width = size[1], fill = "white")
    return size[0]

def is_image_gif(name):    
    formats = ["gif", "jpeg", "jpg", "png"]
    return not path.isdir(directory+name) and imghdr.what(directory + name) in formats 

def new_size(size):
    return (int(PICTURE_HEIGHT*(float(size[0])/size[1])), PICTURE_HEIGHT)

def put_all_pics(ctr = 0):
    index = indeces[-1]
    x = 0
    y = 0
    pic_list = listdir(directory)
    while index < len(pic_list):
        i = pic_list[index]
        if is_image_gif(i):
            put = put_pic(i, x, y) 
            if put:
                index += 1
                x+=(put+MARGIN)
            else:
                x = 0
                y+=(PICTURE_HEIGHT + TEXT_HEIGHT)
                if y + PICTURE_HEIGHT >= HEIGHT:
                    break   
        else:
            index +=1            
    indeces.append(index)
    from_to.config(text = "%d - %d"%(indeces[-2], indeces[-1]))
    return 

def next_pics():
    global texts, photos, image_shown
    for key in photos:
        w.delete(image_shown[key])
        w.delete(texts[key])
    image_shown = {}
    texts = {}
    photos = {}
    put_all_pics()

def back_pics():
    global texts, photos, image_shown
    if len(indeces) <= 2:
        return
    for key in photos:
        w.delete(image_shown[key])
        w.delete(texts[key])
    image_shown = {}
    texts = {}
    photos = {}
    if len(indeces) > 2:
        indeces.pop()
        indeces.pop()
    put_all_pics()

total = Label(master, text = "%d"%len(listdir(directory)), bg = "black", fg = "white")
total.place(x = WIDTH+MARGIN, y = int(HEIGHT/2)-30)
from_to = Label(master, text = "%d - %d"%(indeces[-1], indeces[-1]), bg = "black", fg="white")
from_to.place(x = WIDTH+MARGIN, y = int(HEIGHT/2))
back_button = Button(master, command = back_pics, bg = "black", fg="white", activebackground = "black", activeforeground = "white")
back_button.place(x=WIDTH, y = HEIGHT-3*MARGIN)
back_button.configure(text = "<")
next_button = Button(master, command = next_pics, bg = "black", fg ="white", activebackground = "black", activeforeground = "white")
next_button.place(x=WIDTH, y=0)
next_button.configure(text = ">")
master.mainloop()
