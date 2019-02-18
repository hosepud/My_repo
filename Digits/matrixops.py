from math import e, log

def g(z):
	return 1.0/(1.0+e**(-z))

def gM(X, theta):
	lst = list((X*theta)().lst[0])
	for j in range(len(lst)):
		lst[j] = g(lst[j])
	return Matrix([lst])

def logM(M):
	lst = []
	rows = M.n_rows()
	cols = M.n_cols()
	for i in range(rows):
		row = []
		for j in range(cols):
#			print M.get(i,j)
			tmp = M.lst[i][j]
			if tmp == 0:
				row.append(-1000.0)
			else:
				row.append(log(tmp))
		lst.append(row)
	return Matrix(lst)
	
class Myint(object):
	def __init__(self, val):
		self.val = val

	def __add__(self, other):
		if isinstance(other, int):
			return Myint(self.val+other)
		else:
			lst = []
			rows = other.n_rows()
			cols = other.n_cols()
			for i in range(rows):
				row = []
				for j in range(cols):
					row.append(other.lst[i][j] + self.val)
				lst.append(row)
			return Matrix(lst)
			
	def __mul__(self, other):
		if isinstance(other, int):
			return Myint(self.val*other)
		else:
			lst = []
			rows = other.n_rows()
			cols = other.n_cols()
			for i in range(rows):
				row = []
				for j in range(cols):
					row.append(other.lst[i][j]*self.val)
				lst.append(row)
			return Matrix(lst)

	def __sub__(self, other):
		if isinstance(other, int):
			return Myint(self.val-other)
		else:
			lst = []
			rows = other.n_rows()
			cols = other.n_cols()
			for i in range(rows):
				row = []
				for j in range(cols):
					row.append(self.val-other.lst[i][j])
				lst.append(row)
			return Matrix(lst)

class Matrix(object):
	def __init__(self, lst):
		self.lst = lst
	def get(self, row, column):
		return self.lst[row][column]

	def n_rows(self):
		return len(self.lst)
	
	def n_cols(self):
		return len(self.lst[0])
	
	def size(self):
		return [self.n_rows(), self.n_cols()]

	def __call__(self):
		return Matrix(zip(*self.lst))
	
	def __add__(self, other):
		ret = []
		rows = self.n_rows()
		cols = self.n_cols()
		selflst = self.lst
		for i in range(rows):
			row = []
			for j in range(cols):
				if isinstance(other, int) or isinstance(other, float):
					row.append(selflst[i][j] + other)
				else:
					row.append(selflst[i][j] + other.lst[i][j])
			ret.append(row)
		return Matrix(ret)

	def __mul__(self, other):
		selflst=self.lst
		rows_self = self.n_rows()
		cols_self = self.n_cols()
		if isinstance(other, int) or isinstance(other, float):
			ret = []
			for i in range(rows_self):
				row = []
				for j in range(cols_self):
					row.append(selflst[i][j]*other)
				ret.append(row)
			return Matrix(ret)
		rows_other = other.n_rows()
		cols_other = other.n_cols()
		otherlst = other.lst
		if cols_self != rows_other:
			print self.size(), other.size()
      			print "Multiplication with incorrect dimensions."
      			return
    		res = [[0 for row in range(cols_other)] for col in range(rows_self)]
    		for i in range(rows_self):
        		for j in range(cols_other):
            			for k in range(cols_self):
                			res[i][j] += selflst[i][k] * otherlst[k][j] 		
		return Matrix(res)
	
	def __sub__(self, other):
		selflst=self.lst
		ret = []
		rows = self.n_rows()
		cols = self.n_cols()
		for i in range(rows):
			row = []
			for j in range(cols):
				if isinstance(other, int) or isinstance(other, float):
					row.append(selflst[i][j] - other)
				else:
					row.append(selflst[i][j] - other.lst[i][j])
			ret.append(row)
		return Matrix(ret)	
	
	def __neg__(self):
		zero = Myint(0)
		return zero-self

