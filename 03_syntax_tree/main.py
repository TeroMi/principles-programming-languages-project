#!/usr/bin/env python3
import ply.yacc as yacc
import lexer
import tree_print
tokens = lexer.tokens

import ply.yacc as yacc

precedence = (
     ('left', 'PLUS', 'MINUS'),
     ('left', 'MULT', 'DIV'),
     ('right', 'UMINUS')
 )

class ASTnode:
    def __init__(self, typestr):
        self.nodetype = typestr

def p_program_return(p):
    '''program :  return_value DOT'''
    p[0] = ASTnode('program')
    p[0].children_statements = [p[1]]


def p_program_variables(p):
    '''program : function_or_variable_definition program'''
    p[0] = p[2]
    p[0].children_statements.append(p[1])


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definitions'''
    p[0] = p[1]


# Function stuff for later
# def p_function_definition(p):
#     '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
#                              BEGIN \
#                              return_value DOT \
#                              END DOT'''
#     print("func definition {}".format(p[2]))
#
#
# def p_formals(p):
#     '''formals : varIDENT formals
#                | COMMA varIDENT
#                | COMMA varIDENT formals
#                | varIDENT '''
#     print("formals")


def p_return_value_eq(p):
    '''return_value : EQ simple_expression'''
    p[0] = ASTnode("return_value")
    p[0].child_operator = ASTnode(p[1])
    p[0].child_expression = p[2]


def p_return_value_noteq(p):
    '''return_value : EQ pipe_expression'''
    p[0] = ASTnode("return_value")
    p[0].child_operator = ASTnode(p[1])
    p[0].child_expression = p[2]
    p[0].child_expression.children_terms = []


def p_variable_definitions_var(p):
    '''variable_definitions : varIDENT LARROW simple_expression DOT'''
    print("variable_definition( {} )".format(p[1]))
    p[0] = ASTnode("variable definition")
    p[0].value = p[1]
    p[0].child_definition = p[3]


def p_variable_definitions_constant(p):
    '''variable_definitions : constIDENT LARROW constant_expression DOT'''
    print("constant_definition( {} )".format(p[1]))
    p[0] = ASTnode("constant definition")
    p[0].value = p[1]
    p[0].child_constant_expression = p[3]


def p_variable_definitions_tuple(p):
    '''variable_definitions : tupleIDENT LARROW tuple_expression DOT'''
    print("tuple_definition( {} )".format(p[1]))


def p_variable_definitions_tuple_pipe(p):
    '''variable_definitions : pipe_expression RARROW tupleIDENT DOT'''
    print("tuple_definition ( {} )".format(p[3]))


def p_constant_expression(p):
    '''constant_expression : constIDENT
                           | NUMBER_LITERAL'''
    p[0] = ASTnode(p.slice[1].type)
    p[0].value = p[1]


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


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom'''

def p_tuple_expression2(p):
    '''tuple_expression : tuple_expression tuple_operation tuple_atom'''

def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT
                  | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                  | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
                  | LSQUARE arguments RSQUARE'''


# def p_function_call(p):
#     '''function_call : funcIDENT LSQUARE RSQUARE
#                      | '''


def p_arguments(p):
    '''arguments : simple_expression arguments
                 | COMMA simple_expression
                 | COMMA simple_expression arguments
                 | simple_expression'''
    #print("arguments")


def p_atom(p):
    '''atom : NUMBER_LITERAL
            | STRING_LITERAL
            | varIDENT
            | constIDENT
            | LPAREN simple_expression RPAREN
            | SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    # if len(p) == 4:
    #     print("atom")
    # else:
    #     print("atom( {} )".format(p[1]))
    #p[0] = p[1]
    p[0] = ASTnode(p.slice[1].type)
    p[0].value = p[1]
    #p[0].child_atom = p[0]


def p_unary_operator(p):
    '''unary_operator : MINUS'''


def p_factor(p):
    '''factor : atom'''
    #p[0] = p[1]
    p[0] = ASTnode("atom")
    p[0].value = p[1].value
    p[0].child_atom = p[1]


def p_factor_minus(p):
    '''factor : unary_operator atom %prec UMINUS'''
    p[0] = ASTnode("atom")
    p[0].value = -p[2].value


def p_term(p):
    '''term : factor'''
    #p[0] = p[1]
    p[0] = ASTnode("factor")
    p[0].value = p[1].value
    p[0].children_factor = [p[1]]


def p_term_mult(p):
    '''term : term MULT factor'''
    p[0] = p[1]#ASTnode("term")
    print("{} {} {}".format(p[1],p[3],p[3].value))
    p[0].value = p[1].value * p[3].value
    p[0].children_factor.append(p[3])
    #p[0].children_factor[1].child_operator = p[2]


def p_term_div(p):
    '''term : term DIV factor'''
    p[0] = p[1]#= ASTnode("term")
    print("{} {} {} {}".format(p[1].nodetype, p[1].value, p[3].nodetype, p[3].value))
    try:
        p[0].value = p[1].value / p[3].value
        #p[0].child_factor = p[1]
        p[0].children_factor.append(p[3])
        p[0].children_operator = p[2]
    except ZeroDivisionError:
        parser.errorfunc(p)
        #yacc.YaccProduction.parser
        print("ERROR: Division by zero")
        raise SystemExit


def p_simple_expression_term(p):
    '''simple_expression : term'''
    p[0] = ASTnode("simple_expression")
    p[0].value = p[1].value
    p[0].child_term = p[1]


def p_simple_expression_minus(p):
    '''simple_expression : simple_expression MINUS term'''
    print("{} {}".format(p[1].value, p[3].value))
    p[0] = p[1]#ASTnode("minus_expression")
    p[0].children_terms = []
    p[0].children_terms.append(p[1])
    p[0].children_terms.append(p[3])
    p[0].child_operator = ASTnode("MINUS")
    p[0].value = p[1].value - p[3].value


def p_simple_expression_plus(p):
    '''simple_expression : simple_expression PLUS term'''
    p[0] = ASTnode("plus_expression")
    p[0].children_terms = []
    p[0].children_terms.append(p[1])
    p[0].children_terms.append(p[3])
    p[0].child_operator = ASTnode("PLUS")
    p[0].value = p[1].value + p[3].value


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
        try:
            with codecs.open(file, 'r') as INFILE:
                data = INFILE.read()
                result = parser.parse(data, lexer=lexer.lexer, debug=False)
                tree_print.treeprint(result, "unicode")
        except FileNotFoundError:
            print("File not found: '{}', maybe you forgot or mistyped the suffix".format(file))
