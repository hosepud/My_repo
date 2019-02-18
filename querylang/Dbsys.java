
import java.util.*;
import java.io.FileReader;
import java.io.IOException;

public class Dbsys{
	public static int VAR_CTR;
	public static int DB_SIZE;
	public static HashMap<String,Token> RULES = new HashMap<String,Token>();

	public static void main(String[] args){		
		Token[] db = null;
		try{
			db = load_db_from_file(args[0]);
		}catch(IOException e){
			System.out.println("Filename not found");
		}	
		System.out.println("DB LOADED");
		qREPL(db);
		return;
	}
		
	public static void print_db(Token[] db){
		for(int i = 0; db[i] != null; i++){
			db[i].print();
			System.out.println();
		}
		return;
	}
	
	public static Token[] load_db_from_file(String filename) throws IOException{
		FileReader f = new FileReader(filename);
		String text = "";
		int c;
		while ((c = f.read()) != -1)
			text += (char)c;
		
		f.close();
		int ctr = 0;
		boolean in_exp = false;
		String exp = "";
		char current;
		ArrayList<String> db_list = new ArrayList<String>();
		for(int i = 0; i<text.length();i++){
			current = text.charAt(i);
			if(current == '('){
				in_exp = true;
				ctr += 1;
			}
			if(current == ')')
				ctr -= 1;
			if(in_exp && ctr > 0)
				exp += current;
			if(ctr == 0 && in_exp){
				in_exp = false;		
				db_list.add(exp + ')');
				exp = "";
			}
		}
		DB_SIZE = db_list.size()+1;
		Token[] db = new Token[db_list.size() + 1];
		for(int i = 0; i < db_list.size(); i++)
			db[i] = preprocess(Parser.tokenize(db_list.get(i)));
		return db;
	}		

	public static void print_rules(HashMap<String, Token>varargs){
			Object[] keys =  varargs.keySet().toArray();	
			System.out.println("Rules: ");			
			for(int j = 0;j<keys.length;j++){
				System.out.printf("%s ", keys[j]);
				varargs.get(keys[j]).print();
				System.out.printf("\n");
			}
			return;
	}	

	public static boolean is_rule(Token query){
		return query.data[0].leaf != null && query.data[0].leaf.equals("rule");
	}

	public static boolean is_call(Token query){
		return RULES.get(query.data[0].leaf) != null;
	}
	
	public static Token deal_with_rules(Token query){
		Token t;
		Token vars;
		HashMap<String,Token> varargs = new HashMap<>();
		HashMap<String, Token> argvars = new HashMap<>();
		if(is_leaf(query))
			return query;
		else if(is_call(query)){
			t = RULES.get(query.data[0].leaf).data[3];
			t.args = RULES.get(query.data[0].leaf).data[2];
			for(int i = 0; t.args.data[i] != null; i++){
				if(is_var(query.data[1].data[i]))
					varargs.put(t.args.data[i].leaf, query.data[1].data[i]);
				else
					argvars.put(t.args.data[i].leaf, query.data[1].data[i]);
			}
			t = t.bind_vars(argvars);
			return deal_with_rules(t.bind_vars(varargs));
		}else{
			Token[] data = new Token[Parser.CODELEN];
			int i;
			for(i = 0; query.data[i] != null; i++)
				data[i] = deal_with_rules(query.data[i]);
			return new Token(data, i);
		}
	}
		
	public static Token preprocess(Token q){
		if(is_rule(q)){
			q = uniqify_vars(q);
			q.args = q.data[2];
			RULES.put(q.data[1].leaf, q);
		}
		return deal_with_rules(q);
	}

	public static boolean is_func_var(Token q, HashMap<String,Token> varargs){
			Object[] keys =  varargs.keySet().toArray();	
			for(int j = 0;j<keys.length;j++){
				if(q.leaf.equals(varargs.get(keys[j]).leaf))
					return true;
			}
			return false;
	}			

