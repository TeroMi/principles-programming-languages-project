#!/usr/bin/env python3
import ply.yacc as yacc
import lexer
tokens = lexer.tokens

import ply.yacc as yacc

precedence = (
     ('left', 'PLUS', 'MINUS'),
     ('left', 'MULT', 'DIV'),
     ('right', 'UMINUS')
 )


def p_program(p):
    '''program : function_or_variable_definition program
               | return_value DOT'''


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definitions
                                        | function_definition'''
    print("function_or_variable_definition")


def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
                             BEGIN \
                             return_value DOT \
                             END DOT'''
    print("func definition {}".format(p[2]))


def p_formals(p):
    '''formals : varIDENT formals
               | COMMA varIDENT
               | COMMA varIDENT formals
               | varIDENT '''
    print("formals")


def p_return_value(p):
    '''return_value : EQ simple_expression
                    | NOTEQ pipe_expression'''
    #print("return_value")


def p_variable_definitions(p):
    '''variable_definitions : varIDENT LARROW simple_expression DOT
                            | constIDENT LARROW constant_expression DOT
                            | tupleIDENT LARROW tuple_expression DOT
                            | pipe_expression RARROW tupleIDENT DOT'''

    if p.slice[1].type == 'varIDENT':
        print("variable_definition( {} )".format(p[1]))
    elif p.slice[1].type == 'constIDENT':
        print("constant_definition( {} )".format(p[1]))
    elif p.slice[1].type == 'tupleIDENT':
        print("tuple_definition( {} )".format(p[1]))
    else:
        print("tuple_definition ( {} )".format(p[3]))


def p_constant_expression(p):
    '''constant_expression : constIDENT
                           | NUMBER_LITERAL'''


def p_pipe_expression(p):
    '''pipe_expression : tuple_expression
                       | pipe_expression PIPE pipe_operation'''
    if len(p) == 2:
        print("pipe_expression")


def p_pipe_operation(p):
    '''pipe_operation : funcIDENT
                      | MULT
                      | PLUS
                      | each_statement'''
    #print("pipe_operation")


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom
                        | tuple_expression tuple_operation tuple_atom'''
    #print("tuple_expression")


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    #print("tuple_operation")


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT
                  | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                  | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
                  | LSQUARE arguments RSQUARE'''
    #print("tuple_atom")


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE RSQUARE
                     | '''


def p_arguments(p):
    '''arguments : simple_expression arguments
                 | COMMA simple_expression
                 | COMMA simple_expression arguments
                 | simple_expression'''
    #print("arguments")


def p_atom(p):
    '''atom : function_call
            | NUMBER_LITERAL
            | STRING_LITERAL
            | varIDENT
            | constIDENT
            | LPAREN simple_expression RPAREN
            | SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    if len(p) == 4:
        print("atom")
    else:
        print("atom( {} )".format(p[1]))


def p_unary_operator(p):
    '''unary_operator : MINUS'''


def p_factor(p):
    '''factor : atom
              | unary_operator atom %prec UMINUS'''
    print("factor")


def p_term(p):
    '''term : factor
            | term MULT factor
            | term DIV factor'''
    print("term")


def p_simple_expression(p):
    '''simple_expression : term
                         | simple_expression PLUS term
                         | simple_expression MINUS term
                         '''
    print("simple_expression")


'''def p_empty(p):
    'empty :'
    pass
'''

def p_error(p):
    if p is not None:
        print("{}:Syntax error (token:{})".format(p.lineno, p.value))
    else:
        print("Syntax error: {}".format(p))
    raise SystemExit


parser = yacc.yacc()


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
        '''while True:
            try:
                s = input('calc > ')
            except EOFError:
                break
            if not s: continue
            result = parser.parse(s, lexer=lexer.lexer, debug=True)
            print(result)
        '''
        try:
            with codecs.open(file, 'r') as INFILE:
                data = INFILE.read()
                result = parser.parse(data, lexer=lexer.lexer, debug=False)
                if result is None:
                    print("Syntax correct")
        except FileNotFoundError:
            print("File not found: '{}', maybe you forgot or mistyped the suffix".format(file))
