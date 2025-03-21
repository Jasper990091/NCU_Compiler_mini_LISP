from lark import Lark, Transformer, v_args, Token, UnexpectedInput, UnexpectedToken, UnexpectedCharacters
import sys

with open('lisp.lark') as larkfile:
    parser = Lark(larkfile, start='program', parser='lalr', lexer='contextual')

def print_num(*token):
    print(token[0])
    return

def print_bool(*token):
    if(token[0]): print("#t")
    else: print("#f")
    return

def plus(*token):
    return sum(token)

def minus(*token):
    return token[0] - token[1]

def multiply(*token):
    sum = 1
    for i in token:
        sum *= i
    
    return sum

def devide(*token):
    return token[0] // token[1]

def modulus(*token):
    return token[0] % token[1]

def greater(*token):
    return bool(token[0] > token[1])

def smaller(*token):
    return bool(token[0] < token[1])

def equal(*token):
    return bool(token.count(token[0]) == len(token))

def and_op(*token):
    return all(token)

def or_op(*token):
    return any(token)

def not_op(*token):
    return not token[0]

basicFunctions = {
    'print_num' : print_num,
    'print_bool' : print_bool,
    'plus' : plus,
    'minus' : minus,
    'multiply' : multiply,
    'devide' : devide,
    'modulus' : modulus,
    'greater' : greater,
    'smaller' : smaller,
    'equal' : equal,
    'and_op' : and_op,
    'or_op' : or_op,
    'not_op' : not_op
}
        
class userFunction:
    def __init__(self, rootnode, params = tuple()):
        self.rootnode = rootnode
        self.params = params
    
    def __call__(self, *param):
        newscope = dict()
        for i in range(len(self.params)):
            newscope[self.params[i]] = param[i]
        
        return traverseAST(self.rootnode, newscope)
    
def traverseAST(node, scope):
    try:
        return int(node)
    except:
        if(node == "#t"): return True
        elif(node == "#f"): return False
        elif(isinstance(node, str)):
            if(scope is None):
                return globalscope[node]
            else:
                if(node in scope): return scope[node]
                else: return globalscope[node]
        
        if(node.data == "program"):
            for i in node.children:
                traverseAST(i, scope)
            return
        elif(node.data == "if_exp"):
            if(traverseAST(node.children[0], scope)):
                return traverseAST(node.children[1], scope)
            else:
                return traverseAST(node.children[2], scope)
        elif(node.data == "def_stmt"):
            name = str(node.children[0])
            if(scope is None):
                globalscope[name] = traverseAST(node.children[1], scope)
            else:
                scope[name] = traverseAST(node.children[1], scope)
            
        elif(node.data == "fun_exp"):
            params = node.children[:-1]
            rootnode = traverseAST(node.children[-1], scope)
            return userFunction(rootnode, params)
        elif(node.data == "fun_body"):
            return node.children[0]
        elif(node.data == "fun_call"):
            fun = traverseAST(node.children[0], scope)
            params = []
            for i in node.children[1:]:
                params.append(traverseAST(i, scope))
            return fun(*params)
        else:
            fun = basicFunctions[node.data]
            tokens = []
            for i in node.children:
                tokens.append(traverseAST(i, scope))
            return fun(*tokens)
        
if __name__ == '__main__':
    try:
        userinput = sys.stdin.read()
        tree = parser.parse(userinput)
        #print(tree.pretty())
    except Exception as e:
        print("syntax error")
    else:
        global globalscope
        globalscope = dict()
        traverseAST(tree, None)