	public static Token uniqify_internal_vars(Token rule_query, HashMap<String,Token> varargs, HashMap<String,Token> internal_varargs){
		Token t;
		Token[] data = new Token[Parser.CODELEN];
		if(is_var(rule_query) && !is_func_var(rule_query, varargs)){
			if(internal_varargs.get(rule_query.leaf) != null)
				return internal_varargs.get(rule_query.leaf);
			t = new Token("?var"+((Integer)VAR_CTR).toString());
			internal_varargs.put(rule_query.leaf, t);
			VAR_CTR++;
			return t;
		}if(rule_query.leaf != null){
			return rule_query;
		}
		int i;
		for(i=0;rule_query.data[i] != null; i++){
			data[i] = uniqify_internal_vars(rule_query.data[i], varargs, internal_varargs);
		}
		return new Token(data, i);
	}	

	public static Token uniqify_vars(Token rule_query){
		Token args = rule_query.data[2];
		HashMap<String,Token> varargs = new HashMap<>();
		for(int i = 0; args.data[i] != null; i++){
			varargs.put(args.data[i].leaf, new Token("?var"+((Integer)VAR_CTR).toString()));
			VAR_CTR++;
		}
		return uniqify_internal_vars(rule_query.bind_vars(varargs), varargs, new HashMap<String,Token>());
	}

	public static void present_results(Token query, Token[] results){
		if(results[0] != null && results[0].varargs.size() == 0){
			for(int i = 0; results[i] != null; i++){
				results[i].print();
				System.out.println();
			}
			return;
		}		
		int length;
		for(length=0;results[length] != null; length++);
		int ctr = 0;		
		Token[] ret = new Token[length+1];
		for(int i = 0; results[i] != null; i++){
			if(!query_in(ret,query.bind_vars(results[i].varargs))){
				ret[ctr] = query.bind_vars(results[i].varargs);
				ctr ++;
			}
		}
		ret[ctr] = null;
		for(int i = 0;ret[i] != null; i++){
			ret[i].print();
			System.out.println();
		}		
		return;
	}

	public static boolean is_valid(Token result){
			HashMap<String,Token> varargs = result.varargs;
			Object[] keys =  varargs.keySet().toArray();	
			for(int j = 0;j<keys.length;j++){
				for(int i=0;i<keys.length;i++){
					if(!keys[j].equals(keys[i]) && same_meaning(varargs.get(keys[j]), varargs.get(keys[i]), varargs))
						return false;
				}
			}
			return true;
	}	
	public static Token[] filter_sameness(Token[] results){
		int length;
		int ctr = 0;
		for(length = 0; results[length] != null; length++);
		Token[] ret = new Token[length+1];
		for(length = length-1;length>-1;length--){
			if(is_valid(results[length])){
				ret[ctr] = results[length];
				ctr++;		
			}
		}
		ret[ctr] = null;
		return ret;
	}

	public static void qREPL(Token[] db){
		Scanner inp = new Scanner(System.in);
		String exp;
		Token q;
		Token raw_q;
		int ctr = 0;
		Token[] new_db = new Token[1];
		while(true){
			System.out.printf("\n=> ");
			exp = inp.nextLine();
			try{
				raw_q = Parser.tokenize(exp);
				q = preprocess(Parser.tokenize(exp));
				//q.print();
				//System.out.println();
				//raw_q.print();
				//System.out.println();
				//System.exit(1);
				if(is_rule(raw_q)){
					System.out.printf("rule %s added!\n", raw_q.data[1].leaf);
				}
				else{
					new_db = filter_sameness(qeval(q, db));
					present_results(raw_q, new_db);
				}
				ctr++;
			}catch (Exception e){
				System.out.println("Input error!");
			}
		}
		//return;
	} 

	public static boolean is_var(Token exp){
		return exp.leaf != null && exp.leaf.charAt(0) == '?';
	}				

	public static boolean is_leaf(Token exp){
		return exp.leaf != null;
	}
	
