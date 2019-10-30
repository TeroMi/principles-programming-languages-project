#!/usr/bin/env python3
import ply.yacc as yacc
import lexer
tokens = lexer.tokens

import ply.yacc as yacc
# E <- 3 + 2.

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV')
)

def p_variable_definitions(p):
    '''variable_definitions : varIDENT LARROW simple_expression DOT
                            | constIDENT LARROW constant_expression DOT'''
    p[0] = p[1]
    print("variable_definition({})".format(p[1]))


def p_simple_expression(p):
    '''simple_expression : term PLUS term
                         | term MINUS term
                         | term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    if p[2] == '-':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1]
    print("simple_expression")


def p_constant_expression(p):
    '''constant_expression : constIDENT
                           | NUMBER_LITERAL'''
    p[0] = p[1]
    print("constant_expression({})".format(p[1]))

def p_term(p):
    '''term : factor MULT factor
            | factor DIV factor
            | factor'''
    if len(p) == 4:
        print("term({}{}{})".format(p[1], p[2], p[3]))
    else:
        print("term")

def p_factor(p):
    '''factor : atom
              | MINUS atom'''
    print("factor")


def p_atom(p):
    # | SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE
    '''atom : NUMBER_LITERAL
            | STRING_LITERAL
            | varIDENT
            | constIDENT
            | LPAREN simple_expression RPAREN'''
    if len(p) == 4:
        print("atom")
    else:
        print("atom({})".format(p[1]))


def p_error(p):
    print("ERROR in token {} {}".format(p.type, p.value))


parser = yacc.yacc(debug=True)


if __name__ == '__main__':
    import argparse, codecs
    argument_parser = argparse.ArgumentParser()
    argument_group = argument_parser.add_mutually_exclusive_group()
    argument_group.add_argument('--who', action='store_true', help='author')
    argument_group.add_argument('-f', '--file', help='<FILENAME>.tupl')

    input_args_parsed = argument_parser.parse_args()
    if input_args_parsed.who:
        print("Author: 283121 Tero Mielikäinen")
    elif input_args_parsed.file is None:
        argument_parser.print_help()
    else:
        file = input_args_parsed.file
        try:
            with codecs.open(file, 'r') as INFILE:
                data = INFILE.read()
                result = parser.parse(data, lexer=lexer.lexer, debug=False)
                if result is None:
                    print("Syntax correct")
        except FileNotFoundError:
            print("File not found: '{}', maybe you forgot or mistyped the suffix".format(file))