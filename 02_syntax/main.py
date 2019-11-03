#!/usr/bin/env python3
import ply.yacc as yacc
import lexer
tokens = lexer.tokens

import ply.yacc as yacc
# E <- 3 + 2.


def p_program(p):
    '''program : program return_value DOT
               | variable_definitions
               | return_value DOT'''
    print("program")


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definitions'''


def p_function_definition(p):
    ''''''

def p_formals(p):
    '''formals : varIDENT formals
               | COMMA varIDENT
               | COMMA varIDENT formals
               | varIDENT '''


def p_return_value(p):
    '''return_value : EQ simple_expression'''


def p_variable_definitions(p):
    '''variable_definitions : varIDENT LARROW simple_expression DOT
                            | constIDENT LARROW constant_expression DOT'''

    if p.slice[1].type == 'varIDENT':
        print("variable_definition({})".format(p[1]))
    elif p.slice[1].type == 'constIDENT':
        print("constant_definition({})".format(p[1]))



def p_constant_expression(p):
    '''constant_expression : constIDENT
                           | NUMBER_LITERAL'''


def p_arguments(p):
    '''arguments : simple_expression arguments
                 | COMMA simple_expression
                 | COMMA simple_expression arguments
                 | simple_expression'''


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


def p_factor(p):
    '''factor : atom
              | MINUS atom'''
    print("factor")


def p_term(p):
    '''term : factor
            | term MULT factor
            | term DIV factor'''
    if len(p) == 4:
        print("term({}{}{})".format(p[1], p[2], p[3]))
    else:
        print("term")


def p_simple_expression(p):
    '''simple_expression : term
                         | simple_expression PLUS term
                         | simple_expression MINUS term
                         '''
    print("simple_expression")


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("ERROR in token {}".format(p.error))


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