	public static void print_bindings(HashMap<String, Token>varargs){
			Object[] keys =  varargs.keySet().toArray();	
			System.out.println("Varargs: ");			
			for(int j = 0;j<keys.length;j++){
				System.out.printf("%s ", keys[j]);
				varargs.get(keys[j]).print();
				System.out.printf("\n");
			}
			return;
	}			
	
	public static boolean same_meaning(Token a, Token b, HashMap<String, Token> varargs){
		if(a == null && b == null)
			return true;
		if((a == null && b != null) || (b == null && a != null))
			return false;
		if(is_var(a) && is_var(b))
			return a.leaf.equals(b.leaf);
	//	if(is_leaf(a) && is_leaf(b) && a.leaf.charAt(0) != '?' && b.leaf.charAt(0)!='?')
	//		return a.leaf.equals(b.leaf);
		if(is_var(a)){
			if(varargs.get(a.leaf) != null){
				a = varargs.get(a.leaf);
				return same_meaning(a, b, varargs);
			}	
			varargs.put(a.leaf, b);
			return true;
		}
		if(is_leaf(a) && is_leaf(b))
			return a.leaf.equals(b.leaf);
		if(! (!is_leaf(a) && !is_leaf(b)))
			return false;
		if(a.length != b.length)
			return false;
		for(int i = 0; i < a.length; i++){
			if(!same_meaning(a.data[i], b.data[i], varargs))
				return false;
		}
		return true;
	}

	public static boolean same_structure(Token a, Token b){
		if(is_var(a))
			return true;
		if(is_leaf(a) && is_leaf(b))
			return true;
		if(! (!is_leaf(a) && !is_leaf(b)))
			return false;
		if(a.length != b.length)
			return false;
		for(int i = 0; i < a.length; i++){
			if( !same_structure(a.data[i], b.data[i]))
				return false;
		}
		return true;
	}
				
	public static Token[] qeval_simple(Token query, Token[] db){
		Token[] new_db = new Token[DB_SIZE + 1];
		int j = 0;
		HashMap<String,Token> varargs;
		for(int i = 0; i < DB_SIZE; i++){
			varargs = new HashMap<String,Token>();
			if(same_meaning(query, db[i], varargs)){
				new_db[j] = db[i].copy();
				new_db[j].varargs = varargs;
				j++;
			}
		}
		new_db[j] = null;
		return new_db;				
	}	
			
	public static HashMap<String,Token> combine_varargs(HashMap<String,Token> d1, HashMap<String,Token> d2){
		HashMap<String,Token> d3 = new HashMap<String,Token>();
		d3.putAll(d1);
		d3.putAll(d2);
		return d3;
	}

	public static boolean have_same_bindings(Token t1, Token t2){
			Object[] keys =  t1.varargs.keySet().toArray();			
			for(int j = 0;j<keys.length;j++){
				if(t2.varargs.get(keys[j]) != null  && !same_meaning(t1.varargs.get(keys[j]), t2.varargs.get(keys[j]), t1.varargs)){
					return false;
				}
			}
			return true;
	}					

	public static Token[] from_list_to_array(ArrayList<Token> list){
		Token[] ret = new Token[list.size()+1];
		for(int i = 0; i<list.size(); i++)
			ret[i] = list.get(i);
		return ret;
	}

	public static Token[] and_unify(Token[] new_db, Token[] tmp_db){
		Token res;
		ArrayList<Token> ret_list = new ArrayList<>();
		for(int i = 0; new_db[i] != null; i++){
			for(int j = 0; tmp_db[j] != null; j++){
				res = new Token(new Token[Parser.CODELEN], new_db[0].length+1);	
				int k;
				for(k = 0; k < new_db[0].length;k++){
					res.data[k] = new_db[i].data[k];
				}
				res.data[k] = tmp_db[j];
				if(have_same_bindings(res.data[k], res.data[k-1])){
					res.varargs = combine_varargs(res.data[k].varargs, res.data[k-1].varargs);				
					ret_list.add(res);
				}
			}
		}	
		return from_list_to_array(ret_list);
	}
	
