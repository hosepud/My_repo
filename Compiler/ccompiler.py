from preproc import *

def process(app):
	a = make_into_lst(exp_to_exp_stack(app))
	app_lst = strip_listified(listify(a))
	return app_lst	

var_ctr = 0
func_ctr = 3
global_scope = []
main_scope = []
global_env = {}
definitions = {}

def is_variable(exp):
	return isinstance(exp, str)

def is_call(exp):
	return len(exp) == 2 and isinstance(exp, list)

def is_lambda(exp):
	return exp[0] == "@"

def is_define(exp):
	return exp[0] == "define"

vars_dict = {}
	
def get_frees(var, exp, frees):
	if is_variable(exp):
		if exp != var and exp not in global_env:
			frees[exp] = None
	elif isinstance(exp, list):
		get_frees(var, exp[0], frees)
		get_frees(var, exp[1], frees)
	return list(frees)
	
class Function(object):
	def __init__(self, name, var):
		self.ret = None
		self.var = var
		self.name = name
		self.frees = {}

	def fill_frees(self):
		if is_variable(self.ret):
			if self.ret != self.var and self.ret not in global_env:
				self.frees[self.ret] = None

		else:
			self.frees = get_frees(self.var, self.ret, {})
		return

var_ctrs = []
def cache(exp, ctr):
	global var_ctrs
	var_ctrs.append([exp, ctr])			

def extract(exp):
	global var_ctrs
	for i in var_ctrs:
		if i[0] == exp:
			return i[1]
	return None
				
tmp_var_ctr = 0

def uniqify_vars(exp):
	global var_ctr, vars_dict, var_ctrs
	if is_lambda(exp):
		var = exp[1]
		vars_dict[var] = "var"+str(var_ctr)
		var_ctr += 1
		return [exp[0], vars_dict[var], uniqify_vars(exp[2])]
	if is_call(exp):
		cache(exp, var_ctr)

		f = uniqify_vars(exp[0])
		var_ctr = extract(exp)

		arg = uniqify_vars(exp[1])		
		return [f, arg]
	else:
		if exp in vars_dict:
			return vars_dict[exp]
		else:
			return exp

def tokenize(exp):
	global func_ctr
	if is_variable(exp):
		return exp

	elif is_call(exp):
		return [tokenize(exp[0]), tokenize(exp[1])]

	else:
		var = exp[1]
		f = Function("closure"+str(func_ctr), var)
		func_ctr += 1
		f.ret = tokenize(exp[2])
		return f
	
def get_free(var):
	if "_" in var:
		return "\t"+var + ";"
	index = int(var[3:])
	return "\tfunction* %s = env[%d];"%(var, index)

def obj_name(funcname):
	return funcname[0].upper() + funcname[1:]

def is_clos(name):
	return name[:7] == "closure"

def pycompile(exp, current = main_scope):
	if is_variable(exp):
		return exp
	elif isinstance(exp, Function):
		exp.fill_frees()
		current = []
		current.append("function* %s(function* %s,function** env, memstruct* m){"%(exp.name, exp.var))
		env_index = int(exp.var[3:])
		current.append("\tenv[%d] = %s;"%(env_index, exp.var))
		current.append("\tenv[%d] = NULL;"%(env_index+1))
		for i in exp.frees:
			current.append(get_free(i))
		if isinstance(exp.ret, Function):
			pycompile(exp.ret, current)
			current.append("\tfunction* %s = create_function(%s, env, 0, m);"%(obj_name(exp.ret.name), exp.ret.name))
			current.append("\treturn %s;}\n"%obj_name(exp.ret.name))
		elif isinstance(exp.ret, str):
			current.append("\treturn %s;}\n"%pycompile(exp.ret, current))
		elif isinstance(exp.ret, list):
			ret = pycompile(exp.ret, current)			
			current.append("\treturn %s;}"%ret)	
		global_scope.extend(current)
		return exp.name
	else:
								
		f = pycompile(exp[0], current)
		arg = pycompile(exp[1], current)
		if is_clos(f):
			current.append("\tfunction* %s = create_function(%s, env, 0, m);"%(obj_name(f), f))
			f = obj_name(f)
		if is_clos(arg):
			current.append("\tfunction* %s = create_function(%s, env, 0, m);"%(obj_name(arg), arg))
			arg = obj_name(arg)
		return "call(%s, %s, m)"%(f, arg)

