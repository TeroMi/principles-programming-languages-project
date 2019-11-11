# Syntax checker text document

#### **1.**
* Syntax analysis is used for recognising allowed syntax of the language and how the parsed tokens relate to each other
  
  Syntax analysis is the base for creating the parse tree, because it describes all the variables, operators and expressions.

#### **2.**
* Syntax is expressed in BNF rules, which tell all the possible variations of the expression, operation or parts of them.
  * For example 'atom' can be either function_call, NUMBER_LITERAL, variable identifier and so on.
  
  Code needs functions defined for each non-terminal names and in these functions you specify all the variations of the specific non-terminal.
  
#### **3.**
* **a)** 
     
     Variable definition can be normal variable, constant variable or tuple variable.
       
     Each variable definition begins with the variable identifier, and it is followed with an arrow operator. 
     The arrow operator specifies that the next token is going to be assigned to variable defined before the arrow.
     
    
* **b)**  
     
     Function call is describing how the functions can be called.
     
     It starts with function identifier, the function that you want to call, and contains square brackets after the identifier to specify any arguments needed in the function during its execution.
     Arguments are not necessary if function doesn't use them.
       
   
* **c)** 
    
    Tuple expression is telling how the tuple can be expressed. It may contain one or more tuple atoms separated by tuple operation (++).
    
       
#### **4.**
* **a)** 
 
    It is not, because you can only define variables inside functions.   
* **b)** 
    
    Yes, simple_expression rule states that two or more terms can be either added or subtracted with each other, 
    and terms can be strings.
* **c)**  
    
    Yes, variable_definition allows the value to be simple_expression, which can be constIDENT atom.
* **d)** 
    
    No, constant_definition only allows NUMBER_LITERAL or constIDENT as its value.
* **e)**  
    
    Yes, unary minus operator allows atoms to be negative for example --xx is doing double unary operator.
    And xx--yy is subtracting -yy from xx.
* **f)** 

    By defining them in the precedence rules
#### **5.**
* Didn't implement functions.

#### **6.**
* Quite fun exercise, harder than the previous one for sure. Was quite confused sometimes because the debug was bit cumbersome at times.
* EBNF -> BNF conversion was harder than I thought, but once I understood it made sense how it works.
* Would've wanted to implement functions, but due to my personal schedules couldn't get them to work on time. Might still implement them for fun.
 

