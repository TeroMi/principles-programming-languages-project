# Syntax checker text document

#### **1.**
* Syntax tree is a tool for creating the structure of the program. Symbol table will be created with assistance of the tree.

#### **2.**
* Tokens and BNF rules from previous phases are needed to actually recognize the patterns. 
Then according to BNF rules you need to create nodes that hold necessary values to create a tree.
  
#### **3.**
* **a)** 
     Parent node is type of the variable (variable, constant, tuple) accompanied with name of the variable. 
     Child nodes depend of the expression. If expression is another variable, then node will be that variable defintion.
     Expression can be operation as well or just any literal value, except for constant which accept numbers and other constants.
     
    
* **b)**  
     Parent node is pipe definition accompanied with name of the tuple. 
     Then the child nodes are pipe operation and expression which can be tuple or a tuple expression.
     
       
   
* **c)** 
    Parent node is function call with name of the function and child nodes are the arguments it takes. 
    
    
       
#### **4.**
* **a)** 
 Function call or function definition.
       
* **b)** 
    Don't know really, guess not. 
    Arguments, function calls/definitions are only place I used list of child nodes and I did them that way right away.
    

#### **5.**
* Implemented function call/definition in this phase. Did them out of curiosity and had more time during this phase than the previous.

#### **6.**
* Enjoyed this one a lot as well. First to actually picture the tree was hard. 
Eventually I realized I was thinking too much and simplified the tree alot after getting the idea.
Great thing for this is that there is many ways to implement the tree. I am not so sure about my implementation of each_statement but will modify it during the next phase.

