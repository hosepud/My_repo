import java.util.*;

public class Evaluator{
	public static int prim_ctr = 0;
	public static void main(String[] args){
		Environment env = new Environment();
		eval_func("(define identity (@ x x))", env);
		eval_func("(define true (@ a (@ b a)))", env);
		eval_func("(define false (@ a (@ b b)))", env);
		eval_func("(define cons (@ x (@ y (@ z ((z x) y)))))", env);
		eval_func("(define first (@ p (p (@ x (@ y x)))))", env);
		eval_func("(define second (@ p (p (@ x (@ y y)))))", env);
		define_primitive("+", env);
		define_primitive("-", env);
		define_primitive("if", env);
		define_primitive("<=", env);
		define_primitive("*", env);
		define_primitive("/", env);
		define_primitive("%", env);
		define_primitive("<", env);
		define_primitive(">", env);
		define_primitive("=", env);
		define_primitive(">=", env);
		define_primitive("not", env);
		define_primitive("and", env);
		define_primitive("or", env);
		define_primitive("pair", env);
		define_primitive("print-num", env);
		define_primitive("print-char", env);
		define_primitive("newline", env);
		define_primitive("nil", env);
		define_primitive("isnil", env);
		define_primitive("expt", env);
		define_primitive("map", env);
		define_primitive("filter", env);
		define_primitive("reduce", env);
		define_primitive("case", env);
		eval_func("(define pred (@ x (- x 1)))", env);
		eval_func("(define Y (@ X ((@ procedure (X (@ arg ((procedure procedure) arg)))) (@ procedure (X (@ arg ((procedure procedure) arg)))))))", env);
		eval_func("(define print (@ lst (if (isnil lst) (print-char 10) (and (print-char (first lst)) (print (second lst))))))", env);
		eval_func("(define map-prim (@ func (@ lst (if (isnil lst) nil (pair (func (first lst)) ((map-prim func) (second lst)))))))", env);
		eval_func("(define filter-prim (@ func (@ lst (if (isnil lst) nil (if (func (first lst)) (pair (first lst) ((filter-prim func) (second lst))) ((filter-prim func) (second lst)))))))", env);
		eval_func("(define print-lst (@ lst (if (isnil lst) (print-char 10) (and (print-num (first lst)) (print-char 32) (print-lst (second lst))))))", env);
		eval_func("(define accumulate-prim (@ op (@ initial (@ sequence (if (isnil sequence) initial (op (first sequence) (((accumulate-prim op) initial) (second sequence))))))))", env);	
		
		eval_func("(define fizzbuzz (@ x (case (= x 101) x (= (% x 15) 0) (and (print \"\"\"FizzB\"uzz\n\"\"\") (fizzbuzz (+ x 1))) (= (% x 3) 0) (and (print \"\"\"F\"iz\"z\n\"\"\") (fizzbuzz (+ x 1))) (= (% x 5) 0) (and (print \"\"\"Bu\"z'\"z\n\"\"\") (fizzbuzz (+ x 1))) else (and (print-num x) (newline) (fizzbuzz (+ x 1))))))", env);
		eval_func("(define fibs (Y (@ func (@ x (if (<= x 2) x (+ (func (- x 1)) (func (- x 2))))))))", env);
		eval_func("(define fact (Y (@ func (@ x (if (< x 1) 1 (* x (fact (- x 1))))))))", env);
		REPL(env);
		return;
	}

	public static void print_frame(HashMap<String, Token> locals){
			Object[] keys =  locals.keySet().toArray();	
			System.out.println("Locals: ");			
			for(int j = 0;j<keys.length;j++){
				System.out.printf("%s ", keys[j]);
				locals.get(keys[j]).print();
				System.out.printf("\n");
			}
			return;
	}		
	private static void REPL(Environment env){
		Scanner inp = new Scanner(System.in);
		String exp;
		int ctr = 0;
		while(true){
			try{
				System.out.printf("\n+=> ");
				exp = inp.nextLine();
				eval_func(exp, env);
				ctr++;
			}catch(Exception e){
				System.out.println("Input error");
			}
			
		}
	}

