from matrixops import *
import pickle
from test_mnist import *
from time import sleep
from PIL import Image

Xlst = get_X_lst()

def get_i(index):
	size = [28,28]
	i = Image.new("RGB", size)
	img_lst = Xlst[index][1:]
	for x in range(28):
		for y in range(0, 28):
			color = img_lst[x*28+y]
			if color == -1:
				i.putpixel((x,y), (255,255,255))
			else:
				i.putpixel((x,y), (0,0,0))

	return i

def classify(i):
	ex = [1]
	for x in range(28):
		for y in range(28):
			color = i.getpixel((x,y))
			if color == (0, 0, 0):
			#	print "ERROR",x,y
				ex.append(1.0)
			else:
				ex.append(-1.0)
	f = open("thetas1.pkl", "rb")
	thetas = pickle.load(f)
	f.close()
	print classifier_old(thetas, ex)
	return

def show(i):
	i.rotate(270).transpose(Image.FLIP_LEFT_RIGHT).show()
	return

imgs = []
for i in range(0,30):
	imgs.append(get_i(i))

for i in imgs:
	show(i)
	classify(i)
	sleep(3)

