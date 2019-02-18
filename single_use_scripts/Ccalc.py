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

class Token(object):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(self.val)

def is_operator(i):
    return str(i) in '+-/*negate()'
    
def is_left(i):
    return i in '+-/*'

precedence = {'+':0, '-': 0, '*': 1, '/': 1, 'negate': 2}

def str_to_infix(string):
    infix_queue = Queue()
    enqueue = lambda q, x: q.enqueue(x)
    k = 0
    while(k<len(string)):
        i = string[k]
        if i == ' ':
            k+=1
            continue
        if is_operator(i):
            if i == '-':
                if is_operator(str(infix_queue.back().val)):
                    enqueue(infix_queue, Token('negate'))
                else:
                    enqueue(infix_queue, Token(i))
            else:
                enqueue(infix_queue, Token(i))
            k+=1
        else:
            num = []
            for j in string[k:]:
                if is_operator(j):
                    break   
                num.append(j)
            k+=len(num)
            enqueue(infix_queue, Token(int("".join(num))))
    return infix_queue


def infix_to_postfix(infix_queue):
    outputQ = Queue()
    operator_stack = Stack()
    while(infix_queue.queue):
        token = infix_queue.front()
        if not is_operator(token.val):
            outputQ.enqueue(token)
        else:
            if token.val not in '()':
                while operator_stack.stack and operator_stack.top().val not in '()' and (precedence[operator_stack.top().val]>precedence[token.val] or (precedence[operator_stack.top().val] == precedence[token.val] and is_left(operator_stack.top().val))):
                    outputQ.enqueue(operator_stack.pop())
                operator_stack.push(token)
            else:
                if token.val == '(':
                    operator_stack.push(token)
                else:
                    while True:
                        if operator_stack.top().val == '(':
                            operator_stack.pop()
                            break
                        outputQ.enqueue(operator_stack.pop())
        infix_queue.dequeue()  
    while operator_stack.stack:
        outputQ.enqueue(operator_stack.pop())
    return outputQ

def eval_postfix(postfixQ):
    ans = Stack()
    while postfixQ.queue:
        token = postfixQ.front()
        if not is_operator(token.val):
            ans.push(token.val)
        else:
            if token.val == '+':
                ans.push(ans.pop() + ans.pop())
            if token.val == '-':
                right = ans.pop()
                ans.push(ans.pop() - right)
            if token.val == '/':
                right = ans.pop()
                ans.push(ans.pop()/float(right))
            if token.val == '*':
                ans.push(ans.pop()*ans.pop())
            if token.val == 'negate':
                ans.push(-ans.pop())

        postfixQ.dequeue()

    return ans.pop()     
           
while True:
    infixQ = str_to_infix(input("Expression: "))
    postfixQ = infix_to_postfix(infixQ)
    print("\t%f" % eval_postfix(postfixQ))











