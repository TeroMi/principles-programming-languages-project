# Semantic check and running document

## Implemented semantic checks
   * Variables cannot be used if they are not defined or used before definition. 
        * This is achieved by simply keeping track of values of variables in symbol table and if variable has None value it will print error
        * Function parameters can be used inside function, they appear as Function variables in symbol table and appear as defined variables
     
## Implementation levels
   * Simple integer expressions are evaluated and program prints the return value.
        * Return value can be variable, constant or string
        * Note: Arithmetic operations(+, -, *, /) are usable only as single operations, for example 2+2 is evaluated, but due to hurry 2+2+2 etc. is not.
        * Evaluation is done by parsing the tree 

## Notes
   * From previous phase I have corrected below feedback:
     ```
     * Documentation mentions functions added now, regarding functions: Variable definitions and return value 
     inside function definition are not present in the tree. Also functions without variables crash the program.
     * In line such as result <- Simple_plus[3,5]. the function call expression prinst bit of hexacode as the value.
     Or could be a function call with expression as formals.
     ```

## Thoughts
   Assignment was fun, but I felt for the basic sin and started too late. Then I spent too much time on couple of issues. 
   
   Had trouble figuring out how to efficiently loop through nested arithmetic operations. I didn't have time to solve if it was my tree structure or else that was wrong, so I ended up implementing only single operations.
   
   Also the return value gave me some headache, basic return values were easy, but evaluating return value if it was a variable gave some trouble.
   
   What made this assignment tricky was the way of thinking that the tree is parsed starting from the bottom.
   
   Shame that I started so late I couldn't fix all my issues, great exercise nonetheless.