def define_helper(exp, name, variable):
	global func_ctr
	if is_variable(exp):
		if exp == name:
			return "Closure"+str(func_ctr)
		if exp == variable:
			return exp
		if exp in definitions:
			return definitions[exp]
		return exp
	if is_call(exp):
		return [define_helper(exp[0], name, variable), define_helper(exp[1], name, variable)]		
	else:
		return ["@", exp[1], define_helper(exp[2], name, variable)]

def obfuscate(name):
	tmp = hash(name)
	if tmp < 0:
		tmp *= -1
	return "var_"+str(tmp)

def do_definition(exp):
	global func_ctr
	name = exp[1]
	tbc = exp[2]
	tbc = uniqify_vars(tbc)
	variable = None
	if is_lambda(tbc):
		variable = tbc[1]
	global_env["Closure"+str(func_ctr)] = None
	if len(tbc) == 3 and not isinstance(tbc, str):
		definitions[name] = "Closure"+str(func_ctr)
	else:
		definitions[name] = obfuscate(name)
	return name, define_helper(tbc, name, variable)

debug_scope = []
		
def global_anons():
	global hanging	
	if hanging:
		for i in hanging:
			main_scope.append(i)
	return
		
	
def compile_func(app):
	global var_ctr, hanging, vars_dict
	if isinstance(app, str):
		app_lst = process(app)
	else:
		app_lst = app
	if app_lst[0] != "define":
		compile_func(["define", "io_var", app_lst])
		return
	name, tbc = do_definition(app_lst)
	a = tokenize(tbc)
	if isinstance(a, Function):
		a.user_name = name
		global_scope.append("function* %s;"%obj_name(a.name))
		res = pycompile(a)
		main_scope.append("\t%s = create_function(%s, empty_env, 0, m);\n"%(obj_name(a.name), a.name))
	else:
		global_scope.append("function* %s;"%obfuscate(name))
		res = pycompile(a)
		main_scope.append("\t%s = %s;\n"%(obfuscate(name), res))
	var_ctr = 0
	hanging = []
	vars_dict = {}
	if name == "io_var":
		del definitions[name]
	for i in definitions:
		global_env[definitions[i]] = None
	if name != "io_var":
		main_scope.append("\troots[%d] = %s;"%(len(definitions)-1, definitions[name]))
		main_scope.append("\troots[%d] = garbage_collect(roots[%d]);"%(len(definitions)-1, len(definitions)-1))
		main_scope.append("\t%s = roots[%d];"%(definitions[name], len(definitions)-1))
		main_scope.append("\troots[%d] = NULL;"%len(definitions))
	#main_scope.append("\tGC(m);")
	return 
		
def init():
	preamble = """

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "gc.h"

#define malloc(n) GC_malloc(n)
#define realloc(object, new_size) GC_realloc(object, new_size)
#define free(object) GC_free(object)

struct Memstruct;
struct Function;

struct Function{
	struct Function* (*body)(struct Function*, struct Function** env, struct Memstruct*);
	struct Function* env[8];
	char visited;
	int integer;
};

typedef struct Function function;
struct Memstruct{
	int func_mem_ctr;
	int func_mem_len;
	function** func_mem;
	
	function* Temp_closure;
	function* f;
	function* arg;
	function* ret;	

	function* function_buffer;
};

typedef struct Memstruct memstruct;

typedef struct Function* (*funcbody)(struct Function*, struct Function** env, struct Memstruct*);



function** ascii_table;

int boundary;

function** empty_env;
function** int_env;
function* call(function* f, function* x, memstruct* m){
	return f->body(x, (f->env), m);
}

void func_realloc(memstruct* m){
	if(m->func_mem_ctr == m->func_mem_len){
		m->func_mem = realloc(m->func_mem, 8*(m->func_mem_len)*2);
		m->func_mem_len *= 2;
	}
	return;
}

int length(function** env){
	int len = 0;
	while(env[len])
		len++;
	return len;
}

void my_memcpy(function** env, function** old_env){
	int i = 0;
	while(old_env[i]){
		env[i] = old_env[i];
		i++;
	}
	env[i] = NULL;
}
 	
function* func_malloc(memstruct* m){
	if(m->func_mem_ctr < boundary)
		return &(m->function_buffer[m->func_mem_ctr]);
	return malloc(sizeof(function));
}

function* create_function(funcbody body, function** env, int is_int, memstruct* m){
	function* f = malloc(sizeof(function));
	f->body = body;
	if(env[0] == NULL || is_int)
		f->env[0] = NULL;
	else
		my_memcpy(f->env, env);
	f->visited = 0;
	f->integer = -1;
	//m->func_mem[m->func_mem_ctr] = f;
	//m->func_mem_ctr += 1;
	//func_realloc(m);
	return f;
}
function** roots_mem;
int roots_mem_ctr;
int roots_mem_len;

function* garbage_collect(function* f){
	return f;
	f->visited = 1;
	function* new_f = memcpy(malloc(sizeof(function)), f, sizeof(function));
	roots_mem[roots_mem_ctr] = new_f;
	roots_mem_ctr += 1;
	if(roots_mem_ctr == roots_mem_len){
		roots_mem = realloc(roots_mem, 2*8*roots_mem_len);
		roots_mem_len *= 2;	
	}
	int i = 0;
	while((new_f->env)[i]){
		if(!(((new_f->env)[i])->visited))
			new_f->env[i] = garbage_collect((new_f->env)[i]);
		i++;
	}
	f->visited = 0;
	return new_f;
}

void GC(memstruct* m){
	function** tmp_func = m->func_mem;
	m->func_mem = malloc(boundary*8);
	m->func_mem_len = boundary;

	int i;
	for(i=0;i<m->func_mem_ctr;i++) 
		if(i>=boundary)
			free(tmp_func[i]);
	free(tmp_func);
	m->func_mem_ctr = 0;		

	return;
}

function* IO_var;

void clean_up(memstruct* m){
	int i;
	for(i=0; i<m->func_mem_ctr; i++)
		free(m->func_mem[i]);
	free(m->func_mem);
	free(m->Temp_closure);
	free(m->function_buffer);
	free(m);
	for(i=0; i< roots_mem_ctr; i++)
		free(roots_mem[i]);
	free(roots_mem);
	return;
}

"""	
	global_scope.append(preamble)
	return

