from lark import Lark, Transformer, v_args, Token, UnexpectedInput, UnexpectedToken, UnexpectedCharacters
import argparse
import logging
import sys

variable_to_value = dict()

with open('lisp.lark') as larkfile:
    parser = Lark(larkfile, start='program', parser='lalr', lexer='contextual')
       

class variableToValue(dict):
    def print_num(self, *token):
        print(token[0])
        return
    
    def print_bool(self, *token):
        if(token[0]): print("#t")
        else: print("#f")
        return
    
    def plus(self, *token):
        return sum(token)
    
    def minus(self, *token):
        return token[0] - token[1]
    
    def multiply(self, *token):
        sum = 1
        for i in token:
            sum *= i
        
        return sum
    
    def devide(self, *token):
        return token[0] // token[1]
    
    def modulus(self, *token):
        return token[0] % token[1]
    
    def greater(self, *token):
        return bool(token[0] > token[1])
    
    def smaller(self, *token):
        return bool(token[0] < token[1])
    
    def equal(self, *token):
        return bool(token.count(token[0]) == len(token))
    
    def and_op(self, *token):
        return all(token)
    
    def or_op(self, *token):
        return any(token)
    
    def not_op(self, *token):
        return not token[0]
    
    def if_exp(self, token):
        if(token[0]): return token[1]
        else: return token[2]
        
    def def_stmt(self, token):
        variable_to_value[str(token[0])] = token[1]
    
    def __init__(self, first = False, variables = tuple(), values = tuple(), previous = None):
        super(variableToValue, self).__init__()
        if(first):
            self['print_num'] = self.print_num
            self['print_bool'] = self.print_bool
            self['plus'] = self.plus
            self['minus'] = self.minus
            self['multiply'] = self.multiply
            self['devide'] = self.devide
            self['modulus'] = self.modulus
            self['greater'] = self.greater
            self['smaller'] = self.smaller
            self['equal'] = self.equal
            self['and_op'] = self.and_op
            self['or_op'] = self.or_op
            self['not_op'] = self.not_op
        
        self.update(zip(variables, values))
    
def traverseAST(node, scope):
    if(not scope):
        scope = variableToValue(first = True)

    try:
        return int(node)
    except:
        if(node == "#t"): return True
        elif(node == "#f"): return False
        elif(isinstance(node, str)):
            return scope[node]
        
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
            scope[name] = traverseAST(node.children[1], scope)
        else:
            fun = traverseAST(node.data, scope)
            tokens = []
            for i in node.children:
                tokens.append(traverseAST(i, scope))
            return fun(*tokens)
        
if __name__ == '__main__':
    #try:
    userinput = sys.stdin.read()
    tree = parser.parse(userinput)
    #print(tree.pretty())
    traverseAST(tree, None)
    '''
    except Exception as e:
        print("syntax error")
    else:
        
    '''
    