	private static void define_primitive(String str, Environment env){
		env.frames.get(0).put(str, new Token(prim_ctr));
		env.frames.get(0).get(str).name = str;	
		prim_ctr ++;
		return;
	}
	private static boolean is_definition(String exp){
		String[] parsed = Parser.parse(exp);
		return parsed[0].equals("define");
	}

	private static void eval_func(String exp, Environment env){
		exp = Parser.preprocess(exp).toString();
		String[] parsed = Parser.parse(exp);
		if(Parser.is_variable(exp)){
			System.out.println(exp);
			Parser.tokenize(exp).eval(env).print();
		}else if(is_definition(exp)){
			env.frames.get(0).put(parsed[1], Parser.tokenize(parsed[2]).eval(env));
			env.frames.get(0).get(parsed[1]).name = parsed[1];
		}else{	
			Parser.tokenize(exp).eval(env).print();
		}
		return;
	}
}
	
class Pair{
		public int j;
		public StringBuilder str;
		public Pair(StringBuilder strr, int jj){
			j = jj;
			str = strr;
			return;
		}
}

class Parser {
	public static final int CODELEN = 20;
	public static boolean is_variable(String exp){
		return exp.trim().charAt(0) != '(';
	}

	public static boolean is_variable(String[] exp){
		return false;
	}

	private static boolean is_lambda(String[] exp){
		return exp[0].equals("@");
	}
	public static Token tokenize(String exp){
		if(is_variable(exp))
			return new Token(exp);
		String[] parsed = parse(exp);
		if(is_lambda(parsed))
			return new Token(parsed[1], tokenize(parsed[2]));
		else{
			Token[] args = new Token[Parser.CODELEN];
			int i;
			for(i=0;parsed[i] != null;i++)
				args[i] = tokenize(parsed[i]);
			args[i] = null;
			return new Token(args);
		}
	}
	public static String[] parse(String exp){
		exp = exp.trim();
		int ctr = 1;
		int exp_ctr = 0;
		boolean in_exp = false;
		String[] ret = new String[Parser.CODELEN];
		String current = "";
		for(int i=1;i<exp.length();i++){
			switch(exp.charAt(i)){
				case '(':
					ctr ++;
					current += "(";
					break;
				case ')':
					ctr --;
					if(ctr == 0){
						ret[exp_ctr] = current.trim();
						exp_ctr++;
						break;
					}
					current += ")";
					break;
				case ' ':
					if(!in_exp)
						break;
					if(in_exp && ctr == 1){
						ret[exp_ctr] = current.trim();
						exp_ctr++;
						current = "";
					}
					in_exp = false;
					current += ' ';
					break;					
				default:
					in_exp = true;
					current += exp.charAt(i);	
			}
		}	
		for(int i=exp_ctr;i<10;i++){
			ret[i] = null;
		}							
		return ret;
	}
	public static boolean is_delimiter(char a, char b, char c){
		char[] tmp = new char[3];
		tmp[0] = a;
		tmp[1] = b;
		tmp[2] = c;
		String str = new String(tmp);
		return str.equals("\"\"\"");
	}
	
	public static Character resolve_escaped(Character c){
		HashMap<Character, Character> seqs = new HashMap<Character, Character>();
		seqs.put('n', '\n');
		seqs.put('\\', '\\');
		seqs.put('r', '\r');
		seqs.put('b', '\b');
		seqs.put('t', '\t');
		seqs.put('e', '\f');
		return seqs.get(c);
	}


	public static Pair get_string(String exp, int i){
		StringBuilder str = new StringBuilder();
		boolean escaped = false;
		int j;
		char[] tmp = new char[1];
		for(j = i;j<exp.length();j++){
			if(is_delimiter(exp.charAt(j),exp.charAt(j+1), exp.charAt(j+2))){
				return new Pair(str, j+2);
			}if(exp.charAt(j) == '\\' &&  !escaped){
				escaped = true;
			}else{
				if(escaped){
					tmp[0] = resolve_escaped(exp.charAt(j));
					str.append(tmp);
					escaped = false;
				}else{
					tmp[0] = exp.charAt(j);
					str.append(tmp);
				}
			}
		}
		return new Pair(str, j);
	}
	