def outro():
	ending = ["""

memstruct* create_memstruct(void){
	memstruct* m = malloc(sizeof(memstruct));
	m->Temp_closure = malloc(sizeof(function));
	m->func_mem_ctr = 0;
	m->func_mem_len = boundary;
//	m->func_mem = malloc(8*boundary);
//	m->function_buffer = malloc(sizeof(function)*boundary);
	return m;
}

int main(void){
	ascii_table = malloc(8*128);
	
	function** roots = malloc((1+%d)*8);
	roots[0] = NULL;

	boundary = 1024;
	memstruct* m = create_memstruct();	

	empty_env = malloc(8*8);
	empty_env[0] = NULL;
	function** env = empty_env;

	int_env = malloc(8*8);
	int_env[0] = NULL;

	roots_mem_ctr = 0;
	roots_mem_len = 128;
	roots_mem = malloc(roots_mem_len*8);
"""%(len(definitions)+1)]
	for i in main_scope:
		ending.append(i)
	ending.append("\tclean_up(m);")
	ending.append("\tfree(empty_env);")
	ending.append("\tfree(roots);")
	ending.append("\tfree(ascii_table);")
	ending.append("\tfree(int_env);")
	ending.append("}")
	return ending

def fill_ascii_table():
	for i in definitions:
		try:
			if int(i) in range(0, 128):
				main_scope.append("\tascii_table[%d] = %s;"%(int(i), definitions[i]))
		except:
			continue
	return


def GC_code(name):		
	main_scope.append("\troots[%d] = %s;"%(len(definitions)-1, definitions[name]))
	main_scope.append("\troots[%d] = garbage_collect(roots[%d]);"%(len(definitions)-1, len(definitions)-1))
	main_scope.append("\t%s = roots[%d];"%(definitions[name], len(definitions)-1))
	main_scope.append("\troots[%d] = NULL;"%len(definitions))
	#main_scope.append("\tGC(m);")		
	return

def compile_enum():
	global func_ctr
	func_ctr += 1
	definitions["enum"] = "Enum"
	name = "enum"
	global_scope.append("""
	function* enum1(function* end, function** env, memstruct* m){
		function* ret = Null_ptr;
		int s = env[0]->integer;
		int e = end->integer;	
		function* tmp = NULL;
		while(s < e){
			tmp = create_function(null_ptr, empty_env, 0, m);
			tmp->integer = s;
			ret = call(call(Closure8, tmp, m), ret, m);
			s += 1;
		}
		return ret;	
	}	
			
	function* enum0(function* func, function** env, memstruct* m){
		env[0] = func;
		env[1] = NULL;
		m->Temp_closure->body = enum1; my_memcpy(m->Temp_closure->env, env);
		return m->Temp_closure;
	}

function* Enum;

""")
	main_scope.append("\tEnum = create_function(enum0, empty_env, 0, m);")
	GC_code(name)
	return