	public static ArrayList<HashMap<String,Token>> or_combinations(HashMap<String,Token> v1, HashMap<String,Token> v2){
		ArrayList<HashMap<String,Token>> ret = new ArrayList<>();
		HashMap<String,Token> tmp;
		Object[] keys2 = v2.keySet().toArray();
		Object[] keys1 = v1.keySet().toArray();	
		for(int j = 0;j<keys2.length;j++){
			if(v1.get(keys2[j]) == null){
				tmp = new HashMap<String,Token>(v1);
				for(int i=0;i<keys2.length;i++)
					if(v1.get((String)keys2[i]) == null)
						tmp.put((String)keys2[i], v2.get((String)keys2[i]));
				ret.add(tmp);
			}else if(!same_meaning(v1.get((String)keys2[j]), v2.get((String)keys2[j]), v1)){
				tmp = new HashMap<String,Token>(v1);
				for(int i=0;i<keys2.length;i++)
					if(v1.get((String)keys2[i]) == null)
						tmp.put((String)keys2[i], v2.get((String)keys2[i]));
				ret.add(tmp);
				tmp = new HashMap<String,Token>(v2);
				for(int i=0;i<keys1.length;i++)
					if(v2.get((String)keys1[i]) == null)
						tmp.put((String)keys1[i], v1.get((String)keys1[i]));
				ret.add(tmp);
			}else if(same_meaning(v1.get((String)keys2[j]), v2.get((String)keys2[j]), v1)){
				tmp = new HashMap<String,Token>(v1);
				for(int i = 0; i<keys2.length;i++)
					if(v1.get((String)keys2[i]) == null)
						tmp.put((String)keys2[i], v2.get((String)keys2[i]));
				ret.add(tmp);	
			}	

		}
		return ret;
	}			

	public static ArrayList<HashMap<String,Token>> or_unify(ArrayList<HashMap<String,Token>> new_db, ArrayList<HashMap<String,Token>> tmp_db){
		HashMap<String,Token> new_varargs;
		ArrayList<HashMap<String,Token>> ret = new ArrayList<>();
		int ctr = 0;
		for(int i = 0; i<new_db.size(); i++){
			for(int j = 0; j<tmp_db.size(); j++){
				ret.addAll(or_combinations(new_db.get(i), tmp_db.get(j)));
			}
		}
		return ret;
	}
	public static Token[] listified_first(Token[] tokens){
		ArrayList<Token> ret_list = new ArrayList<>();
		Token t;
		for(int i = 0; tokens[i] != null; i++){
			t = new Token(new Token[Parser.CODELEN], 1);
			t.data[0] = tokens[i];
			ret_list.add(t);
		}
		return from_list_to_array(ret_list);
	}
	
	public static Token[] prepend_str(Token[] db, String str){	
		ArrayList<Token> ret_list = new ArrayList<>();
		for(int i = 0; db[i] != null; i++){
			Token tmp = new Token(new Token[Parser.CODELEN], db[i].length+1);
			tmp.data[0] = new Token(str);
			tmp.varargs = db[i].varargs;
			for(int j = 1; db[i].data[j-1] != null; j++){
				tmp.data[j] = db[i].data[j-1];
			}		
			ret_list.add(tmp);
		}
		return from_list_to_array(ret_list);
	}	
	public static Token[] qeval_and(Token query, Token[] db){
		Token[] new_db = null;
		Token[] tmp_db = qeval(query.data[1], db);
		if(tmp_db[0] == null)
			return tmp_db;
		new_db = listified_first(tmp_db);
		for(int i = 2;query.data[i] != null; i++){
			tmp_db = qeval(query.data[i], db);
			if(tmp_db[0] == null)
				return tmp_db;
			new_db = and_unify(new_db, tmp_db);		
		}
		return prepend_str(new_db, "and");				 
	}		

	public static ArrayList<HashMap<String,Token>> get_bindings_list(Token[] ts){
		ArrayList<HashMap<String,Token>> ret = new ArrayList<>();
		for(int i = 0; ts[i] != null; i++){
			ret.add(ts[i].varargs);
		}
		return ret;
	}
	