	public static String listify(StringBuilder exp){
		String str = "";
		int i;
		for(i=0;i<exp.length();i++){
			str += "(pair " + Integer.toString(((int)exp.charAt(i))) + " ";
		}
		str += " nil";
		for(i=0;i<exp.length();i++){
			str += ")";
		}
		return str;
	}
	public static StringBuilder preprocess(String exp){
		StringBuilder ret = new StringBuilder();
		boolean in_string = false;
		int i = 0;
		int j;
		String str;
		Pair p;
		while (i< exp.length()){
			if(i >= exp.length() || i+1>=exp.length() || i+2>=exp.length()){
				ret.append(exp.substring(i));
				return ret;
			}
			if(is_delimiter(exp.charAt(i),exp.charAt(i+1),exp.charAt(i+2))){
				p = get_string(exp, i+3);
				i = p.j;
				ret.append(listify(p.str));
			}else{
				ret.append(exp.charAt(i));
			}
			i+=1;
		}
		return ret;
	}
}

class Token{
	public int num;
	public String name;
	public String variable;
	public Token body;
	public Token[] code;
	public enum Type {NUMBER, VARIABLE, LAMBDA, CALL};
	public Environment my_env;
	Type type;
	
	public Token(int integer){
		this.type = Type.NUMBER;
		this.num = integer;
		return;
	}
	
	public Token(String name){
		this.type = Type.VARIABLE;
		this.name = name;
		return;
	}

	public Token(String variable, Token body){
		this.type = Type.LAMBDA;
		this.variable = variable;
		this.body = body;
		return;
	}

	public Token(Token[] code){
		this.type = Type.CALL;
		this.code = code;
		return;
	}
	
	public Token copy(Environment env){
		Token ret = new Token(this.num);
		ret.name = name;
		ret.variable = variable;
		ret.body = body;
		ret.code = code;
		ret.type = type;
		ret.my_env = env;
		return ret;
	}
	
	public boolean is_number(String s){
		try {
      			Integer.parseInt(s);
			return true;
		} catch (NumberFormatException e) {
      			return false;
		}
	}
	public Token eval(Environment env){
		switch(type){
			case NUMBER:
				return this;
			case VARIABLE:
				if(is_number(name))
					return new Token(Integer.parseInt(name));
				if(env.lookup_variable(name) != null)
					return env.lookup_variable(name);	
				System.out.printf("VAR %s NOT FOUND\n", name);
				return null;
			case LAMBDA:
				return this.copy(env);
			case CALL:
				Token tmp;
				Token f = code[0].eval(env);
				if(f.name != null){
					switch(f.name){
						case "+":
							return add(code, env);
						case "-":
							return subtract(code, env);
						case "if":
							return if_func(code, env);
						case "<=":
							return lte(code, env);
						case "*":
							return mul(code, env);
						case "/":
							return divide(code, env);
						case "%":
							return modulo(code, env);
						case "=":
							return eq(code, env);
						case "<":
							return lt(code, env);
						case ">":
							return gt(code, env);
						case ">=":
							return gte(code, env);					
						case "not":
							return not_func(code, env);
						case "and":
							return and_func(code, env);
						case "or":
							return or_func(code, env);
						case "pair":
							return pair_func(code, env).eval(env);
						case "print-num":
							tmp = code[1].eval(env);
							System.out.printf("%d", tmp.num);
							return tmp;
						case "print-char":
							tmp = code[1].eval(env);
							System.out.printf("%c",tmp.num);
							return tmp;
						case "newline":
							System.out.print("\n");
							return new Token(10);
						case "nil":
							return f;
						case "isnil":
							return isnil_func(code, env);
						case "expt":
							return expt(code, env);
						case "map":
							return map_func(code, env).eval(env);
						case "filter":
							return filter_func(code, env).eval(env);
						case "reduce":
							return reduce_func(code, env).eval(env);
						case "case":
							return case_func(code, env);
						default:
							break;
					}
				}
				Token arg = code[1].eval(env);
				env = f.my_env.extend_environment(f.variable, arg, f.my_env);
				Token ret = f.body.eval(env);
				return ret;	
			default:
				return null;
		}
	}	
	
