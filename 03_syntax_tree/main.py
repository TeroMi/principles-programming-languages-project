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
    '''function_or_variable_definition : variable_definitions
                                       | function_definition'''
    p[0] = p[1]


# Function stuff for later
def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
                             BEGIN \
                             function_variable_definitions \
                             return_value DOT \
                             END DOT'''
    p[0] = ASTnode("function_definition")
    p[0].value = p[2]
    p[0].children_formals = p[4].children_formals


def p_function_variable_definitions(p):
    '''function_variable_definitions : variable_definitions
                                     | function_variable_definitions variable_definitions
                                     | '''
    p[0] = p[1]


def p_formals_var(p):
    '''formals : varIDENT'''
    p[0] = ASTnode("formals")
    temp_var = ASTnode("varIDENT")
    temp_var.value = p[1]
    p[0].children_formals = [temp_var]

def p_formals_vars(p):
    '''formals : formals COMMA varIDENT'''
    p[0] = p[1]
    temp_var = ASTnode("varIDENT")
    temp_var.value = p[3]
    p[0].children_formals.append(temp_var)


def p_formals_empty(p):
    '''formals : '''
    p[0] = ASTnode("formals")
    p[0].children_formals = []


def p_return_value_eq(p):
    '''return_value : EQ simple_expression'''
    p[0] = ASTnode("return_value")
    p[0].child_expression = p[2]


def p_return_value_noteq(p):
    '''return_value : NOTEQ pipe_expression'''
    p[0] = ASTnode("return_value")
    p[0].child_operator = ASTnode(p[1])
    p[0].child_expression = p[2]
    p[0].child_expression.children_terms = []


def p_variable_definitions_var(p):
    '''variable_definitions : varIDENT LARROW simple_expression DOT'''
    p[0] = ASTnode("variable definition")
    p[0].value = p[1]
    p[0].child_expression = p[3]


def p_variable_definitions_constant(p):
    '''variable_definitions : constIDENT LARROW constant_expression DOT'''
    p[0] = ASTnode("constant definition")
    p[0].value = p[1]
    p[0].child_expression = p[3]
    print("const {}".format(p[1]))


def p_variable_definitions_tuple(p):
    '''variable_definitions : tupleIDENT LARROW tuple_expression DOT'''
    p[0] = ASTnode("tuple_definition")
    p[0].value = p[1]
    p[0].child_expression = p[3]
    print("tuple")


def p_variable_definitions_tuple_pipe(p):
    '''variable_definitions : pipe_expression RARROW tupleIDENT DOT'''
    p[0] = ASTnode("tuple pipe definition")
    p[0].value = p[3]
    p[0].child_pipe_expression = p[1]


def p_constant_expression(p):
    '''constant_expression : constIDENT
                           | NUMBER_LITERAL'''
    p[0] = ASTnode(p.slice[1].type)
    p[0].value = p[1]


def p_pipe_expression_tuple(p):
    '''pipe_expression : tuple_expression'''
    p[0] = p[1]


def p_pipe_expression(p):
    '''pipe_expression : pipe_expression PIPE pipe_operation'''
    p[0] = p[3]
    p[0].child_expression = p[1]


def p_pipe_operation(p):
    '''pipe_operation : funcIDENT
                      | MULT
                      | PLUS'''
    p[0] = ASTnode(p.slice[1].type)
    p[0].value = p[1]


def p_pipe_operation_each(p):
    '''pipe_operation : each_statement'''
    p[0] = p[1]


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''
    p[0] = ASTnode("each_statement")
    p[0].child_from = ASTnode(p[3])


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom'''
    p[0] = p[1]


def p_tuple_expression2(p):
    '''tuple_expression : tuple_expression tuple_operation tuple_atom'''
    p[0] = ASTnode("tuple operation")
    p[0].value = p[2]
    p[0].child_atom1 = p[1]
    p[0].child_atom2 = p[3]


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    p[0] = p[1]


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT'''
    p[0] = ASTnode("tuple identifier")
    p[0].value = p[1]


def p_tuple_atom_arguments(p):
    '''tuple_atom : LSQUARE arguments RSQUARE'''
    p[0] = p[2]


def p_tuple_atom_function_call(p):
    '''tuple_atom : function_call'''
    p[0] = p[1]


def p_tuple_atom_range(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                  | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE'''
    p[0] = ASTnode("tuple range expression")
    p[0].child_start = p[2]
    p[0].child_end = p[4]


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE RSQUARE'''
    p[0] = ASTnode("function_call")
    p[0].value = p[1]
    p[0].children_arguments = []


def p_function_call_arguments(p):
    '''function_call : funcIDENT LSQUARE arguments RSQUARE'''
    p[0] = ASTnode("function_call")
    p[0].value = p[1]
    p[0].children_arguments = p[3].children_argument


def p_arguments(p):
    '''arguments : simple_expression'''
    p[0] = ASTnode("arguments")
    p[0].children_argument = [p[1]]


def p_arguments2(p):
    '''arguments : arguments COMMA simple_expression'''
    p[0] = p[1]
    p[0].children_argument.append(p[3])


def p_atom(p):
    '''atom : NUMBER_LITERAL
            | STRING_LITERAL
            | varIDENT
            | constIDENT
            | function_call'''
    p[0] = ASTnode(p.slice[1].type)
    p[0].value = p[1]


def p_atom_select(p):
    '''atom : SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    p[0] = ASTnode("select")
    p[0].child_const_exp = p[3]
    p[0].child_tuple = p[5]


def p_atom_parentheses(p):
    '''atom : LPAREN simple_expression RPAREN'''
    p[0] = p[2]


def p_unary_operator(p):
    '''unary_operator : MINUS'''


def p_factor(p):
    '''factor : atom'''
    p[0] = p[1]


def p_factor_minus(p):
    '''factor : unary_operator atom %prec UMINUS'''
    p[0] = p[2]
    p[0].value = -p[2].value


def p_term(p):
    '''term : factor'''
    p[0] = p[1]


def p_term_mult(p):
    '''term : term MULT factor'''
    p[0] = ASTnode("multiplication operation")
    p[0].child_term1 = p[1]
    p[0].child_term2 = p[3]


def p_term_div(p):
    '''term : term DIV factor'''
    p[0] = ASTnode("division operation")
    p[0].child_numerator = p[1]
    p[0].child_denominator = p[3]


def p_simple_expression_term(p):
    '''simple_expression : term'''
    p[0] = p[1]


def p_simple_expression_minus(p):
    '''simple_expression : simple_expression MINUS term'''
    p[0] = ASTnode("minus_expression")
    p[0].child_term1 = p[1]
    p[0].child_term2 = p[3]


def p_simple_expression_plus(p):
    '''simple_expression : simple_expression PLUS term'''
    p[0] = ASTnode("plus_expression")
    p[0].child_term1 = p[1]
    p[0].child_term2 = p[3]


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
