"""C Basic is a small programming language that makes it easy for beginners to learn to code.

It is a high-level, interpreted, statically-typed programming language designed for a compilers course at Tecnologico de Monterrey. It is written completely in Python3 using PLY. The language syntax is meant to be very readable and intuitive.

It supports various fundamental programming concepts such as variable-declaration, function calling, conditional statements, loops, proper order of operations, and recursion. But it also supports more complex things like multidimensional arrays; expressions inside array parameters: arr1[2+var1][2][2]; exponentiation(x**y); and modules(%).

How to run a program? 
In the examples folder are some programs that the language can run. 
Press the "Run" button above and enter the name of the file you'd like to run. You can also write your own program and save it inside examples/ without any file type.

"""

from syntax import parser, printq
from run import run

__author__ = "Jorge Diego Rodriguez"
__version__ = "0.0.0"

print("C Basic v", __version__, sep='')
print("=======================================")
print("Introduce the name of the file to compile:")
print("Examples:")
print("add_matrixes")
print("sort")
print("check_for_prime")
print("...")

file = "examples/" + input()
with open(file) as f:
    mystr = f.read()

parser.parse(mystr)

## Uncomment to print quadruples
# printq()

run()