def compile_reduce():
	global func_ctr
	func_ctr += 1
	definitions["reduce"] = "Reduce"
	name = "reduce"
	global_scope.append("""

	function* reduce2(function* lst, function** env, memstruct* m){
		function* op = env[0];
		function* ret = env[1];	
		while(call(Isnil, lst, m) != Closure3){
			ret = call(call(op, call(Closure11, lst, m), m), ret, m);
			lst = call(Closure14, lst, m);
		} 
		return ret;
	}

	function* reduce1(function* initial, function** env, memstruct* m){
		env[1] = initial; env[2] = NULL;
		m->Temp_closure->body = reduce2; my_memcpy(m->Temp_closure->env, env);
		return m->Temp_closure;	
}
	function* reduce0(function* op, function** env, memstruct* m){
		env[0] = op;
		env[1] = NULL;
		m->Temp_closure->body = reduce1; my_memcpy(m->Temp_closure->env, env);
		return m->Temp_closure;
	}

function* Reduce;

""")
	main_scope.append("\tReduce = create_function(reduce0, empty_env, 0, m);")
	GC_code(name)
	return

def compile_reverse():
	global func_ctr
	func_ctr += 1
	definitions["reverse"] = "Reverse"
	name = "reverse"
	global_scope.append("""
			
	function* reverse_func(function* lst, function** env, memstruct* m){
		env[0] = lst;
		env[1] = NULL;
		function* ret = Null_ptr;
		while(call(Isnil, lst, m) != Closure3){
			ret = call(call(Closure8, call(Closure11, lst, m), m), ret, m);
			lst = call(Closure14, lst, m);
		}
		return ret;	
	}	

function* Reverse;

""")
	main_scope.append("\tReverse = create_function(reverse_func, empty_env, 0, m);")
	GC_code(name)
	return

def compile_length():
	global func_ctr
	func_ctr += 1
	definitions["length"] = "Length"
	name = "length"
	global_scope.append("""
			
	function* length_func(function* lst, function** env, memstruct* m){
		env[0] = lst;
		env[1] = NULL;
		int tmp = 0;
		while(call(Isnil, lst, m) != Closure3){
			lst = call(Closure14, lst, m);
			tmp += 1;
		}
		function* ret = create_function(null_ptr, empty_env, 0, m);
		ret->integer = tmp;
		return ret;	
	}	

function* Length;

""")
	main_scope.append("\tLength = create_function(length_func, empty_env, 0, m);")
	GC_code(name)
	return

def compile_list_ref():
	global func_ctr
	func_ctr += 1
	definitions["list-ref"] = "List_ref"
	name = "list-ref"
	global_scope.append("""
	function* list_ref1(function* index, function** env, memstruct* m){
		function* lst = env[0];
		int ctr = 0;	
		int i = index->integer;
		while(call(Isnil, lst, m) != Closure3){
			if(ctr == i)
				return call(Closure11, lst, m);
			lst = call(Closure14, lst, m);
			ctr++;
		}
		return Null_ptr;	
	}	
			
	function* list_ref0(function* func, function** env, memstruct* m){
		env[0] = func;
		env[1] = NULL;
		m->Temp_closure->body = list_ref1; my_memcpy(m->Temp_closure->env, env);
		return m->Temp_closure;
	}

function* List_ref;

""")	
	main_scope.append("\tList_ref = create_function(list_ref0, empty_env, 0, m);")
	GC_code(name)
	return

def compile_map():
	global func_ctr
	func_ctr += 1
	definitions["map"] = "Map"
	name = "map"
	global_scope.append("""
	function* map1(function* lst, function** env, memstruct* m){
		function* func = env[0];
		function* ret = Null_ptr;	
		while(call(Isnil, lst, m) != Closure3){
			ret = call(call(Closure8, call(func, call(Closure11, lst, m), m), m), ret, m);
			lst = call(Closure14, lst, m);
		}
		return ret;	
	}	
			
	function* map0(function* func, function** env, memstruct* m){
		env[0] = func;
		env[1] = NULL;
		m->Temp_closure->body = map1; my_memcpy(m->Temp_closure->env, env);
		return m->Temp_closure;
	}

function* Map;

""")
	main_scope.append("\tMap = create_function(map0, empty_env, 0, m);")
	GC_code(name)
	return

