

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


function* Closure3;
function* closure4(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	function* var0 = env[0];
	return var0;}

function* closure3(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure4 = create_function(closure4, env, 0, m);
	return Closure4;}

function* Closure5;
function* closure6(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	return var1;}

function* closure5(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure6 = create_function(closure6, env, 0, m);
	return Closure6;}

function* Closure7;
function* closure7(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	return var0;}

function* Closure8;
function* closure10(function* var2,function** env, memstruct* m){
	env[2] = var2;
	env[3] = NULL;
	function* var1 = env[1];
	function* var0 = env[0];
	return call(call(var2, var0, m), var1, m);}
function* closure9(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	function* Closure10 = create_function(closure10, env, 0, m);
	return Closure10;}

function* closure8(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure9 = create_function(closure9, env, 0, m);
	return Closure9;}

function* Closure11;
function* closure13(function* var2,function** env, memstruct* m){
	env[2] = var2;
	env[3] = NULL;
	function* var1 = env[1];
	return var1;}

function* closure12(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	function* Closure13 = create_function(closure13, env, 0, m);
	return Closure13;}

function* closure11(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure12 = create_function(closure12, env, 0, m);
	return call(var0, Closure12, m);}
function* Closure14;
function* closure16(function* var2,function** env, memstruct* m){
	env[2] = var2;
	env[3] = NULL;
	return var2;}

function* closure15(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	function* Closure16 = create_function(closure16, env, 0, m);
	return Closure16;}

function* closure14(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure15 = create_function(closure15, env, 0, m);
	return call(var0, Closure15, m);}
function* Null_ptr;

function* null_ptr(function* f, function** env, memstruct* m){
	return NULL;	
}

function* Isnil;

function* isnil(function* f, function** env, memstruct* m){
	if(f == Null_ptr)
		return Closure3;
	return Closure5;
}

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


function* Stdin;
function* Stdout;

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
	buff[len] = '\0';
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



