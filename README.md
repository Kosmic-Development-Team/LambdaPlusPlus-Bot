# λ++ Bot
Create and evaluate λ-Calculus and more in Discord!

## λ-Calculus

## BrainFuck
### Symbols
Classic  
\> increment pointer  
<  decrement pointer  
\+  increment register  
\-  decrement register  
\[  start loop  
\]  end loop  
,  take input  
\.  print  

New  
%  set pointer  

Meta  
$  Take input (not applicable with classic input mode, clears buffer before asking again on buffer mode)  
&  Toggle between character input and hex input  
\!  Flush output  

### Features
 - Has classic, deffered, and buffer input modes  
 - Deffered input waits until an input register is edited, a take input command is issued, or the program ends to ask for all the character inputs at one time  
 - Buffered input asks for input at the begining of the beginning (any length) and uses it as needed throughout the program, asking again if the buffer runs out  
 - Has 256 8 bit or 65536 16 bit register modes  
 - 16 bit mode supports UTF-8 (converting UTF-8 characters into a 16 bit value)  
 - Submitting an input of a length less than the length required (differed input only) will fill the rest with null  