def compile_filter():
	global func_ctr
	func_ctr += 1
	definitions["filter"] = "Filter"
	name = "filter"
	global_scope.append("""
	function* filter1(function* lst, function** env, memstruct* m){
		function* func = env[0];
		function* ret = Null_ptr;	
		function* car = NULL;
		while(call(Isnil, lst, m) != Closure3){
			car = call(Closure11, lst, m);
			if(call(func, car, m)->body == closure3)
				ret = call(call(Closure8, car, m), ret, m);	
			lst = call(Closure14, lst, m);
		}
		return ret;	
	}	
			
	function* filter0(function* func, function** env, memstruct* m){
		env[0] = func;
		env[1] = NULL;
		m->Temp_closure->body = filter1; my_memcpy(m->Temp_closure->env, env);
		return m->Temp_closure;
	}

function* Filter;

""")
	main_scope.append("\tFilter = create_function(filter0, empty_env, 0, m);")
	GC_code(name)
	return

def compile_if():
	global func_ctr
	func_ctr += 1
	definitions["if"] = "If"
	name = "if"
	global_scope.append("""
function* if2(function* var2, function** env, memstruct* m){
	function* var0 = env[0];
	function* var1 = env[1];
	env[2] = var2; env[3] = NULL;
	if(var0->body == closure3)
		return call(var1, Null_ptr, m);
	return call(var2, Null_ptr, m);
}

function* if1(function* cons, function** env, memstruct* m){
	env[1] = cons; env[2] = NULL;
	m->Temp_closure->body = if2; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;	
}

function* if0(function* pred, function** env, memstruct* m){
	env[0] = pred; env[1] = NULL;
	m->Temp_closure->body = if1; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
function* If;
""")
	main_scope.append("\tIf = create_function(if0, empty_env, 0, m);")
	GC_code(name)
	return

def compile_zero():
	global func_ctr
	func_ctr += 1
	name = "0"
	definitions[name] = "Zero"
	global_scope.append("function* Zero;")
	main_scope.append("\tZero = create_function(null_ptr, empty_env, 0, m);")
	main_scope.append("\tZero->integer = 0;")
	GC_code(name)
	return
	 
def compile_one():
	global func_ctr
	func_ctr += 1
	name = "1"
	definitions[name] = "One"
	global_scope.append("function* One;")
	main_scope.append("\tOne = create_function(null_ptr, empty_env, 1, m);")
	main_scope.append("\tOne->integer = 1;")
	GC_code(name)	
	return
	
def compile_plus():
	global func_ctr
	func_ctr += 1
	name = "+"
	definitions[name] = "Plus"
	global_scope.append("""
function* plus_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	function* ret = create_function(null_ptr, empty_env, 1, m);
	ret->integer = (var0->integer + f->integer);
	return ret; 
}

function* plus(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = plus_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
""")
	global_scope.append("function* Plus;")
	main_scope.append("\tPlus = create_function(plus, empty_env, 0, m);")
	GC_code(name)	
	return

def compile_div():
	global func_ctr
	func_ctr += 1
	name = "/"
	definitions[name] = "Div"
	global_scope.append("""
function* div_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	function* ret = create_function(null_ptr, empty_env, 1, m);
	ret->integer = (var0->integer / f->integer);
	return ret; 
}

function* divide(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = div_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
""")
	global_scope.append("function* Div;")
	main_scope.append("\tDiv = create_function(divide, empty_env, 0, m);")
	GC_code(name)	
	return

def compile_mod():
	global func_ctr
	func_ctr += 1
	name = "%"
	definitions[name] = "Mod"
	global_scope.append("""
function* mod_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	function* ret = create_function(null_ptr, empty_env, 1, m);
	ret->integer = (var0->integer % f->integer);
	return ret; 
}

function* mod(function* f, function** env, memstruct* m){
	env[0] = f;
	env[1] = NULL;
	m->Temp_closure->body = mod_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
""")
	global_scope.append("function* Mod;")
	main_scope.append("\tMod = create_function(mod, empty_env, 0, m);")
	GC_code(name)
	return

def compile_expt():
	global func_ctr
	func_ctr += 1
	name = "expt"
	definitions[name] = "Expt"
	global_scope.append("""
function* expt_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	function* ret = create_function(null_ptr, empty_env, 1, m);
	ret->integer = (int)pow(var0->integer, f->integer);
	return ret; 
}

function* expt(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = expt_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
""")
	global_scope.append("function* Expt;")
	main_scope.append("\tExpt = create_function(expt, empty_env, 0, m);")
	GC_code(name)	
	return	

