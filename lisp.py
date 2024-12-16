from lark import Lark, Transformer, v_args, Token, UnexpectedInput, UnexpectedToken, UnexpectedCharacters
import argparse
import logging
import sys

variable_to_value = dict()

with open('lisp.lark') as larkfile:
    parser = Lark(larkfile, start='program', parser='lalr', lexer='contextual')
       
 
class MiniLispFunctions(Transformer):
    def num(self, token):
        return int(token[0])
    
    def boo(self, token):
        if(str(token[0]) == "#t"): return True
        else: return False
        
    def variable(self, token):
        return variable_to_value[str(token[0])]
    
    def var(self, token):
        return token[0]
    
    def print_num(self, token):
        print(token[0])
        return
    
    def print_bool(self, token):
        if(token[0]): print("#t")
        else: print("#f")
        return
    
    def plus(self, token):
        return sum(token)
    
    def minus(self, token):
        return token[0] - token[1]
    
    def multiply(self, token):
        sum = 1
        for i in token:
            sum *= i
        
        return sum
    
    def devide(self, token):
        return token[0] // token[1]
    
    def modulus(self, token):
        return token[0] % token[1]
    
    def greater(self, token):
        return bool(token[0] > token[1])
    
    def smaller(self, token):
        return bool(token[0] < token[1])
    
    def equal(self, token):
        return bool(token.count(token[0]) == len(token))
    
    def and_op(self, token):
        return all(token)
    
    def or_op(self, token):
        return any(token)
    
    def not_op(self, token):
        return not token[0]
    
    def num_op(self, token):
        return token[0]
    
    def logical_op(self, token):
        return token[0]
    
    def get_num(self, token):
        return token[0]
    
    def get_log(self, token):
        return token[0]
    
    def if_exp(self, token):
        if(token[0]): return token[1]
        else: return token[2]
        
    def get_if(self, token):
        return token[0]
    
    def def_stmt(self, token):
        variable_to_value[str(token[0])] = token[1]
        
    
    

if __name__ == '__main__':
    try:
        userinput = sys.stdin.read()
        tree = parser.parse(userinput)
        #print(tree.pretty())
        result = MiniLispFunctions().transform(tree)
    
    except Exception as e:
        print("syntax error")
    