	public static boolean query_in(Token[] queries, Token q){
		for(int i = 0;queries[i] != null;i++)
			if(same_meaning(queries[i], q, queries[i].varargs))
				return true;
		return false;
	}

	public static Token[] use_bindings_list(ArrayList<HashMap<String,Token>> new_db, Token query){
		ArrayList<Token> ret_list = new ArrayList<>();
		Token t;
		int ctr = 0;
		for(int i = 0; i<new_db.size(); i++){
			t = query.bind_vars(new_db.get(i));
			if(!query_in(from_list_to_array(ret_list), t)){
				ret_list.add(query.bind_vars(new_db.get(i)));
				ret_list.get(ctr).varargs = new_db.get(i);
				ctr++;
			}
		}
		return from_list_to_array(ret_list);
	}

	public static Token[] qeval_or(Token query, Token[] db){
		ArrayList<HashMap<String,Token>> new_db = new ArrayList<>();
		ArrayList<HashMap<String,Token>> tmp_db = new ArrayList<>();
		for(int i = 1;query.data[i] != null; i++){
			tmp_db = get_bindings_list(qeval(query.data[i], db));
			if(tmp_db.size() == 0)
				continue;
			else if(new_db.size() == 0)		
				new_db = tmp_db;
			else
				new_db = or_unify(new_db, tmp_db);
		}
		return use_bindings_list(new_db, query);
	}
	
	public static boolean is_and(Token query){
		return query.data[0].leaf != null && query.data[0].leaf.equals("and");
	}
	public static boolean is_or(Token query){
		return query.data[0].leaf != null && query.data[0].leaf.equals("or");
	}

	public static Token[] qeval(Token query, Token[] db){
		if(is_and(query))
			return qeval_and(query, db);
		if(is_or(query))
			return qeval_or(query, db);
		return qeval_simple(query, db);
	
	}			
}


class Token{
	public String leaf;
	public Token[] data;
	public int length;
	public boolean is_root = false;
	public HashMap<String,Token> varargs;
	public Token args;
	
	public Token bind_vars(HashMap<String,Token> varargs){
			Object[] keys =  varargs.keySet().toArray();
			Token tmp = this;	
			for(int j = 0;j<keys.length;j++){
				tmp = tmp.replace_var((String)keys[j], varargs.get(keys[j]));
			}
			return tmp;
	}		

	public Token replace_var(String var, Token replacement){
		if(leaf != null && leaf.equals(var)){
			return replacement;
		}else if(leaf != null){
			return new Token(leaf);
		}else{
			Token t = new Token(new Token[Parser.CODELEN], length);
			for(int i=0;i<length;i++){
				t.data[i] = data[i].replace_var(var, replacement);
			}
			return t;
		}
	}

	public Token copy(){
		Token t = new Token("");
		t.leaf = this.leaf;
		t.data = this.data;
		t.length = this.length;
		t.is_root = this.is_root;
		t.varargs = this.varargs;
		return t;
	}		

	public Token(String str){
		leaf = str;
		data = null;
		return;
	}

	public Token(Token[] data, int length){
		this.data = data;
		this.leaf = null;
		this.length = length;
		return;
	}

	public void print(){
		if(leaf != null){
			System.out.printf(leaf);
			return;	
		}
		System.out.printf("(");
		int i = 0;
		while(data[i] != null){
			data[i].print();
			if(data[i+1] != null)
				System.out.printf(" ");
			i++;
		}
		System.out.printf(")");
		return;
	}
}

class Parser {
	public static final int CODELEN = 100;
	
	public static boolean is_leaf(String exp){
		return exp.charAt(0) != '(';
	}

	public static Token tokenize(String exp){
		if(is_leaf(exp))
			return new Token(exp);
		String[] parsed = parse(exp);
		int i = 0;
		Token[] data = new Token[CODELEN];
		while(parsed[i] != null){
			data[i] = tokenize(parsed[i]);
			i++;
		}
		data[i] = null;
		return new Token(data, i);
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

}