def compile_times():
	global func_ctr
	func_ctr += 1
	name = "*"
	definitions[name] = "Times"
	global_scope.append("""
function* times_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	function* ret = create_function(null_ptr, empty_env, 1, m);
	ret->integer = (var0->integer * f->integer);
	return ret; 
}

function* times(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = times_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
""")
	global_scope.append("function* Times;")
	main_scope.append("\tTimes = create_function(times, empty_env, 0, m);")
	GC_code(name)	
	return		

def compile_minus():
	global func_ctr
	func_ctr += 1
	name = "-"
	definitions[name] = "Minus"
	global_scope.append("""
function* minus_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	function* ret = create_function(null_ptr, empty_env, 1, m);
	ret->integer = (var0->integer - f->integer);
	return ret; 
}

function* minus(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = minus_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
""")
	global_scope.append("function* Minus;")
	main_scope.append("\tMinus = create_function(minus, empty_env, 0, m);")
	GC_code(name)
	return	

def compile_equals():
	global func_ctr
	func_ctr += 1
	name = "="
	definitions[name] = "Equals"
	global_scope.append("""
function* equals_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	if (var0->integer == f->integer)
		return Closure3;
	return Closure5;
}

function* equals(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = equals_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
""")
	global_scope.append("function* Equals;")
	main_scope.append("\tEquals = create_function(equals, empty_env, 0, m);")
	GC_code(name)	
	return	

def compile_LEQ():
	global func_ctr
	func_ctr += 1
	name = "<="
	definitions[name] = "Leq"
	global_scope.append("""
function* leq_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	if (var0->integer <= f->integer)
		return Closure3;
	return Closure5;
}

function* leq(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	my_memcpy(m->Temp_closure->env, env); m->Temp_closure->body = leq_closure;
	return m->Temp_closure;
}
""")
	global_scope.append("function* Leq;")
	main_scope.append("\tLeq = create_function(leq, empty_env, 0, m);")
	GC_code(name)	
	return	

def compile_GEQ():
	global func_ctr
	func_ctr += 1
	name = ">="
	definitions[name] = "Geq"
	global_scope.append("""
function* geq_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	if (var0->integer >= f->integer)
		return Closure3;
	return Closure5;
}

function* geq(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = geq_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
""")
	global_scope.append("function* Geq;")
	main_scope.append("\tGeq = create_function(geq, empty_env, 0, m);")
	GC_code(name)	
	return	

def compile_GT():
	global func_ctr
	func_ctr += 1
	name = ">"
	definitions[name] = "Gt"
	global_scope.append("""
function* gt_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	if (var0->integer > f->integer)
		return Closure3;
	return Closure5;
}

function* gt(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = gt_closure; my_memcpy(m->Temp_closure->env, env);;
	return m->Temp_closure;
}
""")
	global_scope.append("function* Gt;")
	main_scope.append("\tGt = create_function(gt, empty_env, 0, m);")
	GC_code(name)	
	return	

def compile_LT():
	global func_ctr
	func_ctr += 1
	name = "<"
	definitions[name] = "Lt"
	global_scope.append("""
function* lt_closure(function* f, function** env, memstruct* m){
	function* var0 = env[0];
	if (var0->integer < f->integer)
		return Closure3;
	return Closure5;
}

function* lt(function* f, function** env, memstruct* m){
	env[0] = f; env[1] = NULL;
	m->Temp_closure->body = lt_closure; my_memcpy(m->Temp_closure->env, env);;
	return m->Temp_closure;
}
""")
	global_scope.append("function* Lt;")
	main_scope.append("\tLt = create_function(lt, empty_env, 0, m);")
	GC_code(name)
	return	

def compile_nil():
	global func_ctr
	func_ctr += 1
	definitions["nil"] = "Null_ptr"
	name = "nil"
	global_scope.append("""function* Null_ptr;

function* null_ptr(function* f, function** env, memstruct* m){
	return NULL;	
}
""")
	main_scope.append("\tNull_ptr = create_function(null_ptr, empty_env, 0, m);")
	GC_code(name)	

def compile_stdin():
	global func_ctr
	func_ctr += 1
	definitions["stdin"] = "Stdin"
	name = "stdin"
	global_scope.append("function* Stdin;")
	main_scope.append("\tStdin = create_function(null_ptr, empty_env, 1, m);")
	main_scope.append("\tStdin->integer = 1;")
	GC_code(name)