function* write_to_stdout(function* input, function** env, memstruct* m){
	function* tmp = input;
	while(call(Isnil, tmp, m)->body != closure3){
		printf("%c",lookup(call(Closure11, tmp, m)));
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


function* print_num(function* f, function** env, memstruct* m){
	printf("%d",f->integer);
	return f;
}

function* Print_num;


function* print_char(function* f, function** env, memstruct* m){
	printf("%c",f->integer);
	return f;
}

function* Print_char;

function* Zero;
function* One;

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

function* Plus;

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

function* Expt;

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

function* Times;

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

function* Minus;

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

function* Equals;

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

function* Leq;

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

function* Geq;

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

function* Gt;

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

function* Lt;

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

function* Div;

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

function* Mod;

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


function* var_6400019251;
function* var_6528019634;
function* var_6656020021;
function* var_6784020404;
function* var_6912020791;
function* var_7040021174;
function* var_7168021561;
function* var_7296021944;
function* var_6272037681056609;
function* var_6272037681056608;
function* var_6272037681056611;
function* var_6272037681056610;
function* var_6272037681056613;
function* var_6272037681056612;
function* var_6272037681056615;
function* var_6272037681056614;
function* var_6272037681056617;
function* var_6272037681056616;
function* var_6400038450057764;
function* var_6400038450057765;
function* var_6400038450057766;
function* var_6400038450057767;
function* var_6400038450057760;
function* var_6400038450057761;
function* var_6400038450057762;
function* var_6400038450057763;
function* var_6400038450057772;
function* var_6400038450057773;
function* var_6528039219058923;
function* var_6528039219058922;
function* var_6528039219058921;
function* var_6528039219058920;
function* var_6528039219058927;
function* var_6528039219058926;
function* var_6528039219058925;
function* var_6528039219058924;
function* var_6528039219058915;
function* var_6528039219058914;
function* var_6656039988060078;
function* var_6656039988060079;
function* var_6656039988060076;
function* var_6656039988060077;
function* var_6656039988060074;
function* var_6656039988060075;
function* var_6656039988060072;
function* var_6656039988060073;
function* var_6656039988060070;
function* var_6656039988060071;
function* var_6784040757061229;
function* var_6784040757061228;
function* var_6784040757061231;
function* var_6784040757061230;
function* var_6784040757061225;
function* var_6784040757061224;
function* var_6784040757061227;
function* var_6784040757061226;
function* var_6784040757061221;
function* var_6784040757061220;
function* var_6912041526062352;
function* var_6912041526062353;
function* var_6912041526062354;
function* var_6912041526062355;
function* var_6912041526062356;
function* var_6912041526062357;
function* var_6912041526062358;
function* var_6912041526062359;
function* var_6912041526062360;
function* var_6912041526062361;
function* var_7040042295063511;
function* var_7040042295063510;
function* var_7040042295063509;
function* var_7040042295063508;
function* var_7040042295063507;
function* var_7040042295063506;
function* var_7040042295063505;
function* var_7040042295063504;
function* var_7040042295063519;
function* var_7040042295063518;
function* var_7168043064064666;
function* var_7168043064064667;
function* var_7168043064064664;
function* var_7168043064064665;
function* var_7168043064064670;
function* var_7168043064064671;
function* var_7168043064064668;
function* var_7168043064064669;
function* var_7168043064064658;
function* var_7168043064064659;
function* var_7296043833065817;
function* var_7296043833065816;
function* var_7296043833065819;
function* var_7296043833065818;
function* var_7296043833065821;
function* var_7296043833065820;
function* var_7296043833065823;
function* var_7296043833065822;
function* var_7296043833065809;
function* var_7296043833065808;
function* var_163512108406620378;
function* var_163512108406620379;
function* var_163512108406620376;
function* var_163512108406620377;
function* var_163512108406620382;
function* var_163512108406620383;
function* var_163512108406620380;
function* var_163512108406620381;
function* var_163512108406620370;
function* var_163512108406620371;
function* var_163512108405620373;
function* var_163512108405620372;
function* var_163512108405620375;
function* var_163512108405620374;
function* var_163512108405620369;
function* var_163512108405620368;
function* var_163512108405620371;
function* var_163512108405620370;
function* var_163512108405620381;
function* var_163512108405620380;
function* var_163512108404620368;
function* var_163512108404620369;
function* var_163512108404620370;
function* var_163512108404620371;
function* var_163512108404620372;
function* var_163512108404620373;
function* var_163512108404620374;
function* var_163512108404620375;
function* Closure49;
function* closure51(function* var2,function** env, memstruct* m){
	env[2] = var2;
	env[3] = NULL;
	function* var1 = env[1];
	function* var0 = env[0];
	return call(call(var0, var2, m), var1, m);}
function* closure50(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	function* Closure51 = create_function(closure51, env, 0, m);
	return Closure51;}

function* closure49(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure50 = create_function(closure50, env, 0, m);
	return Closure50;}

function* Closure52;
function* closure52(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	return call(Print_char, var_6272037681056609, m);}
function* Closure53;
function* closure53(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	return call(call(Minus, var0, m), One, m);}
function* Closure54;
function* closure56(function* var2,function** env, memstruct* m){
	env[2] = var2;
	env[3] = NULL;
	return Closure3;}

function* closure58(function* var3,function** env, memstruct* m){
	env[3] = var3;
	env[4] = NULL;
	return Closure5;}

function* closure60(function* var4,function** env, memstruct* m){
	env[4] = var4;
	env[5] = NULL;
	function* var1 = env[1];
	function* var0 = env[0];
	return call(call(Closure54, var0, m), call(call(Minus, var1, m), One, m), m);}
function* closure61(function* var4,function** env, memstruct* m){
	env[4] = var4;
	env[5] = NULL;
	return Null_ptr;}

function* closure59(function* var3,function** env, memstruct* m){
	env[3] = var3;
	env[4] = NULL;
	function* Closure60 = create_function(closure60, env, 0, m);
	function* Closure61 = create_function(closure61, env, 0, m);
	return call(call(call(If, Closure3, m), Closure60, m), Closure61, m);}
function* closure57(function* var2,function** env, memstruct* m){
	env[2] = var2;
	env[3] = NULL;
	function* var1 = env[1];
	function* var0 = env[0];
	function* Closure58 = create_function(closure58, env, 0, m);
	function* Closure59 = create_function(closure59, env, 0, m);
	return call(call(call(If, call(call(Equals, call(call(Mod, var0, m), var1, m), m), Zero, m), m), Closure58, m), Closure59, m);}
function* closure55(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	function* Closure56 = create_function(closure56, env, 0, m);
	function* Closure57 = create_function(closure57, env, 0, m);
	return call(call(call(If, call(call(Equals, var1, m), One, m), m), Closure56, m), Closure57, m);}
function* closure54(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure55 = create_function(closure55, env, 0, m);
	return Closure55;}

function* Closure62;
function* closure62(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	return call(call(Closure54, var0, m), call(call(Plus, call(call(Div, var0, m), var_6400019251, m), m), One, m), m);}
function* var_4991407356201764482;
function* Closure63;
function* closure66(function* var3,function** env, memstruct* m){
	env[3] = var3;
	env[4] = NULL;
	function* var2 = env[2];
	return var2;}

function* closure68(function* var4,function** env, memstruct* m){
	env[4] = var4;
	env[5] = NULL;
	function* var1 = env[1];
	function* var0 = env[0];
	function* var2 = env[2];
	return call(call(call(Closure63, call(call(Plus, One, m), var0, m), m), call(call(Plus, One, m), var1, m), m), call(call(Closure8, var1, m), var2, m), m);}
function* closure70(function* var5,function** env, memstruct* m){
	env[5] = var5;
	env[6] = NULL;
	function* var1 = env[1];
	function* var0 = env[0];
	function* var2 = env[2];
	return call(call(call(Closure63, var0, m), call(call(Plus, One, m), var1, m), m), var2, m);}
function* closure71(function* var5,function** env, memstruct* m){
	env[5] = var5;
	env[6] = NULL;
	return Null_ptr;}

function* closure69(function* var4,function** env, memstruct* m){
	env[4] = var4;
	env[5] = NULL;
	function* Closure70 = create_function(closure70, env, 0, m);
	function* Closure71 = create_function(closure71, env, 0, m);
	return call(call(call(If, Closure3, m), Closure70, m), Closure71, m);}
function* closure67(function* var3,function** env, memstruct* m){
	env[3] = var3;
	env[4] = NULL;
	function* var1 = env[1];
	function* Closure68 = create_function(closure68, env, 0, m);
	function* Closure69 = create_function(closure69, env, 0, m);
	return call(call(call(If, call(Closure62, var1, m), m), Closure68, m), Closure69, m);}
function* closure65(function* var2,function** env, memstruct* m){
	env[2] = var2;
	env[3] = NULL;
	function* var0 = env[0];
	function* Closure66 = create_function(closure66, env, 0, m);
	function* Closure67 = create_function(closure67, env, 0, m);
	return call(call(call(If, call(call(Equals, var0, m), var_4991407356201764482, m), m), Closure66, m), Closure67, m);}
function* closure64(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	function* Closure65 = create_function(closure65, env, 0, m);
	return Closure65;}

function* closure63(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure64 = create_function(closure64, env, 0, m);
	return Closure64;}

function* Closure72;
function* closure73(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	return call(Print_char, var_6272037681056609, m);}
function* closure74(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	function* var0 = env[0];
	return call(call(Or, call(Closure72, call(Closure14, var0, m), m), m), call(call(Or, call(Print_char, var_6272037681056609, m), m), call(Print_num, call(Closure11, var0, m), m), m), m);}
function* closure72(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure73 = create_function(closure73, env, 0, m);
	function* Closure74 = create_function(closure74, env, 0, m);
	return call(call(call(If, call(Isnil, var0, m), m), Closure73, m), Closure74, m);}
function* Closure75;
function* closure76(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	return call(call(Write, Stdout, m), call(call(Closure8, var_163512108405620371, m), call(call(Closure8, var_163512108405620369, m), call(call(Closure8, var_163512108405620370, m), call(call(Closure8, var_163512108406620379, m), Null_ptr, m), m), m), m), m);}
function* closure77(function* var1,function** env, memstruct* m){
	env[1] = var1;
	env[2] = NULL;
	return call(call(Write, Stdout, m), call(call(Closure8, var_163512108406620376, m), call(call(Closure8, var_7296043833065822, m), call(call(Closure8, var_163512108406620370, m), call(call(Closure8, var_163512108405620368, m), call(call(Closure8, var_163512108406620379, m), Null_ptr, m), m), m), m), m), m);}
function* closure75(function* var0,function** env, memstruct* m){
	env[0] = var0;
	env[1] = NULL;
	function* Closure76 = create_function(closure76, env, 0, m);
	function* Closure77 = create_function(closure77, env, 0, m);
	return call(call(call(If, var0, m), Closure76, m), Closure77, m);}
function* var_7876451200857581859;
function* var_2083207811319332352;
function* var_2083207811319332352;
function* var_2083207811319332352;
function* var_2083207811319332352;
function* var_2083207811319332352;
function* var_2083207811319332352;
function* var_2083207811319332352;
function* var_2083207811319332352;


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
	
	function** roots = malloc((1+175)*8);
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

	Closure3 = create_function(closure3, empty_env, 0, m);

	roots[0] = Closure3;
	roots[0] = garbage_collect(roots[0]);
	Closure3 = roots[0];
	roots[1] = NULL;
	Closure5 = create_function(closure5, empty_env, 0, m);

	roots[1] = Closure5;
	roots[1] = garbage_collect(roots[1]);
	Closure5 = roots[1];
	roots[2] = NULL;
	Closure7 = create_function(closure7, empty_env, 0, m);

	roots[2] = Closure7;
	roots[2] = garbage_collect(roots[2]);
	Closure7 = roots[2];
	roots[3] = NULL;
	Closure8 = create_function(closure8, empty_env, 0, m);

	roots[3] = Closure8;
	roots[3] = garbage_collect(roots[3]);
	Closure8 = roots[3];
	roots[4] = NULL;
	Closure11 = create_function(closure11, empty_env, 0, m);

	roots[4] = Closure11;
	roots[4] = garbage_collect(roots[4]);
	Closure11 = roots[4];
	roots[5] = NULL;
	Closure14 = create_function(closure14, empty_env, 0, m);

	roots[5] = Closure14;
	roots[5] = garbage_collect(roots[5]);
	Closure14 = roots[5];
	roots[6] = NULL;
	Null_ptr = create_function(null_ptr, empty_env, 0, m);
	roots[6] = Null_ptr;
	roots[6] = garbage_collect(roots[6]);
	Null_ptr = roots[6];
	roots[7] = NULL;
	Isnil = create_function(isnil, empty_env, 0, m);
	roots[7] = Isnil;
	roots[7] = garbage_collect(roots[7]);
	Isnil = roots[7];
	roots[8] = NULL;
	If = create_function(if0, empty_env, 0, m);
	roots[8] = If;
	roots[8] = garbage_collect(roots[8]);
	If = roots[8];
	roots[9] = NULL;
	Map = create_function(map0, empty_env, 0, m);
	roots[9] = Map;
	roots[9] = garbage_collect(roots[9]);
	Map = roots[9];
	roots[10] = NULL;
	Enum = create_function(enum0, empty_env, 0, m);
	roots[10] = Enum;
	roots[10] = garbage_collect(roots[10]);
	Enum = roots[10];
	roots[11] = NULL;
	Filter = create_function(filter0, empty_env, 0, m);
	roots[11] = Filter;
	roots[11] = garbage_collect(roots[11]);
	Filter = roots[11];
	roots[12] = NULL;
	Reduce = create_function(reduce0, empty_env, 0, m);
	roots[12] = Reduce;
	roots[12] = garbage_collect(roots[12]);
	Reduce = roots[12];
	roots[13] = NULL;
	Reverse = create_function(reverse_func, empty_env, 0, m);
	roots[13] = Reverse;
	roots[13] = garbage_collect(roots[13]);
	Reverse = roots[13];
	roots[14] = NULL;
	Length = create_function(length_func, empty_env, 0, m);
	roots[14] = Length;
	roots[14] = garbage_collect(roots[14]);
	Length = roots[14];
	roots[15] = NULL;
	List_ref = create_function(list_ref0, empty_env, 0, m);
	roots[15] = List_ref;
	roots[15] = garbage_collect(roots[15]);
	List_ref = roots[15];
	roots[16] = NULL;
	Stdin = create_function(null_ptr, empty_env, 1, m);
	Stdin->integer = 1;
	roots[16] = Stdin;
	roots[16] = garbage_collect(roots[16]);
	Stdin = roots[16];
	roots[17] = NULL;
	Stdout = create_function(null_ptr, empty_env, 1, m);
	Stdout->integer = 0;
	roots[17] = Stdout;
	roots[17] = garbage_collect(roots[17]);
	Stdout = roots[17];
	roots[18] = NULL;
	Append = create_function(myappend, empty_env, 0, m);
	roots[18] = Append;
	roots[18] = garbage_collect(roots[18]);
	Append = roots[18];
	roots[19] = NULL;
	Write = create_function(mywrite, empty_env, 0, m);
	roots[19] = Write;
	roots[19] = garbage_collect(roots[19]);
	Write = roots[19];
	roots[20] = NULL;
	Read = create_function(myread, empty_env, 0, m);
	roots[20] = Read;
	roots[20] = garbage_collect(roots[20]);
	Read = roots[20];
	roots[21] = NULL;
	Print_num = create_function(print_num, empty_env, 1, m);
	roots[21] = Print_num;
	roots[21] = garbage_collect(roots[21]);
	Print_num = roots[21];
	roots[22] = NULL;
	Print_char = create_function(print_char, empty_env, 1, m);
	roots[22] = Print_char;
	roots[22] = garbage_collect(roots[22]);
	Print_char = roots[22];
	roots[23] = NULL;
	Zero = create_function(null_ptr, empty_env, 0, m);
	Zero->integer = 0;
	roots[23] = Zero;
	roots[23] = garbage_collect(roots[23]);
	Zero = roots[23];
	roots[24] = NULL;
	One = create_function(null_ptr, empty_env, 1, m);
	One->integer = 1;
	roots[24] = One;
	roots[24] = garbage_collect(roots[24]);
	One = roots[24];
	roots[25] = NULL;
	Plus = create_function(plus, empty_env, 0, m);
	roots[25] = Plus;
	roots[25] = garbage_collect(roots[25]);
	Plus = roots[25];
	roots[26] = NULL;
	Expt = create_function(expt, empty_env, 0, m);
	roots[26] = Expt;
	roots[26] = garbage_collect(roots[26]);
	Expt = roots[26];
	roots[27] = NULL;
	Times = create_function(times, empty_env, 0, m);
	roots[27] = Times;
	roots[27] = garbage_collect(roots[27]);
	Times = roots[27];
	roots[28] = NULL;
	Minus = create_function(minus, empty_env, 0, m);
	roots[28] = Minus;
	roots[28] = garbage_collect(roots[28]);
	Minus = roots[28];
	roots[29] = NULL;
	Equals = create_function(equals, empty_env, 0, m);
	roots[29] = Equals;
	roots[29] = garbage_collect(roots[29]);
	Equals = roots[29];
	roots[30] = NULL;
	Leq = create_function(leq, empty_env, 0, m);
	roots[30] = Leq;
	roots[30] = garbage_collect(roots[30]);
	Leq = roots[30];
	roots[31] = NULL;
	Geq = create_function(geq, empty_env, 0, m);
	roots[31] = Geq;
	roots[31] = garbage_collect(roots[31]);
	Geq = roots[31];
	roots[32] = NULL;
	Gt = create_function(gt, empty_env, 0, m);
	roots[32] = Gt;
	roots[32] = garbage_collect(roots[32]);
	Gt = roots[32];
	roots[33] = NULL;
	Lt = create_function(lt, empty_env, 0, m);
	roots[33] = Lt;
	roots[33] = garbage_collect(roots[33]);
	Lt = roots[33];
	roots[34] = NULL;
	Div = create_function(divide, empty_env, 0, m);
	roots[34] = Div;
	roots[34] = garbage_collect(roots[34]);
	Div = roots[34];
	roots[35] = NULL;
	Mod = create_function(mod, empty_env, 0, m);
	roots[35] = Mod;
	roots[35] = garbage_collect(roots[35]);
	Mod = roots[35];
	roots[36] = NULL;
	Or = create_function(or_func, empty_env, 0, m);
	roots[36] = Or;
	roots[36] = garbage_collect(roots[36]);
	Or = roots[36];
	roots[37] = NULL;
	And = create_function(and_func, empty_env, 0, m);
	roots[37] = And;
	roots[37] = garbage_collect(roots[37]);
	And = roots[37];
	roots[38] = NULL;
	var_6400019251 = call(call(Plus, One, m), One, m);

	roots[38] = var_6400019251;
	roots[38] = garbage_collect(roots[38]);
	var_6400019251 = roots[38];
	roots[39] = NULL;
	var_6528019634 = call(call(Plus, One, m), var_6400019251, m);

	roots[39] = var_6528019634;
	roots[39] = garbage_collect(roots[39]);
	var_6528019634 = roots[39];
	roots[40] = NULL;
	var_6656020021 = call(call(Plus, One, m), var_6528019634, m);

	roots[40] = var_6656020021;
	roots[40] = garbage_collect(roots[40]);
	var_6656020021 = roots[40];
	roots[41] = NULL;
	var_6784020404 = call(call(Plus, One, m), var_6656020021, m);

	roots[41] = var_6784020404;
	roots[41] = garbage_collect(roots[41]);
	var_6784020404 = roots[41];
	roots[42] = NULL;
	var_6912020791 = call(call(Plus, One, m), var_6784020404, m);

	roots[42] = var_6912020791;
	roots[42] = garbage_collect(roots[42]);
	var_6912020791 = roots[42];
	roots[43] = NULL;
	var_7040021174 = call(call(Plus, One, m), var_6912020791, m);

	roots[43] = var_7040021174;
	roots[43] = garbage_collect(roots[43]);
	var_7040021174 = roots[43];
	roots[44] = NULL;
	var_7168021561 = call(call(Plus, One, m), var_7040021174, m);

	roots[44] = var_7168021561;
	roots[44] = garbage_collect(roots[44]);
	var_7168021561 = roots[44];
	roots[45] = NULL;
	var_7296021944 = call(call(Plus, One, m), var_7168021561, m);

	roots[45] = var_7296021944;
	roots[45] = garbage_collect(roots[45]);
	var_7296021944 = roots[45];
	roots[46] = NULL;
	var_6272037681056609 = call(call(Plus, One, m), var_7296021944, m);

	roots[46] = var_6272037681056609;
	roots[46] = garbage_collect(roots[46]);
	var_6272037681056609 = roots[46];
	roots[47] = NULL;
	var_6272037681056608 = call(call(Plus, One, m), var_6272037681056609, m);

	roots[47] = var_6272037681056608;
	roots[47] = garbage_collect(roots[47]);
	var_6272037681056608 = roots[47];
	roots[48] = NULL;
	var_6272037681056611 = call(call(Plus, One, m), var_6272037681056608, m);

	roots[48] = var_6272037681056611;
	roots[48] = garbage_collect(roots[48]);
	var_6272037681056611 = roots[48];
	roots[49] = NULL;
	var_6272037681056610 = call(call(Plus, One, m), var_6272037681056611, m);

	roots[49] = var_6272037681056610;
	roots[49] = garbage_collect(roots[49]);
	var_6272037681056610 = roots[49];
	roots[50] = NULL;
	var_6272037681056613 = call(call(Plus, One, m), var_6272037681056610, m);

	roots[50] = var_6272037681056613;
	roots[50] = garbage_collect(roots[50]);
	var_6272037681056613 = roots[50];
	roots[51] = NULL;
	var_6272037681056612 = call(call(Plus, One, m), var_6272037681056613, m);

	roots[51] = var_6272037681056612;
	roots[51] = garbage_collect(roots[51]);
	var_6272037681056612 = roots[51];
	roots[52] = NULL;
	var_6272037681056615 = call(call(Plus, One, m), var_6272037681056612, m);

	roots[52] = var_6272037681056615;
	roots[52] = garbage_collect(roots[52]);
	var_6272037681056615 = roots[52];
	roots[53] = NULL;
	var_6272037681056614 = call(call(Plus, One, m), var_6272037681056615, m);

	roots[53] = var_6272037681056614;
	roots[53] = garbage_collect(roots[53]);
	var_6272037681056614 = roots[53];
	roots[54] = NULL;
	var_6272037681056617 = call(call(Plus, One, m), var_6272037681056614, m);

	roots[54] = var_6272037681056617;
	roots[54] = garbage_collect(roots[54]);
	var_6272037681056617 = roots[54];
	roots[55] = NULL;
	var_6272037681056616 = call(call(Plus, One, m), var_6272037681056617, m);

	roots[55] = var_6272037681056616;
	roots[55] = garbage_collect(roots[55]);
	var_6272037681056616 = roots[55];
	roots[56] = NULL;
	var_6400038450057764 = call(call(Plus, One, m), var_6272037681056616, m);

	roots[56] = var_6400038450057764;
	roots[56] = garbage_collect(roots[56]);
	var_6400038450057764 = roots[56];
	roots[57] = NULL;
	var_6400038450057765 = call(call(Plus, One, m), var_6400038450057764, m);

	roots[57] = var_6400038450057765;
	roots[57] = garbage_collect(roots[57]);
	var_6400038450057765 = roots[57];
	roots[58] = NULL;
	var_6400038450057766 = call(call(Plus, One, m), var_6400038450057765, m);

	roots[58] = var_6400038450057766;
	roots[58] = garbage_collect(roots[58]);
	var_6400038450057766 = roots[58];
	roots[59] = NULL;
	var_6400038450057767 = call(call(Plus, One, m), var_6400038450057766, m);

	roots[59] = var_6400038450057767;
	roots[59] = garbage_collect(roots[59]);
	var_6400038450057767 = roots[59];
	roots[60] = NULL;
	var_6400038450057760 = call(call(Plus, One, m), var_6400038450057767, m);

	roots[60] = var_6400038450057760;
	roots[60] = garbage_collect(roots[60]);
	var_6400038450057760 = roots[60];
	roots[61] = NULL;
	var_6400038450057761 = call(call(Plus, One, m), var_6400038450057760, m);

	roots[61] = var_6400038450057761;
	roots[61] = garbage_collect(roots[61]);
	var_6400038450057761 = roots[61];
	roots[62] = NULL;
	var_6400038450057762 = call(call(Plus, One, m), var_6400038450057761, m);

	roots[62] = var_6400038450057762;
	roots[62] = garbage_collect(roots[62]);
	var_6400038450057762 = roots[62];
	roots[63] = NULL;
	var_6400038450057763 = call(call(Plus, One, m), var_6400038450057762, m);

	roots[63] = var_6400038450057763;
	roots[63] = garbage_collect(roots[63]);
	var_6400038450057763 = roots[63];
	roots[64] = NULL;
	var_6400038450057772 = call(call(Plus, One, m), var_6400038450057763, m);

	roots[64] = var_6400038450057772;
	roots[64] = garbage_collect(roots[64]);
	var_6400038450057772 = roots[64];
	roots[65] = NULL;
	var_6400038450057773 = call(call(Plus, One, m), var_6400038450057772, m);

	roots[65] = var_6400038450057773;
	roots[65] = garbage_collect(roots[65]);
	var_6400038450057773 = roots[65];
	roots[66] = NULL;
	var_6528039219058923 = call(call(Plus, One, m), var_6400038450057773, m);

	roots[66] = var_6528039219058923;
	roots[66] = garbage_collect(roots[66]);
	var_6528039219058923 = roots[66];
	roots[67] = NULL;
	var_6528039219058922 = call(call(Plus, One, m), var_6528039219058923, m);

	roots[67] = var_6528039219058922;
	roots[67] = garbage_collect(roots[67]);
	var_6528039219058922 = roots[67];
	roots[68] = NULL;
	var_6528039219058921 = call(call(Plus, One, m), var_6528039219058922, m);

	roots[68] = var_6528039219058921;
	roots[68] = garbage_collect(roots[68]);
	var_6528039219058921 = roots[68];
	roots[69] = NULL;
	var_6528039219058920 = call(call(Plus, One, m), var_6528039219058921, m);

	roots[69] = var_6528039219058920;
	roots[69] = garbage_collect(roots[69]);
	var_6528039219058920 = roots[69];
	roots[70] = NULL;
	var_6528039219058927 = call(call(Plus, One, m), var_6528039219058920, m);

	roots[70] = var_6528039219058927;
	roots[70] = garbage_collect(roots[70]);
	var_6528039219058927 = roots[70];
	roots[71] = NULL;
	var_6528039219058926 = call(call(Plus, One, m), var_6528039219058927, m);

	roots[71] = var_6528039219058926;
	roots[71] = garbage_collect(roots[71]);
	var_6528039219058926 = roots[71];
	roots[72] = NULL;
	var_6528039219058925 = call(call(Plus, One, m), var_6528039219058926, m);

	roots[72] = var_6528039219058925;
	roots[72] = garbage_collect(roots[72]);
	var_6528039219058925 = roots[72];
	roots[73] = NULL;
	var_6528039219058924 = call(call(Plus, One, m), var_6528039219058925, m);

	roots[73] = var_6528039219058924;
	roots[73] = garbage_collect(roots[73]);
	var_6528039219058924 = roots[73];
	roots[74] = NULL;
	var_6528039219058915 = call(call(Plus, One, m), var_6528039219058924, m);

	roots[74] = var_6528039219058915;
	roots[74] = garbage_collect(roots[74]);
	var_6528039219058915 = roots[74];
	roots[75] = NULL;
	var_6528039219058914 = call(call(Plus, One, m), var_6528039219058915, m);

	roots[75] = var_6528039219058914;
	roots[75] = garbage_collect(roots[75]);
	var_6528039219058914 = roots[75];
	roots[76] = NULL;
	var_6656039988060078 = call(call(Plus, One, m), var_6528039219058914, m);

	roots[76] = var_6656039988060078;
	roots[76] = garbage_collect(roots[76]);
	var_6656039988060078 = roots[76];
	roots[77] = NULL;
	var_6656039988060079 = call(call(Plus, One, m), var_6656039988060078, m);

	roots[77] = var_6656039988060079;
	roots[77] = garbage_collect(roots[77]);
	var_6656039988060079 = roots[77];
	roots[78] = NULL;
	var_6656039988060076 = call(call(Plus, One, m), var_6656039988060079, m);

	roots[78] = var_6656039988060076;
	roots[78] = garbage_collect(roots[78]);
	var_6656039988060076 = roots[78];
	roots[79] = NULL;
	var_6656039988060077 = call(call(Plus, One, m), var_6656039988060076, m);

	roots[79] = var_6656039988060077;
	roots[79] = garbage_collect(roots[79]);
	var_6656039988060077 = roots[79];
	roots[80] = NULL;
	var_6656039988060074 = call(call(Plus, One, m), var_6656039988060077, m);

	roots[80] = var_6656039988060074;
	roots[80] = garbage_collect(roots[80]);
	var_6656039988060074 = roots[80];
	roots[81] = NULL;
	var_6656039988060075 = call(call(Plus, One, m), var_6656039988060074, m);

	roots[81] = var_6656039988060075;
	roots[81] = garbage_collect(roots[81]);
	var_6656039988060075 = roots[81];
	roots[82] = NULL;
	var_6656039988060072 = call(call(Plus, One, m), var_6656039988060075, m);

	roots[82] = var_6656039988060072;
	roots[82] = garbage_collect(roots[82]);
	var_6656039988060072 = roots[82];
	roots[83] = NULL;
	var_6656039988060073 = call(call(Plus, One, m), var_6656039988060072, m);

	roots[83] = var_6656039988060073;
	roots[83] = garbage_collect(roots[83]);
	var_6656039988060073 = roots[83];
	roots[84] = NULL;
	var_6656039988060070 = call(call(Plus, One, m), var_6656039988060073, m);

	roots[84] = var_6656039988060070;
	roots[84] = garbage_collect(roots[84]);
	var_6656039988060070 = roots[84];
	roots[85] = NULL;
	var_6656039988060071 = call(call(Plus, One, m), var_6656039988060070, m);

	roots[85] = var_6656039988060071;
	roots[85] = garbage_collect(roots[85]);
	var_6656039988060071 = roots[85];
	roots[86] = NULL;
	var_6784040757061229 = call(call(Plus, One, m), var_6656039988060071, m);

	roots[86] = var_6784040757061229;
	roots[86] = garbage_collect(roots[86]);
	var_6784040757061229 = roots[86];
	roots[87] = NULL;
	var_6784040757061228 = call(call(Plus, One, m), var_6784040757061229, m);

	roots[87] = var_6784040757061228;
	roots[87] = garbage_collect(roots[87]);
	var_6784040757061228 = roots[87];
	roots[88] = NULL;
	var_6784040757061231 = call(call(Plus, One, m), var_6784040757061228, m);

	roots[88] = var_6784040757061231;
	roots[88] = garbage_collect(roots[88]);
	var_6784040757061231 = roots[88];
	roots[89] = NULL;
	var_6784040757061230 = call(call(Plus, One, m), var_6784040757061231, m);

	roots[89] = var_6784040757061230;
	roots[89] = garbage_collect(roots[89]);
	var_6784040757061230 = roots[89];
	roots[90] = NULL;
	var_6784040757061225 = call(call(Plus, One, m), var_6784040757061230, m);

	roots[90] = var_6784040757061225;
	roots[90] = garbage_collect(roots[90]);
	var_6784040757061225 = roots[90];
	roots[91] = NULL;
	var_6784040757061224 = call(call(Plus, One, m), var_6784040757061225, m);

	roots[91] = var_6784040757061224;
	roots[91] = garbage_collect(roots[91]);
	var_6784040757061224 = roots[91];
	roots[92] = NULL;
	var_6784040757061227 = call(call(Plus, One, m), var_6784040757061224, m);

	roots[92] = var_6784040757061227;
	roots[92] = garbage_collect(roots[92]);
	var_6784040757061227 = roots[92];
	roots[93] = NULL;
	var_6784040757061226 = call(call(Plus, One, m), var_6784040757061227, m);

	roots[93] = var_6784040757061226;
	roots[93] = garbage_collect(roots[93]);
	var_6784040757061226 = roots[93];
	roots[94] = NULL;
	var_6784040757061221 = call(call(Plus, One, m), var_6784040757061226, m);

	roots[94] = var_6784040757061221;
	roots[94] = garbage_collect(roots[94]);
	var_6784040757061221 = roots[94];
	roots[95] = NULL;
	var_6784040757061220 = call(call(Plus, One, m), var_6784040757061221, m);

	roots[95] = var_6784040757061220;
	roots[95] = garbage_collect(roots[95]);
	var_6784040757061220 = roots[95];
	roots[96] = NULL;
	var_6912041526062352 = call(call(Plus, One, m), var_6784040757061220, m);

	roots[96] = var_6912041526062352;
	roots[96] = garbage_collect(roots[96]);
	var_6912041526062352 = roots[96];
	roots[97] = NULL;
	var_6912041526062353 = call(call(Plus, One, m), var_6912041526062352, m);

	roots[97] = var_6912041526062353;
	roots[97] = garbage_collect(roots[97]);
	var_6912041526062353 = roots[97];
	roots[98] = NULL;
	var_6912041526062354 = call(call(Plus, One, m), var_6912041526062353, m);

	roots[98] = var_6912041526062354;
	roots[98] = garbage_collect(roots[98]);
	var_6912041526062354 = roots[98];
	roots[99] = NULL;
	var_6912041526062355 = call(call(Plus, One, m), var_6912041526062354, m);

	roots[99] = var_6912041526062355;
	roots[99] = garbage_collect(roots[99]);
	var_6912041526062355 = roots[99];
	roots[100] = NULL;
	var_6912041526062356 = call(call(Plus, One, m), var_6912041526062355, m);

	roots[100] = var_6912041526062356;
	roots[100] = garbage_collect(roots[100]);
	var_6912041526062356 = roots[100];
	roots[101] = NULL;
	var_6912041526062357 = call(call(Plus, One, m), var_6912041526062356, m);

	roots[101] = var_6912041526062357;
	roots[101] = garbage_collect(roots[101]);
	var_6912041526062357 = roots[101];
	roots[102] = NULL;
	var_6912041526062358 = call(call(Plus, One, m), var_6912041526062357, m);

	roots[102] = var_6912041526062358;
	roots[102] = garbage_collect(roots[102]);
	var_6912041526062358 = roots[102];
	roots[103] = NULL;
	var_6912041526062359 = call(call(Plus, One, m), var_6912041526062358, m);

	roots[103] = var_6912041526062359;
	roots[103] = garbage_collect(roots[103]);
	var_6912041526062359 = roots[103];
	roots[104] = NULL;
	var_6912041526062360 = call(call(Plus, One, m), var_6912041526062359, m);

	roots[104] = var_6912041526062360;
	roots[104] = garbage_collect(roots[104]);
	var_6912041526062360 = roots[104];
	roots[105] = NULL;
	var_6912041526062361 = call(call(Plus, One, m), var_6912041526062360, m);

	roots[105] = var_6912041526062361;
	roots[105] = garbage_collect(roots[105]);
	var_6912041526062361 = roots[105];
	roots[106] = NULL;
	var_7040042295063511 = call(call(Plus, One, m), var_6912041526062361, m);

	roots[106] = var_7040042295063511;
	roots[106] = garbage_collect(roots[106]);
	var_7040042295063511 = roots[106];
	roots[107] = NULL;
	var_7040042295063510 = call(call(Plus, One, m), var_7040042295063511, m);

	roots[107] = var_7040042295063510;
	roots[107] = garbage_collect(roots[107]);
	var_7040042295063510 = roots[107];
	roots[108] = NULL;
	var_7040042295063509 = call(call(Plus, One, m), var_7040042295063510, m);

	roots[108] = var_7040042295063509;
	roots[108] = garbage_collect(roots[108]);
	var_7040042295063509 = roots[108];
	roots[109] = NULL;
	var_7040042295063508 = call(call(Plus, One, m), var_7040042295063509, m);

	roots[109] = var_7040042295063508;
	roots[109] = garbage_collect(roots[109]);
	var_7040042295063508 = roots[109];
	roots[110] = NULL;
	var_7040042295063507 = call(call(Plus, One, m), var_7040042295063508, m);

	roots[110] = var_7040042295063507;
	roots[110] = garbage_collect(roots[110]);
	var_7040042295063507 = roots[110];
	roots[111] = NULL;
	var_7040042295063506 = call(call(Plus, One, m), var_7040042295063507, m);

	roots[111] = var_7040042295063506;
	roots[111] = garbage_collect(roots[111]);
	var_7040042295063506 = roots[111];
	roots[112] = NULL;
	var_7040042295063505 = call(call(Plus, One, m), var_7040042295063506, m);

	roots[112] = var_7040042295063505;
	roots[112] = garbage_collect(roots[112]);
	var_7040042295063505 = roots[112];
	roots[113] = NULL;
	var_7040042295063504 = call(call(Plus, One, m), var_7040042295063505, m);

	roots[113] = var_7040042295063504;
	roots[113] = garbage_collect(roots[113]);
	var_7040042295063504 = roots[113];
	roots[114] = NULL;
	var_7040042295063519 = call(call(Plus, One, m), var_7040042295063504, m);

	roots[114] = var_7040042295063519;
	roots[114] = garbage_collect(roots[114]);
	var_7040042295063519 = roots[114];
	roots[115] = NULL;
	var_7040042295063518 = call(call(Plus, One, m), var_7040042295063519, m);

	roots[115] = var_7040042295063518;
	roots[115] = garbage_collect(roots[115]);
	var_7040042295063518 = roots[115];
	roots[116] = NULL;
	var_7168043064064666 = call(call(Plus, One, m), var_7040042295063518, m);

	roots[116] = var_7168043064064666;
	roots[116] = garbage_collect(roots[116]);
	var_7168043064064666 = roots[116];
	roots[117] = NULL;
	var_7168043064064667 = call(call(Plus, One, m), var_7168043064064666, m);

	roots[117] = var_7168043064064667;
	roots[117] = garbage_collect(roots[117]);
	var_7168043064064667 = roots[117];
	roots[118] = NULL;
	var_7168043064064664 = call(call(Plus, One, m), var_7168043064064667, m);

	roots[118] = var_7168043064064664;
	roots[118] = garbage_collect(roots[118]);
	var_7168043064064664 = roots[118];
	roots[119] = NULL;
	var_7168043064064665 = call(call(Plus, One, m), var_7168043064064664, m);

	roots[119] = var_7168043064064665;
	roots[119] = garbage_collect(roots[119]);
	var_7168043064064665 = roots[119];
	roots[120] = NULL;
	var_7168043064064670 = call(call(Plus, One, m), var_7168043064064665, m);

	roots[120] = var_7168043064064670;
	roots[120] = garbage_collect(roots[120]);
	var_7168043064064670 = roots[120];
	roots[121] = NULL;
	var_7168043064064671 = call(call(Plus, One, m), var_7168043064064670, m);

	roots[121] = var_7168043064064671;
	roots[121] = garbage_collect(roots[121]);
	var_7168043064064671 = roots[121];
	roots[122] = NULL;
	var_7168043064064668 = call(call(Plus, One, m), var_7168043064064671, m);

	roots[122] = var_7168043064064668;
	roots[122] = garbage_collect(roots[122]);
	var_7168043064064668 = roots[122];
	roots[123] = NULL;
	var_7168043064064669 = call(call(Plus, One, m), var_7168043064064668, m);

	roots[123] = var_7168043064064669;
	roots[123] = garbage_collect(roots[123]);
	var_7168043064064669 = roots[123];
	roots[124] = NULL;
	var_7168043064064658 = call(call(Plus, One, m), var_7168043064064669, m);

	roots[124] = var_7168043064064658;
	roots[124] = garbage_collect(roots[124]);
	var_7168043064064658 = roots[124];
	roots[125] = NULL;
	var_7168043064064659 = call(call(Plus, One, m), var_7168043064064658, m);

	roots[125] = var_7168043064064659;
	roots[125] = garbage_collect(roots[125]);
	var_7168043064064659 = roots[125];
	roots[126] = NULL;
	var_7296043833065817 = call(call(Plus, One, m), var_7168043064064659, m);

	roots[126] = var_7296043833065817;
	roots[126] = garbage_collect(roots[126]);
	var_7296043833065817 = roots[126];
	roots[127] = NULL;
	var_7296043833065816 = call(call(Plus, One, m), var_7296043833065817, m);

	roots[127] = var_7296043833065816;
	roots[127] = garbage_collect(roots[127]);
	var_7296043833065816 = roots[127];
	roots[128] = NULL;
	var_7296043833065819 = call(call(Plus, One, m), var_7296043833065816, m);

	roots[128] = var_7296043833065819;
	roots[128] = garbage_collect(roots[128]);
	var_7296043833065819 = roots[128];
	roots[129] = NULL;
	var_7296043833065818 = call(call(Plus, One, m), var_7296043833065819, m);

	roots[129] = var_7296043833065818;
	roots[129] = garbage_collect(roots[129]);
	var_7296043833065818 = roots[129];
	roots[130] = NULL;
	var_7296043833065821 = call(call(Plus, One, m), var_7296043833065818, m);

	roots[130] = var_7296043833065821;
	roots[130] = garbage_collect(roots[130]);
	var_7296043833065821 = roots[130];
	roots[131] = NULL;
	var_7296043833065820 = call(call(Plus, One, m), var_7296043833065821, m);

	roots[131] = var_7296043833065820;
	roots[131] = garbage_collect(roots[131]);
	var_7296043833065820 = roots[131];
	roots[132] = NULL;
	var_7296043833065823 = call(call(Plus, One, m), var_7296043833065820, m);

	roots[132] = var_7296043833065823;
	roots[132] = garbage_collect(roots[132]);
	var_7296043833065823 = roots[132];
	roots[133] = NULL;
	var_7296043833065822 = call(call(Plus, One, m), var_7296043833065823, m);

	roots[133] = var_7296043833065822;
	roots[133] = garbage_collect(roots[133]);
	var_7296043833065822 = roots[133];
	roots[134] = NULL;
	var_7296043833065809 = call(call(Plus, One, m), var_7296043833065822, m);

	roots[134] = var_7296043833065809;
	roots[134] = garbage_collect(roots[134]);
	var_7296043833065809 = roots[134];
	roots[135] = NULL;
	var_7296043833065808 = call(call(Plus, One, m), var_7296043833065809, m);

	roots[135] = var_7296043833065808;
	roots[135] = garbage_collect(roots[135]);
	var_7296043833065808 = roots[135];
	roots[136] = NULL;
	var_163512108406620378 = call(call(Plus, One, m), var_7296043833065808, m);

	roots[136] = var_163512108406620378;
	roots[136] = garbage_collect(roots[136]);
	var_163512108406620378 = roots[136];
	roots[137] = NULL;
	var_163512108406620379 = call(call(Plus, One, m), var_163512108406620378, m);

	roots[137] = var_163512108406620379;
	roots[137] = garbage_collect(roots[137]);
	var_163512108406620379 = roots[137];
	roots[138] = NULL;
	var_163512108406620376 = call(call(Plus, One, m), var_163512108406620379, m);

	roots[138] = var_163512108406620376;
	roots[138] = garbage_collect(roots[138]);
	var_163512108406620376 = roots[138];
	roots[139] = NULL;
	var_163512108406620377 = call(call(Plus, One, m), var_163512108406620376, m);

	roots[139] = var_163512108406620377;
	roots[139] = garbage_collect(roots[139]);
	var_163512108406620377 = roots[139];
	roots[140] = NULL;
	var_163512108406620382 = call(call(Plus, One, m), var_163512108406620377, m);

	roots[140] = var_163512108406620382;
	roots[140] = garbage_collect(roots[140]);
	var_163512108406620382 = roots[140];
	roots[141] = NULL;
	var_163512108406620383 = call(call(Plus, One, m), var_163512108406620382, m);

	roots[141] = var_163512108406620383;
	roots[141] = garbage_collect(roots[141]);
	var_163512108406620383 = roots[141];
	roots[142] = NULL;
	var_163512108406620380 = call(call(Plus, One, m), var_163512108406620383, m);

	roots[142] = var_163512108406620380;
	roots[142] = garbage_collect(roots[142]);
	var_163512108406620380 = roots[142];
	roots[143] = NULL;
	var_163512108406620381 = call(call(Plus, One, m), var_163512108406620380, m);

	roots[143] = var_163512108406620381;
	roots[143] = garbage_collect(roots[143]);
	var_163512108406620381 = roots[143];
	roots[144] = NULL;
	var_163512108406620370 = call(call(Plus, One, m), var_163512108406620381, m);

	roots[144] = var_163512108406620370;
	roots[144] = garbage_collect(roots[144]);
	var_163512108406620370 = roots[144];
	roots[145] = NULL;
	var_163512108406620371 = call(call(Plus, One, m), var_163512108406620370, m);

	roots[145] = var_163512108406620371;
	roots[145] = garbage_collect(roots[145]);
	var_163512108406620371 = roots[145];
	roots[146] = NULL;
	var_163512108405620373 = call(call(Plus, One, m), var_163512108406620371, m);

	roots[146] = var_163512108405620373;
	roots[146] = garbage_collect(roots[146]);
	var_163512108405620373 = roots[146];
	roots[147] = NULL;
	var_163512108405620372 = call(call(Plus, One, m), var_163512108405620373, m);

	roots[147] = var_163512108405620372;
	roots[147] = garbage_collect(roots[147]);
	var_163512108405620372 = roots[147];
	roots[148] = NULL;
	var_163512108405620375 = call(call(Plus, One, m), var_163512108405620372, m);

	roots[148] = var_163512108405620375;
	roots[148] = garbage_collect(roots[148]);
	var_163512108405620375 = roots[148];
	roots[149] = NULL;
	var_163512108405620374 = call(call(Plus, One, m), var_163512108405620375, m);

	roots[149] = var_163512108405620374;
	roots[149] = garbage_collect(roots[149]);
	var_163512108405620374 = roots[149];
	roots[150] = NULL;
	var_163512108405620369 = call(call(Plus, One, m), var_163512108405620374, m);

	roots[150] = var_163512108405620369;
	roots[150] = garbage_collect(roots[150]);
	var_163512108405620369 = roots[150];
	roots[151] = NULL;
	var_163512108405620368 = call(call(Plus, One, m), var_163512108405620369, m);

	roots[151] = var_163512108405620368;
	roots[151] = garbage_collect(roots[151]);
	var_163512108405620368 = roots[151];
	roots[152] = NULL;
	var_163512108405620371 = call(call(Plus, One, m), var_163512108405620368, m);

	roots[152] = var_163512108405620371;
	roots[152] = garbage_collect(roots[152]);
	var_163512108405620371 = roots[152];
	roots[153] = NULL;
	var_163512108405620370 = call(call(Plus, One, m), var_163512108405620371, m);

	roots[153] = var_163512108405620370;
	roots[153] = garbage_collect(roots[153]);
	var_163512108405620370 = roots[153];
	roots[154] = NULL;
	var_163512108405620381 = call(call(Plus, One, m), var_163512108405620370, m);

	roots[154] = var_163512108405620381;
	roots[154] = garbage_collect(roots[154]);
	var_163512108405620381 = roots[154];
	roots[155] = NULL;
	var_163512108405620380 = call(call(Plus, One, m), var_163512108405620381, m);

	roots[155] = var_163512108405620380;
	roots[155] = garbage_collect(roots[155]);
	var_163512108405620380 = roots[155];
	roots[156] = NULL;
	var_163512108404620368 = call(call(Plus, One, m), var_163512108405620380, m);

	roots[156] = var_163512108404620368;
	roots[156] = garbage_collect(roots[156]);
	var_163512108404620368 = roots[156];
	roots[157] = NULL;
	var_163512108404620369 = call(call(Plus, One, m), var_163512108404620368, m);

	roots[157] = var_163512108404620369;
	roots[157] = garbage_collect(roots[157]);
	var_163512108404620369 = roots[157];
	roots[158] = NULL;
	var_163512108404620370 = call(call(Plus, One, m), var_163512108404620369, m);

	roots[158] = var_163512108404620370;
	roots[158] = garbage_collect(roots[158]);
	var_163512108404620370 = roots[158];
	roots[159] = NULL;
	var_163512108404620371 = call(call(Plus, One, m), var_163512108404620370, m);

	roots[159] = var_163512108404620371;
	roots[159] = garbage_collect(roots[159]);
	var_163512108404620371 = roots[159];
	roots[160] = NULL;
	var_163512108404620372 = call(call(Plus, One, m), var_163512108404620371, m);

	roots[160] = var_163512108404620372;
	roots[160] = garbage_collect(roots[160]);
	var_163512108404620372 = roots[160];
	roots[161] = NULL;
	var_163512108404620373 = call(call(Plus, One, m), var_163512108404620372, m);

	roots[161] = var_163512108404620373;
	roots[161] = garbage_collect(roots[161]);
	var_163512108404620373 = roots[161];
	roots[162] = NULL;
	var_163512108404620374 = call(call(Plus, One, m), var_163512108404620373, m);

	roots[162] = var_163512108404620374;
	roots[162] = garbage_collect(roots[162]);
	var_163512108404620374 = roots[162];
	roots[163] = NULL;
	var_163512108404620375 = call(call(Plus, One, m), var_163512108404620374, m);

	roots[163] = var_163512108404620375;
	roots[163] = garbage_collect(roots[163]);
	var_163512108404620375 = roots[163];
	roots[164] = NULL;
	ascii_table[42] = var_6656039988060076;
	ascii_table[24] = var_6400038450057760;
	ascii_table[26] = var_6400038450057762;
	ascii_table[27] = var_6400038450057763;
	ascii_table[20] = var_6400038450057764;
	ascii_table[21] = var_6400038450057765;
	ascii_table[22] = var_6400038450057766;
	ascii_table[23] = var_6400038450057767;
	ascii_table[95] = var_7296043833065820;
	ascii_table[28] = var_6400038450057772;
	ascii_table[29] = var_6400038450057773;
	ascii_table[0] = Zero;
	ascii_table[4] = var_6656020021;
	ascii_table[8] = var_7168021561;
	ascii_table[119] = var_163512108405620380;
	ascii_table[120] = var_163512108404620368;
	ascii_table[121] = var_163512108404620369;
	ascii_table[122] = var_163512108404620370;
	ascii_table[123] = var_163512108404620371;
	ascii_table[124] = var_163512108404620372;
	ascii_table[125] = var_163512108404620373;
	ascii_table[126] = var_163512108404620374;
	ascii_table[127] = var_163512108404620375;
	ascii_table[118] = var_163512108405620381;
	ascii_table[59] = var_6784040757061220;
	ascii_table[58] = var_6784040757061221;
	ascii_table[55] = var_6784040757061224;
	ascii_table[54] = var_6784040757061225;
	ascii_table[57] = var_6784040757061226;
	ascii_table[56] = var_6784040757061227;
	ascii_table[51] = var_6784040757061228;
	ascii_table[50] = var_6784040757061229;
	ascii_table[53] = var_6784040757061230;
	ascii_table[52] = var_6784040757061231;
	ascii_table[115] = var_163512108405620368;
	ascii_table[114] = var_163512108405620369;
	ascii_table[89] = var_7168043064064659;
	ascii_table[111] = var_163512108405620372;
	ascii_table[110] = var_163512108405620373;
	ascii_table[113] = var_163512108405620374;
	ascii_table[112] = var_163512108405620375;
	ascii_table[82] = var_7168043064064664;
	ascii_table[83] = var_7168043064064665;
	ascii_table[80] = var_7168043064064666;
	ascii_table[81] = var_7168043064064667;
	ascii_table[86] = var_7168043064064668;
	ascii_table[87] = var_7168043064064669;
	ascii_table[85] = var_7168043064064671;
	ascii_table[117] = var_163512108405620370;
	ascii_table[3] = var_6528019634;
	ascii_table[7] = var_7040021174;
	ascii_table[25] = var_6400038450057761;
	ascii_table[108] = var_163512108406620370;
	ascii_table[109] = var_163512108406620371;
	ascii_table[102] = var_163512108406620376;
	ascii_table[103] = var_163512108406620377;
	ascii_table[100] = var_163512108406620378;
	ascii_table[101] = var_163512108406620379;
	ascii_table[106] = var_163512108406620380;
	ascii_table[107] = var_163512108406620381;
	ascii_table[104] = var_163512108406620382;
	ascii_table[105] = var_163512108406620383;
	ascii_table[39] = var_6528039219058914;
	ascii_table[38] = var_6528039219058915;
	ascii_table[33] = var_6528039219058920;
	ascii_table[32] = var_6528039219058921;
	ascii_table[31] = var_6528039219058922;
	ascii_table[30] = var_6528039219058923;
	ascii_table[37] = var_6528039219058924;
	ascii_table[36] = var_6528039219058925;
	ascii_table[35] = var_6528039219058926;
	ascii_table[34] = var_6528039219058927;
	ascii_table[60] = var_6912041526062352;
	ascii_table[61] = var_6912041526062353;
	ascii_table[62] = var_6912041526062354;
	ascii_table[63] = var_6912041526062355;
	ascii_table[64] = var_6912041526062356;
	ascii_table[65] = var_6912041526062357;
	ascii_table[66] = var_6912041526062358;
	ascii_table[67] = var_6912041526062359;
	ascii_table[68] = var_6912041526062360;
	ascii_table[69] = var_6912041526062361;
	ascii_table[2] = var_6400019251;
	ascii_table[79] = var_7040042295063518;
	ascii_table[6] = var_6912020791;
	ascii_table[99] = var_7296043833065808;
	ascii_table[98] = var_7296043833065809;
	ascii_table[91] = var_7296043833065816;
	ascii_table[90] = var_7296043833065817;
	ascii_table[93] = var_7296043833065818;
	ascii_table[92] = var_7296043833065819;
	ascii_table[94] = var_7296043833065821;
	ascii_table[97] = var_7296043833065822;
	ascii_table[96] = var_7296043833065823;
	ascii_table[11] = var_6272037681056608;
	ascii_table[10] = var_6272037681056609;
	ascii_table[13] = var_6272037681056610;
	ascii_table[12] = var_6272037681056611;
	ascii_table[15] = var_6272037681056612;
	ascii_table[14] = var_6272037681056613;
	ascii_table[17] = var_6272037681056614;
	ascii_table[16] = var_6272037681056615;
	ascii_table[19] = var_6272037681056616;
	ascii_table[18] = var_6272037681056617;
	ascii_table[88] = var_7168043064064658;
	ascii_table[116] = var_163512108405620371;
	ascii_table[48] = var_6656039988060070;
	ascii_table[49] = var_6656039988060071;
	ascii_table[46] = var_6656039988060072;
	ascii_table[47] = var_6656039988060073;
	ascii_table[44] = var_6656039988060074;
	ascii_table[45] = var_6656039988060075;
	ascii_table[43] = var_6656039988060077;
	ascii_table[40] = var_6656039988060078;
	ascii_table[41] = var_6656039988060079;
	ascii_table[1] = One;
	ascii_table[5] = var_6784020404;
	ascii_table[84] = var_7168043064064670;
	ascii_table[9] = var_7296021944;
	ascii_table[77] = var_7040042295063504;
	ascii_table[76] = var_7040042295063505;
	ascii_table[75] = var_7040042295063506;
	ascii_table[74] = var_7040042295063507;
	ascii_table[73] = var_7040042295063508;
	ascii_table[72] = var_7040042295063509;
	ascii_table[71] = var_7040042295063510;
	ascii_table[70] = var_7040042295063511;
	ascii_table[78] = var_7040042295063519;
	Closure49 = create_function(closure49, empty_env, 0, m);

	roots[164] = Closure49;
	roots[164] = garbage_collect(roots[164]);
	Closure49 = roots[164];
	roots[165] = NULL;
	Closure52 = create_function(closure52, empty_env, 0, m);

	roots[165] = Closure52;
	roots[165] = garbage_collect(roots[165]);
	Closure52 = roots[165];
	roots[166] = NULL;
	Closure53 = create_function(closure53, empty_env, 0, m);

	roots[166] = Closure53;
	roots[166] = garbage_collect(roots[166]);
	Closure53 = roots[166];
	roots[167] = NULL;
	Closure54 = create_function(closure54, empty_env, 0, m);

	roots[167] = Closure54;
	roots[167] = garbage_collect(roots[167]);
	Closure54 = roots[167];
	roots[168] = NULL;
	Closure62 = create_function(closure62, empty_env, 0, m);

	roots[168] = Closure62;
	roots[168] = garbage_collect(roots[168]);
	Closure62 = roots[168];
	roots[169] = NULL;
	var_4991407356201764482 = call(call(Times, var_6272037681056609, m), var_163512108406620378, m);

	roots[169] = var_4991407356201764482;
	roots[169] = garbage_collect(roots[169]);
	var_4991407356201764482 = roots[169];
	roots[170] = NULL;
	Closure63 = create_function(closure63, empty_env, 0, m);

	roots[170] = Closure63;
	roots[170] = garbage_collect(roots[170]);
	Closure63 = roots[170];
	roots[171] = NULL;
	Closure72 = create_function(closure72, empty_env, 0, m);

	roots[171] = Closure72;
	roots[171] = garbage_collect(roots[171]);
	Closure72 = roots[171];
	roots[172] = NULL;
	Closure75 = create_function(closure75, empty_env, 0, m);

	roots[172] = Closure75;
	roots[172] = garbage_collect(roots[172]);
	Closure75 = roots[172];
	roots[173] = NULL;
	var_7876451200857581859 = call(call(call(Closure63, Zero, m), One, m), Null_ptr, m);

	roots[173] = var_7876451200857581859;
	roots[173] = garbage_collect(roots[173]);
	var_7876451200857581859 = roots[173];
	roots[174] = NULL;
	var_2083207811319332352 = call(Closure72, var_7876451200857581859, m);

	var_2083207811319332352 = call(Print_num, call(Length, var_7876451200857581859, m), m);

	var_2083207811319332352 = call(Print_char, var_6272037681056609, m);

	var_2083207811319332352 = call(Print_num, call(call(List_ref, var_7876451200857581859, m), Zero, m), m);

	var_2083207811319332352 = call(Print_char, var_6272037681056609, m);

	var_2083207811319332352 = call(call(Write, Stdout, m), call(call(Closure8, var_7168043064064665, m), call(call(Closure8, var_163512108405620370, m), call(call(Closure8, var_163512108406620371, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_163512108405620372, m), call(call(Closure8, var_163512108406620376, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_163512108406620376, m), call(call(Closure8, var_163512108406620383, m), call(call(Closure8, var_163512108405620369, m), call(call(Closure8, var_163512108405620368, m), call(call(Closure8, var_163512108405620371, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_6656039988060071, m), call(call(Closure8, var_6656039988060070, m), call(call(Closure8, var_6656039988060070, m), call(call(Closure8, var_6656039988060070, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_163512108405620375, m), call(call(Closure8, var_163512108405620369, m), call(call(Closure8, var_163512108406620383, m), call(call(Closure8, var_163512108406620371, m), call(call(Closure8, var_163512108406620379, m), call(call(Closure8, var_163512108405620368, m), call(call(Closure8, var_6272037681056609, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_7296043833065809, m), call(call(Closure8, var_163512108406620379, m), call(call(Closure8, var_163512108406620370, m), call(call(Closure8, var_163512108405620372, m), call(call(Closure8, var_163512108405620380, m), call(call(Closure8, var_6656039988060074, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_7040042295063508, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_7296043833065822, m), call(call(Closure8, var_163512108406620371, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_7296043833065822, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_163512108406620371, m), call(call(Closure8, var_163512108405620370, m), call(call(Closure8, var_163512108406620370, m), call(call(Closure8, var_163512108405620371, m), call(call(Closure8, var_163512108406620383, m), call(call(Closure8, var_6656039988060075, m), call(call(Closure8, var_163512108406620370, m), call(call(Closure8, var_163512108406620383, m), call(call(Closure8, var_163512108405620373, m), call(call(Closure8, var_163512108406620379, m), call(call(Closure8, var_6528039219058921, m), call(call(Closure8, var_163512108405620368, m), call(call(Closure8, var_163512108405620371, m), call(call(Closure8, var_163512108405620369, m), call(call(Closure8, var_163512108406620383, m), call(call(Closure8, var_163512108405620373, m), call(call(Closure8, var_163512108406620377, m), call(call(Closure8, var_6272037681056609, m), Null_ptr, m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m), m);

	var_2083207811319332352 = call(Print_num, call(call(call(Reduce, Plus, m), Zero, m), var_7876451200857581859, m), m);

	var_2083207811319332352 = call(Print_char, var_6272037681056609, m);

	clean_up(m);
	free(empty_env);
	free(roots);
	free(ascii_table);
	free(int_env);
}
