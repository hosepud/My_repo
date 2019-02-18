from math import e, log
from matrixops import *

invX = None

def h(theta, X):
	return gM(X, theta)

def size(M):
	return M.size()

def cost(theta, X, Y, tX):
	global invX
	invX = tX
	hyp = h(theta, X)()
	m = X.n_rows()
	one = Myint(1.0)
#	print "THETA: ",size(theta), theta.lst
#	print "X: ", size(X), X.lst
#	print "Y: ", size(Y), Y.lst
#	print "hyp: ", size(hyp), hyp.lst
#	print "LOG1: ", (-Y()*logM(hyp)).size()
#	print "LOG2: ", (-(one-Y())*logM(one-hyp)).size()
#	print "LOGDIF: ", ((-Y()*logM(hyp)) - (one-Y())*logM(one-hyp)).size()
#	for i in hyp.lst:
#		print i
	invY = Y()
	J = (-invY*logM(hyp)-(one-invY)*logM(one-hyp))*(1.0/m)
#	print J.lst
	return J.get(0,0)
		
def differential(theta, X, Y):
#	print "X SIZE: ", X.size()
#	print "gM SIZE: ", gM(X, theta).size()
#	print "Y SIZE: ", Y.size()
	return invX*(gM(X, theta)() - Y)

def gradient_descent(theta, X, Y, alpha):
	const = alpha/X.n_rows()
	return theta - differential(theta, X, Y)*const

def normalized(X, max_n):
	lst = []
	for i in range(X.n_rows()):
		row = []
		for j in range(X.n_cols()):
			row.append(X.get(i,j)/max_n)
		lst.append(row)
	return Matrix(lst)

from random import randint
from time import time

def gen_train_set(N):
	X = []
	Y = []
	for i in range(N):
		ex = [1,randint(1,10), randint(1,7), randint(1,20)]
		X.append(ex)
		Y.append(int(ex[1]*2+ex[2]*2+2>ex[3]*3+3))
	return normalized(Matrix(X), 20.0*3+3), Matrix([Y])()

def test_theta(theta):
	correct = 0.0
	test_X,test_Y = gen_train_set(100)
	for i in range(test_X.n_rows()):
		ex = test_X.lst[i]
		y = test_Y.lst[i]
		hyp = g((Matrix([ex])*theta).lst[0][0])	
	#	print theta.size(), Matrix([ex]).size(), round(hyp), y[0]
		if round(hyp) == y[0]:
			correct += 1
	print "Success rate: ", 100*correct/(i+1), "%" 
	return

def done(J, prev_J, a):
#	return (J-prev_J)**2 < a
	return (1-abs(J/prev_J) < a) and J < prev_J
#start = time()
#alpha = 1.0
#X, Y = gen_train_set(300)
#theta = Matrix([[0.15, -0.15, 0.1, 0.3]])()
#J = cost(theta, X, Y)
#prev_J = 1000
#while not done(J, prev_J):
#	theta = gradient_descent(theta, X, Y, alpha)
#	prev_J = J
#	J = cost(theta, X, Y)

#print theta.lst
#print (time() - start)/60, " minutes"
#test_theta(theta)
