# C-Basic
C Basic is a small programming language with a readable and intuitive syntax that makes it easy for beginners to learn to code.

It is a high-level, interpreted and statically-typed language written in Python3 with [PLY](https://www.dabeaz.com/ply/). It was designed for a compilers course at Tecnologico de Monterrey. 

It supports various fundamental programming concepts such as variable-declaration, function calling, conditional statements, loops, proper order of operations, and recursion. But it also supports more complex things like multidimensional arrays; expressions inside array parameters: `arr1[2+var1][2][2]` eexponentiatio `x**y` and modules `x%11`

## Demo
The code can be found in [repl.it](https://repl.it/@j_diegodiego/C-Basic), where you click the "Run" button and then enter the name of a program to compile and run it.

## Syntax

### Variable declaration
```c
int var1, var2 = 0 
int var3[5]
float var4[2][2][2] = {1,2,3,4,5,6,7,8}

var3[2] = 2+2*(var2-4)
```

### Functions
```c
function add() {
  // Do something
}

add()
```

### Comments
```c
// Single line Comment

/*
  Multiline Comment
*/
```

### Input/Output
```c
input(var1, var1, var3[2])

print("Hello, World", var1, 2*2)
```

### Loops
```c
for(int i = 0; i < 3; i++) {
  // For loop
}

while(i==0) {
  // While
}

do {
  // Do while
} while(i==0)
```

### Conditional Statements
```c
if(a == 1) {
  // if
} else if (a == 2) {
  // else if
} else {
  // else
}
```

## Examples
Examples can be found in the `examples` 
