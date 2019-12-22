from semantics_common import SymbolData, SemData


def run_program(tree, semdata):
    eval_node(tree, semdata)


def eval_node(node, semdata):
    if node.nodetype == "program":
        semdata.return_value_var = None
        semdata.return_value = None
        for node in node.children_statements:
            eval_node(node, semdata)
        #printing the return value
        if semdata.return_value_var is not None:
            print(semdata.symtbl[semdata.return_value_var]["value"])
        else:
            print(semdata.return_value)

    if node.nodetype == "var_definition":
        var_value = ""
        if hasattr(node.child_expression, "child_term1") and hasattr(node.child_expression, "child_term2"):
            term1 = node.child_expression.child_term1
            term2 = node.child_expression.child_term2
            if not hasattr(term1, "child_term1") and not hasattr(term1, "child_term2") \
                    and not hasattr(term2, "child_term1") and not hasattr(term2, "child_term2"):
                if node.child_expression.nodetype == "mult_operation":
                    var_value = term1.value * term2.value
                elif node.child_expression.nodetype == "div_operation":
                    var_value = term1.value / term2.value
                elif node.child_expression.nodetype == "minus_expression":
                    var_value = term1.value - term2.value
                elif node.child_expression.nodetype == "plus_expression":
                    var_value = term1.value + term2.value
        else:
            var_value = node.child_expression.value
        semdata.symtbl[node.value]["value"] = var_value

    if node.nodetype == "const_definition":
        if hasattr(node.child_expression, "value"):
            semdata.return_value = node.child_expression.value

    if node.nodetype == "return_value":
        if node.child_expression.nodetype == "varIDENT":
            semdata.return_value_var = node.child_expression.value
        else:
            semdata.return_value = node.child_expression.value




