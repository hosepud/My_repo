from random import uniform
from logreg import *
import pickle

def get_Y_lst(num, N):
	Y = []
	f = open("mnist/train-labels-idx1-ubyte", "rb")
	byte = f.read(8)
	byte = f.read(1)
	ctr = 0
	while byte != "":
		if ord(byte) == num:
			Y.append(1)
		else:
			Y.append(0)
		ctr += 1
	#	print ord(byte), ctr
		byte = f.read(1)
		if ctr == N:
			break
	f.close()
	return Y

def get_X_lst(N):
	X = []
	f = open("mnist/train-images-idx3-ubyte", "rb")
	bytes = f.read(16)
	rows = 28
	cols = rows
	ctr = 60000
	while ctr != 0:
		bytes = f.read(28*28)
		bytes = map(lambda x: ord(x), list(bytes))
		tmp = [1]
		for i in bytes:
			if i:
	#			tmp.append(i/255.0)
				tmp.append(1.0)
			else:
			#	tmp.append(0.0)
				tmp.append(-1.0)
		X.append(tmp)
	#	print ctr
		ctr -= 1
		if ctr == 60000-N:
			break
	f.close()
	print len(X), len(X[0])
	return X

def get_theta_lst(n):
	theta = []
	for i in range(n):
		theta.append(uniform(-0.05, 0.05))
	return theta

def test_all(X,N):
	def classifier(thetas, ex):
		probs = {}
		for key in thetas:
			theta = thetas[key]
			hyp = g((Matrix([ex])*theta).lst[0][0])			
			probs[hyp] = key
		return probs[max(probs)]
	Y = []
	f = open("mnist/train-labels-idx1-ubyte", "rb")
	byte = f.read(8)
	byte = f.read(1)
	ctr = 0
	while byte != "":
		Y.append(ord(byte))
		ctr += 1
	#	print ord(byte), ctr
		byte = f.read(1)
		if ctr == N:
			break
	f = open("thetas1.pkl", "rb")
	thetas = pickle.load(f)
	f.close()
	correct = 0.0
	for i in range(N):
		ex = X.lst[i]
		ans = classifier(thetas, ex)
		print Y[i], ans, correct
		if Y[i] == ans:
			correct += 1
	print "Success: ", correct/N
	f.close()
	return Y	

def test_one(X, Y, num, N):
	f = open("theta%d.pkl"%num, "rb")
	theta = pickle.load(f)
	f.close()
	nums = 0
	correct = 0
	FN = 0.0
	FP = 0.0
	for i in range(N):
		ex = X.lst[i]
		y = Y.lst[i]
		hyp = g((Matrix([ex])*theta).lst[0][0])	
	#	print theta.size(), Matrix([ex]).size(), round(hyp), y[0]
		if round(hyp) == y[0]:
			correct += 1
		elif round(hyp) == 0 and y[0] == 1:
			FN += 1
		elif round(hyp) == 1 and y[0] == 0:
			FP += 1
		if y[0] == 1:
			nums += 1
	print "Success rate: ", 100*correct/(i+1), "%" 
	print "Total %d's: "%num, nums
	print "FN/nums %f FP %f"%(FN/nums, FP/(60000-nums))
	return	

def regularized(theta, l, alpha, m):
	lst = theta().lst
	const = l/(m*2.0)
	cost_reg = 0.0
	for i in range(1,len(lst)):
		lst[i] = lst[i] + alpha*const*lst[i]*2
		cost_reg += const*lst[i]**2
	return Matrix(lst)(), cost_reg
	
def load_thetas():
	thetas = {}
	for i in range(0, 10):
		f = open("theta%d.pkl"%i,"rb")
		thetas[i] = pickle.load(f)
		f.close()
	f = open("thetas2.pkl", "wb")
	pickle.dump(thetas, f, pickle.HIGHEST_PROTOCOL)
	f.close()	
	return thetas

def reduce_data(X, Y):
	newX = []
	newY = []
	negs = 0
	for i in range(len(Y.lst[0])):
		if Y.lst[0][i] == 1:
			newY.append(1)
			newX.append(X.lst[i])
			negs += 1
	for i in range(len(Y.lst[0])):
		if Y.lst[0][i] == 0:
			newY.append(0)
			newX.append(X.lst[i])
			negs -= 1
		if negs == 0:
			break
	return Matrix(newX), Matrix([newY])()

def done(s, t):
	return (time()-s)/60.0 > t

def train(N):
	theta_dict = {}
	X = Matrix(get_X_lst(N))
	t = Matrix([get_theta_lst(len(X.lst[0]))])()
	#prev_thetas = load_thetas()
	alpha = 0.01
	error = 0.000125
	l = 1000.0
	for i in range(1,9):
		s = time()
		Ylst = get_Y_lst(i, N)
		Y = Matrix([Ylst])()
		X = Matrix(get_X_lst(N))
		X,Y = reduce_data(X,Y())
		invX = X()
	#	theta = prev_thetas[i]
		theta = t
		theta, J = regularized(theta, l, alpha, N)
		J = J + cost(theta, X, Y, invX)
		print X.size(), Y.size(), theta.size()
		prev_J = 1000000000
		while (not done(s, 10)):
			prev_J = J
			theta = gradient_descent(theta, X, Y, alpha)
			theta, J = regularized(theta, l, alpha, N)
			J = J + cost(theta, X, Y, invX)		
			print J, 1-abs(J/prev_J)
		theta_dict[i] = theta
		f = open("theta%d.pkl"%i,"wb")
		pickle.dump(theta, f, pickle.HIGHEST_PROTOCOL)
		f.close()
		print i,"'s Done in ", (time()-s)/60.0, " minutes"
	f = open("thetas.pkl", "wb")
	pickle.dump(theta_dict, f, pickle.HIGHEST_PROTOCOL)
	f.close()
	return

#load_thetas()

N=60000

#start = time()
#train(N)		
#print (time()-start)/60.0, "minutes"

for i in range(1,10):
	num = i
	X = Matrix(get_X_lst(N))
	Y = Matrix([get_Y_lst(num, N)])()
	test_one(X, Y, num, N)
	print '\n',


#X = Matrix(get_X_lst(N))
#test_all(X, N)
