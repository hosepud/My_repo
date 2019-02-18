from preproc import *
from sys import argv, exit
from ccompiler import *

def_ctr = 0
new_names = {}
keywords = ["lazy"]
forbidden = ["if"]

def process(app):
	a = make_into_lst(exp_to_exp_stack(app))
	app_lst = strip_listified(listify(a))
	return app_lst	

def resolve_escaped(char):
	seqs = {"n": '\n', "\\": '\\', "r": '\r', "b": '\b', "t": '\t', "a":'\a',
		"e": '\f',"v":'\v',} 
	return str(ord(seqs[char]))

def get_string(exp, i):
	string = "(string "
	escaped = False
	for j in range(i, len(exp)):
		if exp[j] + exp[j+1]+exp[j+2] == '"""':
			return string + ")", j+2
		if exp[j] == "\\" and not escaped:
			escaped = True
		else:
			if escaped:
				string += resolve_escaped(exp[j]) + " "
				escaped = False
			else:
				string += str(ord(exp[j])) + " "
	
def preprocess(exp):
	ret = []
	in_string = False
	i = 0
	while (i< len(exp)):
		if i >= len(exp) or i+1>=len(exp) or i+2>=len(exp):
			ret.append(exp[i:])
			return ''.join(ret)
		if exp[i]+exp[i+1]+exp[i+2] == '"""':
			string, j = get_string(exp, i+3)
			i = j
			ret.append(string)
		else:
			ret.append(exp[i])
		i+=1
	
	return ''.join(ret)

def is_string(exp):
	return exp[0] == "string"

def is_var(exp):
	return isinstance(exp, str)

def is_char(exp):
	return exp[0] == "'" and exp[-1] == "'"

def is_lambda(exp):
	#print(exp)
	return exp[0] == "@"

def is_call(exp):
	return isinstance(exp, list)

def is_printstr(exp):
	return exp[0] == "print"

def is_input(exp):
	return exp[0] == "input"

def is_newline(exp):
	return exp[0] == "newline"

def deal_with_string(exp):
	ret = "nil"
	for i in exp[::-1]:
		ret = [["pair", i], ret]		
	return ret

infinite = ["*", "+", "/", "-"]
dual = ["expt", "=", "<=", ">=", ">", "<", "pair", "and", "%"]
reverse = ["or", "and"]
tri = ["map", "filter", "enum", "list-ref"]

def deal_with_call(exp):
	if len(exp) == 2:
		return [sanitized(exp[0]), sanitized(exp[1])]
	if exp[0] in reverse:
		if len(exp) == 3:
			return [[exp[0], sanitized(exp[2])], sanitized(exp[1])]
		new_exp = [exp[0]]
		new_exp.append([[exp[0], exp[2]], exp[1]])
		new_exp.extend(exp[3:])
		return deal_with_call(new_exp)					
	elif exp[0] in infinite:
		if len(exp) == 3:
			return [[exp[0], sanitized(exp[1])], sanitized(exp[2])]
		new_exp = [exp[0]]
		new_exp.append([[exp[0], exp[1]], exp[2]])
		new_exp.extend(exp[3:])
		return deal_with_call(new_exp)
	elif exp[0] in dual:
		new_exp = []
		new_exp.append([exp[0], sanitized(exp[1])])
		new_exp.append(sanitized(exp[2]))
		return new_exp
	elif exp[0] in tri:
		return [[exp[0], sanitized(exp[1])], sanitized(exp[2])]
	elif exp[0] == "if":
		return [[["if", sanitized(exp[1])], ["@", "lazy", sanitized(exp[2])]], ["@", "lazy", sanitized(exp[3])]]	
	elif exp[0] == "reduce":
		return [[["reduce", sanitized(exp[1])], sanitized(exp[2])], sanitized(exp[3])]

def is_case(exp):
	return exp[0] == "case"

def deal_with_clauses(exp):	
	if exp[0] != "else":
		pred = sanitized(exp[0])
		cons = sanitized(exp[1])
		rest = deal_with_clauses(exp[2:])				
		return sanitized(["if", pred, cons, rest])
	else:
		return sanitized(["if", "true", sanitized(exp[1]), "nil"]) 

def cmpl_exps(exps):
	global def_ctr
	for i in exps:
		if i[0] == "import":
			deal_with_import(i)
			continue
		if i[0] == "define":
			new_names[i[1]] = i[1] + "_"+ str(def_ctr)
			def_ctr += 1
			i[1] = new_names[i[1]]
			i[2] = name_pass(i[2], {})
			compile_func(i)
		else:
			i = [name_pass(i[0], {}), name_pass(i[1], {})]
			compile_func(i)
		

def name_pass(exp, variables):
	if is_var(exp):
		if exp in variables:
			return exp
		if exp in new_names:
			return new_names[exp]
		else:
			return exp
	if is_lambda(exp):
		variables[exp[1]] = None
		return [exp[0], exp[1],	name_pass(exp[2], variables)]
	else:
		return [name_pass(exp[0], variables), name_pass(exp[1], variables)]
	
def deal_with_import(exp):
	fname = exp[1] + ".lc"
	exps = get_exps(fname)
	cmpl_exps(exps)
	return
			
def is_import(exp):
	return exp[0] == "import"

def sanitized(exp):
	if is_char(exp):
		return str(ord(exp[1]))	
	if is_var(exp):
		return exp
	if is_import(exp):
		return exp
	if is_string(exp):
		return deal_with_string(exp[1:])
	if is_newline(exp):
		return ["print-char", "10"]
	if is_input(exp):
		return [["read", "stdin"] ,"nil"]	
	if is_printstr(exp):
		return [["write", "stdout"], sanitized(exp[1])]
	if is_lambda(exp):
		return [exp[0], exp[1], sanitized(exp[2])]
	if is_case(exp):
		return deal_with_clauses(exp[1:])
	if is_call(exp):
		return deal_with_call(exp)

def remove_comments(f):
	current = ""
	text = []
	for line in f:
		for i in line:
			if i == "#":
				break
			current += i
		text.append(current + "\n")
		current = ""
	return ''.join(text)

def parse_file(f):
	ctr = 0
	in_exp = False
	current = ""
	exps = []
	text = remove_comments(f)
	for i in text:
		if i in ["\n", "\t", "\r"]:
			i = " "
		if i == "(":
			in_exp = True
			ctr += 1
		if in_exp:
			current += i
		if i == ")":
			ctr -= 1
			if ctr == 0:
				in_exp = False
				exps.append(current)
	if ctr < 0:
		print("Unbalanced brackets at %s, too many!"%f.name)
		exit()
	if ctr > 0:
		print("Unbalanced brackets at %s, too few!"%f.name)
		exit()
	return exps
	 
def get_exps(filename):
	f = open(filename, "r")
	exps = parse_file(f)
	f.close()
	tmp = []
	for i in exps:
		if i.strip():
			tmp.append(process(preprocess(i.strip())))
	
	ret = []
	for i in tmp:
		if i[0] == "define":
			ret.append([i[0], i[1], sanitized(i[2])])
		else:
			ret.append(sanitized(i))
	return ret
				
def output_code():
	for i in global_scope:
		print(i)	

	for i in outro():
		print(i)

exps = get_exps(sys.argv[1])
cmpl_exps(exps)
output_code()



