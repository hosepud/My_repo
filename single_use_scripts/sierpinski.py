from tkinter import *

root = Tk()
root.maxsize(width = 500, height = 500)
root.minsize(width = 500, height = 500)
w = Canvas(root, width = 500, height = 500)
w.pack()

def x(point):
    return point[0]

def y(point):
    return point[1]

def Point(x,y):
    return (x,y)

def Triangle(p1, p2, p3):
    return (p1, p2, p3)

def draw_triangle(triangle, color):
    p1,p2,p3 = triangle
    w.create_polygon(triangle, fill = color)
    return 

def middle(p1, p2):
    return Point((x(p1) + x(p2))/2.0, (y(p1) + y(p2))/2.0)  
    
def shrink_and_kill(triangle):
    p1 = middle(triangle[0], triangle[1])
    p2 = middle(triangle[1], triangle[2])
    p3 = middle(triangle[2], triangle[0])
    draw_triangle(Triangle(p1, p2, p3), 'white')
    top_triangle = (triangle[0], p1, p3)
    left_triangle = (p1, triangle[1], p2)
    right_triangle = (p3, p2, triangle[2])
    return (top_triangle, left_triangle, right_triangle)

def draw_sierpinski(t, levels):
    if levels == 0:
        return
    for t in shrink_and_kill(t):
        draw_sierpinski(t, levels - 1)  

if __name__ == '__main__':    
    b = Triangle(Point(250, 0), Point(0, 433.0127), Point(500, 433.0127))
    draw_triangle(b, 'black')
    draw_sierpinski(b, 6)
    root.mainloop()