	public void print_lst_as_str(Token lst, Environment env){
		Token[] call = new Token[Parser.CODELEN];
		Token t;
		while(lst != env.lookup_variable("nil")){
			call[0] = env.lookup_variable("first");
			call[1] = lst;
			call[2] = null;
			t = new Token(call);
			Parser.tokenize("(first zee)").print();
			t.print();
			t = t.eval(env);
			lst = t;
		}
		return;
	}
	
	public Token case_func(Token[] args, Environment env){
		int i = 1;
		while(args[i] != null){
			if(args[i].name != null && args[i].name.equals("else"))
				return args[i+1].eval(env);
			if(args[i].eval(env) == env.lookup_variable("true"))
				return args[i+1].eval(env);
			i += 2;
		}
		return null;
	}

	public Token expt(Token[] args, Environment env){
		int ret;
		Token base = args[1].eval(env);
		Token power = args[2].eval(env);
		ret = (int) Math.pow(base.num, power.num);
		return new Token(ret);
	}
	
	public Token reduce_func(Token[] args, Environment env){
		Token[] clos_args = new Token[Parser.CODELEN];
		clos_args[0] = env.lookup_variable("accumulate-prim");
		clos_args[1] = args[1];
		clos_args[2] = null;
		Token[] clos_args2 = new Token[Parser.CODELEN];
		clos_args2[0] = new Token(clos_args);
		clos_args2[1] = args[2];
		clos_args2[2] = null;
		Token[] ret = new Token[Parser.CODELEN];
		ret[0] = new Token(clos_args2);
		ret[1] = args[3];
		ret[2] = null;
		Token t = new Token(ret);
		return t;
	}				

	public Token map_func(Token[] args, Environment env){
		Token[] clos_args = new Token[Parser.CODELEN];
		clos_args[0] = env.lookup_variable("map-prim");
		clos_args[1] = args[1];
		clos_args[2] = null;
		Token[] ret = new Token[Parser.CODELEN];
		ret[0] = new Token(clos_args);
		ret[1] = args[2];
		ret[2] = null;
		Token t = new Token(ret);
		return t;
	}	

	public Token filter_func(Token[] args, Environment env){
		Token[] clos_args = new Token[Parser.CODELEN];
		clos_args[0] = env.lookup_variable("filter-prim");
		clos_args[1] = args[1];
		clos_args[2] = null;
		Token[] ret = new Token[Parser.CODELEN];
		ret[0] = new Token(clos_args);
		ret[1] = args[2];
		ret[2] = null;
		Token t = new Token(ret);
		return t;
	}	
		
	public Token pair_func(Token[] args, Environment env){
		Token[] clos_args = new Token[Parser.CODELEN];
		clos_args[0] = env.lookup_variable("cons");
		clos_args[1] = args[1];
		clos_args[2] = null;
		Token[] ret = new Token[Parser.CODELEN];
		ret[0] = new Token(clos_args);
		ret[1] = args[2];
		ret[2] = null;
		Token t = new Token(ret);
		return t;
	}

	public Token isnil_func(Token[] args, Environment env){
		if(args[1].eval(env) == env.lookup_variable("nil"))
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}

	public Token add(Token[] args, Environment env){
		int i = 1;
		int sum = 0;
		while(args[i] != null){
			sum += args[i].eval(env).num;
			i++;
		}		
		return new Token(sum);
	}	

	public Token not_func(Token[] args, Environment env){
		boolean ret = false;
		if(args[1].eval(env) == env.lookup_variable("false"))
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}

	public Token or_func(Token[] args, Environment env){
		boolean ret = false;
		int i = 1;
		while(args[i] != null){
			if(args[i].eval(env) == env.lookup_variable("true"))
				ret = true;
			i++;
		}
		if(ret)
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}	
	
