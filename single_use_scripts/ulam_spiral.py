from PIL import Image

im = Image.new('RGB',(200, 200), (225,225,225))

def is_prime(n):
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True
           
def fill_square(n, start, x, y, d):
    if n == 1:
        d[x,y] = start
        return start,x,y
    for i in range(n):
        d[x,y] = start
        start-=1
        x-=1
    x+=1
    y-=1
    for i in range(n-1):
        d[x,y] = start
        start-=1
        y-=1
    x+=1
    y+=1
    for i in range(n-1):
        d[x,y] = start
        start-=1
        x+=1
    y += 1
    x -= 1
    for i in range(n-2):
        d[x,y] = start
        start -= 1
        y += 1
    return start

def fill_picture_dict(n):
    d = {}
    start = n*n
    x = n-1
    y = n-1
    for i in range(n, -1, -2):
        start = fill_square(i, start, x, y, d)
        x = x-1
        y = y-1
    return d

d = fill_picture_dict(199)
def fill_pic(im,d):
    for x in range(im.size[0]-1):
        for y in range(im.size[1]-1):
            if is_prime(d[x,y]):
                im.putpixel((x,y), (0,0,0))

fill_pic(im, d)
im.show()
