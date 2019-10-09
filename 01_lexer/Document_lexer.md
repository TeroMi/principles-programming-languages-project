# Lexer text document

#### **1.**
* Lexical analysis is detecting tokens from input like code file. It will generate legal tokens that are allowed in the syntax.
  
  Helps the work load of semantic analysis, when it has already checked if the tokens are valid programming language.

#### **2.**
* Token types need to be specified, regular expression rules for each token and a function for more complex token handling.
  
  The regex patterns and token list specifies the valid tokens and thus create the structure and the rules for the language.
#### **3.**
* **a)** All reserved keywords are in a dictionary and then recognized by defined function with regular expressions for each keyword.
       The function will also set the token type to recognized keyword.
    
* **b)** Comment block is recognized with starting and ending brace brackets {}. 
       Everything between will be ignored and if comment is multiline lexer line number will be fixed accordingly. 
       Lexer doesn't support nested comments
   
* **c)** Whitespaces are ignored by the lexer, by specifying them in t_ignore.
    
* **d)** Each possible operator and delimiter are in tokens list, followed by the regular expressions pattern.
       With regexp patterns the PLY lexer can recognize them from the input. For example r'<-' finds the left arrow token
    
* **e)** Has function matching the token list entry and recognizes numbers from 0 to 9 once or more times. 
       If input has zeroes in front, for example 03, it will be recognized separately as 0 and 3 number literals.
       
* **f)** Matching token list entry function will find anything that's between quotes. For example "String" will be recognized as string literal
       Error occurs if the literal finds the closing quote
          
* **g)** Regular expression pattern in the token function will find words starting with captital letter following with lowcase letters, but only lowcase letters.
       
* **h)** Tuples are recognized kind of the same way as string literals, but the regular expression requires that it has atleast one lowcase letter inside the angle brackets. 
       
#### **4.**
* **a)** Constant name regular expression has all captital letter and while functions start with capital letter, they require atleast one lowcase letter. 
    
* **b)** Regular expressions specified for each keyword will try to find word exactly like the keyword, otherwise if there is even one letter difference it will be a variable name.
    
* **c)** Regex used to recognized the right arrow is run first, so it will be recognized before the minus sign. 
    
* **d)** Functions are recognized as words which start with captial letter and variables are words that start with lowcase letter.
    
* **e)** Comment expression will find starting bracket and ending bracket, then it will ignore anything inside of it. 
    
* **f)** Tuples require atleast one lowcase letter between two angle brackets, so they won't mix.
#### **5.**
* Implemented  comment that spans multiple lines and corrects the line number to lexer toxens.
* Implemented few error messages: showing the illegal token in context, error message if file is not found, handling of other lexer type errors.
#### **6.**
* Very fun exercise, not too hard. Regular expressions were hardest part to get right. Learnt the recognise process of the lexical analysis and quite alot about regex.