def compile_stdout():
	global func_ctr
	func_ctr += 1
	definitions["stdout"] = "Stdout"
	name = "stdout"
	global_scope.append("function* Stdout;")
	main_scope.append("\tStdout = create_function(null_ptr, empty_env, 1, m);")
	main_scope.append("\tStdout->integer = 0;")
	GC_code(name)	

def compile_isnil():
	global func_ctr
	func_ctr += 1
	definitions["isnil"] = "Isnil"
	name = "isnil"
	global_scope.append("""function* Isnil;

function* isnil(function* f, function** env, memstruct* m){
	if(f == Null_ptr)
		return Closure3;
	return Closure5;
}""")
		
	main_scope.append("\tIsnil = create_function(isnil, empty_env, 0, m);")
	GC_code(name)		
	return

def compile_append():
	global func_ctr
	func_ctr += 1
	name = "append"
	definitions[name] = "Append"
	global_scope.append("""
char lookup(function* f){
	return f->integer;
}

char* lst_to_str(function* lst, memstruct* m){
	int len = 0;
	char* buff;
	function* tmp = lst;
	while(call(Isnil, lst, m)->body != closure3){
		len ++;	
		lst = call(Closure14, lst, m);
	}
	buff = malloc(len+1);
	int i = 0;		
	while(i < len){
		buff[i] = lookup(call(Closure11, tmp, m));
		tmp = call(Closure14, tmp, m);
		i++;
	}
	buff[len] = '\\0';
	return buff;
}

function* myappend_closure(function* input, function** env, memstruct* m){
	function* filename = env[0];
	char* fname = lst_to_str(filename, m);

	char* inp = lst_to_str(input, m);
	int len = strlen(inp);
	
	FILE* fp = fopen(fname, "a");
	fwrite(inp, 1, len, fp);
	fclose(fp);
	
	free(fname);
	free(inp);
	return input;
	
}

function* myappend(function* filename, function** env, memstruct* m){
	env[0] = filename; env[1] = NULL;
	function* Append_closure = create_function(myappend_closure, env, 0, m);
	return Append_closure;
}	
 
function* Append;

""")
	main_scope.append("\tAppend = create_function(myappend, empty_env, 0, m);")
	GC_code(name)		
	return

def compile_write():
	global func_ctr
	func_ctr += 1
	name = "write"
	definitions[name] = "Write"
	global_scope.append("""
function* write_to_stdout(function* input, function** env, memstruct* m){
	function* tmp = input;
	while(call(Isnil, tmp, m)->body != closure3){
		printf(\"%c\",lookup(call(Closure11, tmp, m)));
		tmp = call(Closure14, tmp, m);
	}
	return input;
}

function* mywrite_closure(function* input, function** env, memstruct* m){
	function* filename = env[0];
	if(filename->integer == 0)
		return write_to_stdout(input, env, m);
	char* fname = lst_to_str(filename, m);

	char* inp = lst_to_str(input, m);
	int len = strlen(inp);
	
	FILE* fp = fopen(fname, "w");
	fwrite(inp, 1, len, fp);
	fclose(fp);
	
	free(fname);
	free(inp);
	return input;
	
}

function* mywrite(function* filename, function** env, memstruct* m){
	env[0] = filename; env[1] = NULL;
	function* Write_closure = create_function(mywrite_closure, env, 0, m);
	return Write_closure;
}	
 
function* Write;

""")
	main_scope.append("\tWrite = create_function(mywrite, empty_env, 0, m);")
	GC_code(name)		
	return

def compile_read():
	global func_ctr
	func_ctr += 1
	name = "read"
	definitions[name] = "Read"
	global_scope.append("""
function* reverse_lookup(char x){
	int i;
	for(i=0;i<128;i++){
		if(i == x)
			return ascii_table[i];
	}
	return Null_ptr;
}

function* read_from_stdin(function* f, function** env, memstruct* m){
	char c = getchar();
	function* ret = Null_ptr;
	while(c != EOF){
		ret = call(call(Closure8, reverse_lookup(c), m), ret, m);	
		c = getchar();
	}
	function* tmp = Null_ptr;
	function* car;
	while(call(Isnil, ret, m)->body != closure3){
		car = call(Closure11, ret, m);
		tmp = call(call(Closure8, car, m), tmp, m);
		ret = call(Closure14, ret, m);
	}	
	return tmp;
}
	
function* myread_closure(function* f, function** env, memstruct* m){
	int chunk_size = 100;
	int nread = 0;
	int i;
	function* filename = env[0];
	if(filename->integer == 1)		
		return read_from_stdin(f, env, m);
	char* fname = lst_to_str(filename, m);
	FILE* fp = fopen(fname, "r");
	char buffer[chunk_size];
	nread = fread(buffer, 1, chunk_size, fp);
	function* ret = Null_ptr;
	while(nread != 0){
		for(i=nread-1;i>-1;i--)
			ret = call(call(Closure8, reverse_lookup(buffer[i]), m), ret, m);
		
		nread = fread(buffer, 1, chunk_size, fp);
	}	
	fclose(fp);
	free(fname);		
	return ret;
}

function* myread(function* filename, function** env, memstruct* m){
	env[0] = filename; env[1] = NULL;
	function* Read_closure = create_function(myread_closure, env, 0, m);
	return Read_closure;
}

function* Read;			
""")
	main_scope.append("\tRead = create_function(myread, empty_env, 0, m);")
	GC_code(name)		
	return	

