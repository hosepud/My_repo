
This is a compiler for a functional language that uses LISP syntax.
The compiler is written in python. Compiles the code to C and then gcc compiles that to a binary.

Main differences from a regular Scheme:
Unlike Scheme a 'lambda' is represented as @ and functions can only have 1 argument so the programmer needs to use currying (for a maximum of 7 curried arguments per function).
So (define z (lambda (x) (+ x 1))) becomes (define z (@ x (+ x 1)))
Notice + has more than one argument, but internally (+ x) returns a closure over x.

Functions that 'appear' to have more than one argument and can be used with the below syntax for simplicity.
(map function lst)
(filter function lst) 
(reduce function initial lst)
(+ n1 n2 n3 ..... n7)
(- n1 n2 n3 .... n7)
(* n1 n2 n3 .... n7)
(if predicate consequent antescedent)
(list-ref lst index)

Strings come in the form """my string hehe, here's a newline char - \n""".
Internally represented as singly linked lists (nil terminated)

It has IO:
(input) - asks for user input, terminate with ctrl D
	For example (define mystring (input)) will bind a string to mystring variable
(print """Hello World\n""") - prints hello world
(write filename string) - writes the string to filename, creates filename if needed
(append filename string) - appends instead
(read filename) - returns a string with the contents of filename
	For example (define mystring (read filename))


Numbers are 32 bit signed ints. Initially only the numbers from 0 to 127 are defined.
to use let's say 1010 you need 
(define 1012 (+ 2 (* 101 10)))
It has closures, but it doesn't have internal definitions

A couple example programs are included.

TO INSTALL AND USE COMPILER:
Have gcc.
Download Compiler folder contents.
Download GC in Compiler folder. GC is downloaded from https://github.com/ivmai/bdwgc/.
Follow their installation instructions. A gc.a must exist in bdwgc. bdwgc must be in Compiler folder.
To compile a .lc program (.lc is needed) do python3 lccompiler.py myprogram.lc.
To run do ./myprogram.


