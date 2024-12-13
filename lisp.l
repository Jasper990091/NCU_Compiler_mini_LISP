%option noyywrap
%{
#include<stdio.h>
#include<stdbool.h>
#include<string.h>
#include "y.tab.h"
%}

NUMBER 0|[1-9][0-9]*|"-"[1-9][0-9]*
BOOL "#t"|"#f"
ID [a-z]([a-z]|[0-9]|"-")*
SEP [ \t\n\r]+

%%
{NUMBER} {
    sscanf(yytext, "%d", &(yylval.intNum));
    return NUM;
}
"mod" {return MOD;}
"print-num" {return PNUM;}
"print-bool" {return PBOOL;}
"and" {return AND;}
"or" {return OR;}
"not" {return NOT;}
"define" {return DEF;}
"fun" {return FUN;}
"if" {return IF;}
"(" {return LEFTBRC;}
")" {return RIGHTBRC;}
"+" {return PLUS;}
"-" {return MIN;}
"*" {return MUL;}
"/" {return DIV;}
">" {return BIG;}
"<" {return SMALL;}
"=" {return EQUAL;}

{ID} {
    sscanf(yytext, "%s", &(yylval.string));
    return ID;
}
{BOOL} {
    sscanf(yytext, "%s", &(yylval.string));
    return BOOL;
}
{SEP} {}
. {}


%%