def compile_print_num():
	global func_ctr;
	func_ctr += 1
	name = "print-num"
	definitions[name] = "Print_num"
	global_scope.append("""
function* print_num(function* f, function** env, memstruct* m){
	printf("%d",f->integer);
	return f;
}

function* Print_num;
""")
	main_scope.append("\tPrint_num = create_function(print_num, empty_env, 1, m);")
	GC_code(name)		
	return	

def compile_print_char():
	global func_ctr;
	func_ctr += 1
	name = "print-char"
	definitions[name] = "Print_char"
	global_scope.append("""
function* print_char(function* f, function** env, memstruct* m){
	printf("%c",f->integer);
	return f;
}

function* Print_char;
""")
	main_scope.append("\tPrint_char = create_function(print_char, empty_env, 1, m);")
	GC_code(name)		
	return	

def compile_or():
	global func_ctr
	func_ctr += 1
	name = "or"
	definitions[name] = "Or"
	global_scope.append("""
int is_true(function *f){
	return f->body != closure5;
}
function* or_closure(function* var1, function** env, memstruct* m){
	function* var0 = env[0];
	if(is_true(var0) || is_true(var1))
		return Closure3;
	return Closure5;
}

function* or_func(function* f, function** env, memstruct* m){
	env[0] = f;	
	env[1] = NULL;
	m->Temp_closure->body = or_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
function* Or;

""")
	main_scope.append("\tOr = create_function(or_func, empty_env, 0, m);")
	GC_code(name)		
	return

def compile_and():
	global func_ctr
	func_ctr += 1
	name = "and"
	definitions[name] = "And"
	global_scope.append("""

function* and_closure(function* var1, function** env, memstruct* m){
	function* var0 = env[0];
	if(is_true(var0) && is_true(var1))
		return Closure3;
	return Closure5;
}

function* and_func(function* f, function** env, memstruct* m){
	env[0] = f;	
	env[1] = NULL;
	m->Temp_closure->body = and_closure; my_memcpy(m->Temp_closure->env, env);
	return m->Temp_closure;
}
function* And;

""")
	main_scope.append("\tAnd = create_function(and_func, empty_env, 0, m);")
	GC_code(name)		
	return

init()
compile_func("(define true (@ a (@ b a)))")
compile_func("(define false (@ a (@ b b)))")
compile_func("(define identity (@ x x))")
compile_func("(define pair (@ x (@ y (@ z ((z x) y)))))")
compile_func("(define first (@ p (p (@ x (@ y x)))))")
compile_func("(define second (@ p (p (@ x (@ y y)))))")
compile_nil()
compile_isnil()
compile_if()
compile_map()
compile_enum()
compile_filter()
compile_reduce()
compile_reverse()
compile_length()
compile_list_ref()
compile_stdin()
compile_stdout()
compile_append()
compile_write()
compile_read()
compile_print_num()
compile_print_char()	
compile_zero()
compile_one()
compile_plus()
compile_expt()
compile_times()
compile_minus()
compile_equals()
compile_LEQ()
compile_GEQ()
compile_GT()
compile_LT()
compile_div()
compile_mod()
compile_or()
compile_and()

for i in range(2, 128):
	compile_func("(define %d ((+ 1) %d))"%(i, (i-1)))	
fill_ascii_table()
compile_func("(define not (@ p (@ a (@ b ((p b) a)))))")
compile_func("(define newline (@ x (print-char 10)))")
compile_func("(define pred (@ x ((- x) 1)))")

#for i in global_scope:
#	print(i)
#for i in outro():
#	print(i)