	public Token and_func(Token[] args, Environment env){
		boolean ret = true;
		int i = 1;
		while(args[i] != null){
			if(args[i].eval(env) == env.lookup_variable("false"))
				ret = false;
			i++;
		}
		if(ret)
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}	
						
	public Token mul(Token[] args, Environment env){
		int i = 1;
		int prod = 1;
		while(args[i] != null){
			prod *= args[i].eval(env).num;
			i++;
		}
		return new Token(prod);
	}

	public Token divide(Token[] args, Environment env){
		int i = 2;
		int res = args[1].eval(env).num;
		while(args[i] != null){
			res /= args[i].eval(env).num;
			i++;
		}		
		return new Token(res);
	}

	public Token modulo(Token[] args, Environment env){
		int i = 2;
		int res = args[1].eval(env).num;
		while(args[i] != null){
			res %= args[i].eval(env).num;
			i++;
		}		
		return new Token(res);
	}	

	public Token subtract(Token[] args, Environment env){
		int i = 2;
		int sum = args[1].eval(env).num;
		while(args[i] != null){
			sum -= args[i].eval(env).num;
			i++;
		}		
		return new Token(sum);
	}

	public Token if_func(Token[] args, Environment env){
		if(args[1].eval(env) == env.lookup_variable("true"))
			return args[2].eval(env);
		return args[3].eval(env);
	}

	public Token lte(Token[] args, Environment env){
		if(args[1].eval(env).num <= args[2].eval(env).num)
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}

	public Token eq(Token[] args, Environment env){
		if(args[1].eval(env).num == args[2].eval(env).num)
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}

	public Token gte(Token[] args, Environment env){
		if(args[1].eval(env).num >= args[2].eval(env).num)
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}

	public Token lt(Token[] args, Environment env){
		if(args[1].eval(env).num < args[2].eval(env).num)
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}

	public Token gt(Token[] args, Environment env){
		if(args[1].eval(env).num > args[2].eval(env).num)
			return env.lookup_variable("true");
		return env.lookup_variable("false");
	}

	public void print(){
		switch(type){
			case NUMBER:
				System.out.printf("%d", num);
				return;
			case VARIABLE:
				System.out.printf("%s", name);
				return;
			case CALL:
				int i = 0;
				System.out.printf("(");
				while(code[i] != null){
					code[i].print();
					System.out.printf(" ");
					i++;
					}
				System.out.printf(")");
				return;
			case LAMBDA:
				if(name != null)
					System.out.printf("%s", name);
				else
					System.out.printf("anonymous ");
				System.out.printf(variable + " -> ");
				body.print();
				return;
			default:
				return;
		}
	}
}
	

class Environment {
	public ArrayList<HashMap<String,Token>> frames;

	public Environment() {
		frames = new ArrayList<>();
		frames.add(new HashMap<String,Token>());
	}

	public Environment extend_environment(String var, Token val, Environment env){		
		ArrayList<HashMap<String,Token>> new_frames = new  ArrayList<HashMap<String,Token>>();
		for(int i=0;i<frames.size();i++)
			new_frames.add(frames.get(i));				
		Environment new_env = new Environment();
		HashMap<String,Token> new_frame = new HashMap<String,Token>();
		new_frame.put(var, val);
		new_frames.add(new_frame);
		new_env.frames = new_frames;	
		return new_env;
	}

	public Token lookup_variable(String var){
		for(int i = frames.size()-1;i>-1;i--){
			if(frames.get(i).get(var) != null){
				return frames.get(i).get(var);
			}
		}
		return null;				
	}	

	public void print(){
		for(int i = 0; i<frames.size();i++){
			Object[] keys =  frames.get(i).keySet().toArray();	
			System.out.println("FRAME: ");			
			for(int j = 0;j<keys.length;j++){
				System.out.printf("%s ", keys[j]);
				frames.get(i).get(keys[j]).print();
				System.out.printf("\n");
			}
		}
		return;
	}
}



