import codecs
import sys

def cons(x,y):
    return lambda m: m(x,y)

def car(z):
    return z(lambda x,y: x)
def cdr(z):
    return z(lambda x, y: y)

def scheme_list():
    return None

class Queue(object):
    def __init__(self):
        self.queue = []
        self.last_pair = None
    def enqueue(self, x):
        if self.queue == []:
            self.last_pair = [x, None]
            self.queue = self.last_pair
        else:
            self.last_pair[1] = [x, None]
            self.last_pair = self.last_pair[1]
    def dequeue(self):
        if self.queue[1] == None:
            self.queue = []
            self.last_pair = None
        else:
            self.queue = self.queue[1]
    def front(self):
        return self.queue[0]
    def back(self):
        return self.last_pair[0]

    def __str__(self):
        if self.queue == []:
            return '(queue)'
        queue = ['(queue']
        rest = self.queue
        while rest:
            queue.append(' ' + str(rest[0]))
            rest = rest[1]
        queue.append(')')
        return ''.join(queue)

class Stack(object):
    def __init__(self):
        self.stack = []
    def push(self, elt):
        self.stack.append(elt)
    def pop(self):
        x = self.stack.pop()
        return x
    def top(self):
        return self.stack[-1]
    def __str__(self):
        if self.stack == []:
            return '(stack)'
        stack = ['(stack']
        s = self.stack
        for i in range(len(self.stack)-1, -1, -1):
            stack.append(' ' + str(s[i]))
        stack.append(')')
        return ''.join(stack)

def exp_to_exp_stack(exp):
    exp_stack = Stack()
    at_word = False
    for i in range(len(exp)-1, -1, -1):
        if exp[i] in '() ':
            at_word = False
            exp_stack.push(exp[i])
        elif exp[i] not in '() ' and at_word:
            word = exp_stack.pop()
            word = exp[i] + word
            exp_stack.push(word)
        elif not at_word and exp[i] not in '() ':
            at_word = True
            exp_stack.push(exp[i])
        else:
            exp_stack.push(exp[i])
    return exp_stack

def make_into_lst(exp_stack):
    if exp_stack.stack == [')', '(']:
        return '()'
    stack = Stack()
    linked_lst = scheme_list()
    in_string = False
    while len(exp_stack.stack) > 1 or (not hasattr(exp_stack.top(), '__call__')):
        i = exp_stack.pop() 
        if i == '"':
            in_string = not in_string       
        if i == ')':
            while stack.stack:
                elt = stack.pop()
                if elt == '(':
                    exp_stack.push(linked_lst)
                    linked_lst = scheme_list()
                    break
                else:
                    linked_lst = cons(elt, linked_lst)
        elif (i != ' ' and i != '\n') or (i == '\n' and in_string):
            stack.push(i)
    return exp_stack.top()

def tree_str(tree):
    ans = ['(']
    while tree:
        if isinstance(car(tree), str) or isinstance(car(tree), dict):
            ans.append(str(car(tree)))
        else:
            ans.extend(tree_str(car(tree)))
        tree = cdr(tree)
    ans.append(')')
    return ans

def print_tree(tree_str):
    string = ''
    for i in range(len(tree_str)):
        symbol = tree_str[i]
        if i-1 > -1:
            left = tree_str[i-1]
        else:
            left = '()'
        if i+1 < len(tree_str):
            right = tree_str[i+1]
        else:
            right = '()'

        if symbol == '(':
            if left == ')' or (left not in '()'):
                string += (' ' + symbol)
            else:
                string += symbol

        elif symbol == ')':
            if i+1 == len(tree_str) or tree_str[i+1] == ')' or tree_str[i-1] == ')':
                string += symbol
            else:
                string += (symbol + ' ')
        elif left == '(' and right == '(':
            string += symbol
        elif left == '(' and right == ')':
            string += symbol + ' '
        elif left == ')' and right == ')':
            string += ' ' + symbol
        elif left not in '()' and right in '()':
            string += (' ' + symbol)
        elif right not in '()' and left in '()':
            string += (symbol + ' ')
        else:
            string += (' ' + symbol + ' ')

    return string

def get_input_exp():
    while True:
        print('in: '),
        function = raw_input()
        try:
            print('out:'), print_tree(tree_str(make_into_lst(exp_to_exp_stack(function))))
        except:
            if function == 'quit':
                break

def listify(body):
    ret = []
    if isinstance(body, str):
        return body
    else:
        while body:
            ret.append(listify(car(body)))
            body = cdr(body)
    return ret

def strip_listified(body):
	ret = []
	for i in body:
		if isinstance(i, list):
			ret.append(strip_listified(i))
		elif isinstance(i, str) and i.strip():
			ret.append(i.strip())		
	return ret
	


