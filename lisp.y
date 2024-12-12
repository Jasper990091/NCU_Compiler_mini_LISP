%{
#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<string.h>

int yylex(void);
void yyerror(const char *s){

}
extern char* yytext;

%}

%union {
    int intNum;
    char string[10000];
    int pair[2];
}
%token <intNum> NUM
%token <string> BOOL

%token ID SEP LEFTBRC RIGHTBRC PLUS MIN MUL DIV MOD PNUM PBOOL BIG SMALL EQUAL AND OR NOT DEF FUN IF

%type <pair> exp num_op logical_op if_exp and_op or_op not_op exp_plus exp_multiply exp_and exp_or exp_equal plus minus multiply devide modulus greater smaller equal

%%
program: stmts
    | error{
        printf("syntax error\n");
        exit(0);
    }
    ;

stmts: stmt
    | stmts stmt
    ;

stmt: exp
    | def_stmt
    | print_stmt
    ;

print_stmt: LEFTBRC PNUM exp RIGHTBRC{
        printf("%d\n", $3[1]);
    }
    | LEFTBRC PBOOL exp RIGHTBRC{
        if($3[1] == 1) printf("#t\n");
        else printf("#f\n");
    }
    ;

exp: BOOL{
        $$[0] = 1;
        if(!strcmp($1, "#t")) $$[1] = 1;
        else $$[1] = 0;
    }
    | NUM{
        $$[0] = 0;
        $$[1] = $1;
    }
    | variable{
        $$[0] = 2;
    }
    | num_op{
        $$[0] = $1[0];
        $$[1] = $1[1];
    }
    | logical_op{
        $$[0] = $1[0];
        $$[1] = $1[1];
    }
    | fun_exp{
        $$[0] = 2;
    }
    | fun_call{
        $$[0] = 2;
    }
    | if_exp{
        $$[0] = $1[0];
        $$[1] = $1[1];
    }
    ;

num_op: plus{
        $$[0] = 0;
        $$[1] = $1[1];
    }
    | minus{
        $$[0] = 0;
        $$[1] = $1[1];
    }
    | multiply{
        $$[0] = 0;
        $$[1] = $1[1];
    }
    | devide{
        $$[0] = 0;
        $$[1] = $1[1];
    }
    | modulus{
        $$[0] = 0;
        $$[1] = $1[1];
    }
    | greater{
        $$[0] = 1;
        $$[1] = $1[1];
    }
    | smaller{
        $$[0] = 1;
        $$[1] = $1[1];
    }
    | equal{
        $$[0] = 1;
        $$[1] = $1[1];
    }
    ;

plus: LEFTBRC PLUS exp_plus RIGHTBRC{
    $$[0] = 0;
    $$[1] = $3[1];
};
minus: LEFTBRC MIN exp exp RIGHTBRC{
    $$[0] = 0;
    $$[1] = $3[1] - $4[1];
};
multiply : LEFTBRC MUL exp_multiply RIGHTBRC{
    $$[0] = 0;
    $$[1] = $3[1];
};
devide: LEFTBRC DIV exp exp RIGHTBRC{
    $$[0] = 0;
    $$[1] = $3[1] / $4[1];
};
modulus: LEFTBRC MOD exp exp RIGHTBRC{
    $$[0] = 0;
    $$[1] = $3[1] % $4[1];
};
greater: LEFTBRC BIG exp exp RIGHTBRC{
    $$[0] = 1;
    if($3[1] > $4[1]) $$[1] = 1;
    else $$[1] = 0;
};
smaller: LEFTBRC SMALL exp exp RIGHTBRC{
    $$[0] = 1;
    if($3[1] < $4[1]) $$[1] = 1;
    else $$[1] = 0;
};
equal: LEFTBRC EQUAL exp_equal RIGHTBRC{
    $$[0] = 1;
    $$[1] = $3[0];
};

logical_op: and_op{
        $$[0] = 1;
        $$[1] = $1[1];
    }
    | or_op{
        $$[0] = 1;
        $$[1] = $1[1];
    }
    | not_op{
        $$[0] = 1;
        $$[1] = $1[1];
    }
    ;

and_op: LEFTBRC AND exp_and RIGHTBRC{
    $$[0] = 1;
    $$[1] = $3[1];
};
or_op: LEFTBRC OR exp_or RIGHTBRC{
    $$[0] = 1;
    $$[1] = $3[1];
};
not_op: LEFTBRC NOT exp RIGHTBRC{
    $$[0] = 1;
    $$[1] = ($3[1] + 1) % 2;
};

def_stmt: LEFTBRC DEF variable exp RIGHTBRC
    ;

variable: ID;

fun_exp: LEFTBRC FUN fun_ids fun_body RIGHTBRC
    ;


fun_ids: LEFTBRC ids RIGHTBRC;
ids: ID
    | ids ID
    ;
fun_body: exp;
fun_call: LEFTBRC fun_exp exps RIGHTBRC 
    | LEFTBRC fun_name exps RIGHTBRC
    ;
exps: exp|exps exp;
fun_name: ID;

if_exp: LEFTBRC IF exp exp exp RIGHTBRC{
    if($3[1] == 1){
        $$[0] = $4[0];
        $$[1] = $4[1];
    }
    else{
        $$[0] = $5[0];
        $$[1] = $5[1];
    }
};

exp_plus: exp exp{
        $$[0] = 0;
        $$[1] = $1[1] + $2[1];
    }
    | exp_plus exp{
        $$[0] = 0;
        $$[1] = $1[1] + $2[1];
    }
    ;

exp_multiply: exp exp{
        $$[0] = 0;
        $$[1] = $1[1] * $2[1];
    }
    | exp_multiply exp{
        $$[0] = 0;
        $$[1] = $1[1] * $2[1];
    }
    ;

exp_equal: exp exp{
        if($1[1] == $2[1]) $$[0] = 1;
        else $$[0] = 0;
        $$[1] = $1[1];
    }
    | exp_equal exp{
        if($1[0] == 0) $$[0] = 0;
        else{
            if($1[1] == $2[1]) $$[0] = 1;
            else $$[0] = 0;
        }
        $$[1] = $1[1];
    }
    ;

exp_and: exp exp{
        $$[0] = 1;
        if($1[1] == 1 && $2[1] == 1) $$[1] = 1;
        else $$[1] = 0;
    }
    | exp_and exp{
        $$[0] = 1;
        if($1[1] == 1 && $2[1] == 1) $$[1] = 1;
        else $$[1] = 0;
    }
    ;

exp_or: exp exp{
        $$[0] = 1;
        if($1[1] == 1 || $2[1] == 1) $$[1] = 1;
        else $$[1] = 0;
    }
    | exp_or exp{
        $$[0] = 1;
        if($1[1] == 1 || $2[1] == 1) $$[1] = 1;
        else $$[1] = 0;
    }
    ;

%%

int main() {
    return yyparse(); 
}