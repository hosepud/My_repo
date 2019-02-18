from matrixops import *
import pickle
from random import randint 

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

def get_X_lst():
	N = 10000
	X = []
	f = open("mnist/t10k-images-idx3-ubyte", "rb")
	bytes = f.read(16)
	rows = 28
	cols = rows
	ctr = 10000
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
		if ctr == 10000-N:
			break
	f.close()
	print len(X), len(X[0])
	return X

def classifier_old(thetas, ex):
	probs = {}
	for key in thetas:
		theta = thetas[key]
		probs[g((Matrix([ex])*theta).lst[0][0])] = key
	return probs[max(probs)]

def test_func():
	def classifier(thetas_neg, thetas_pos, ex, old = False):
		if old:
			return classifier_old(thetas_neg, ex)
		probs_neg = {}
		probs_pos = {}
		for key in thetas_neg:
			theta_pos = thetas_pos[key]
			theta_neg = thetas_neg[key]
			probs_neg[key] = g((Matrix([ex])*theta_neg).lst[0][0])
			probs_pos[key] = g((Matrix([ex])*theta_pos).lst[0][0])
		probs = {}
		
		for key in probs_neg:
			probs[probs_neg[key]*probs_pos[key]] = key	
		tmp = probs[max(probs)]

		pos_lst = []
		neg_lst = []
		for key in probs_neg:
			neg_lst.append([probs_neg[key],key])			
			pos_lst.append([probs_pos[key], key])

		neg_lst = filter(lambda x: x[0] > 0.5, sorted(neg_lst)[::-1])
		pos_lst = filter(lambda x: x[0] > 0.5, sorted(pos_lst)[::-1])
		if len(pos_lst) == 0 and len(neg_lst) == 0:
			return classifier_old(thetas_pos, ex)
		elif len(pos_lst) == 0:
			return classifier_old(thetas_neg, ex)
		elif len(neg_lst) == 0:
			return classifier_old(thetas_neg, ex)
	
		for i in range(len(neg_lst)):
			ans = neg_lst[i][1]
			val = neg_lst[i][1]
			for j in range(len(pos_lst)):
				if pos_lst[j][1] == ans:
					return ans
		return 



	N = 10000
	X = Matrix(get_X_lst())
	Y = []
	f = open("mnist/t10k-labels-idx1-ubyte", "rb")
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
	f = open("thetas2.pkl", "rb")
	thetas_pos = pickle.load(f)
	f.close()
	f = open("thetas1.pkl", "rb")
	thetas_neg = pickle.load(f)
	f.close()
	correct = 0.0
	for i in range(N):
		ex = X.lst[i]
		ans = classifier(thetas_neg, thetas_pos, ex, False)
		print Y[i], ans, correct
		if Y[i] == ans:
			correct += 1
	print "Success: ", correct/N
	f.close()
	return Y

#test_func()
