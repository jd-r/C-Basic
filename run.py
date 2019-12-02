from syntax import parser, quadruples, variables, printq

print("C Basic v0.0.0")
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

def parseop(var):
    optype = type(var)
    if optype == str:
        element = variables.get(var)
        if element is not None:
            return element[1]
        else:
            # var is not a defined variable
            if var[0] == '_': 
                # if it is a temp
                return temps[int(var[2])]
            elif var[0] == '"':
                return var[1:-1]
            else: 
                # it wasnt defined
                print("Error: '", var, "' is not defined", sep='')
                exit()
    elif optype == tuple: 
        return get_element_of_array(var)
    else:
        return var


def saveres(res, var):
    optype = type(var)
    if optype == tuple:
        save_to_array(res, var)
    else: 
        element = variables.get(var)
        if element is not None:
            if element[0] == 'int':
                element[1] = int(res)
            else:
                element[1] = float(res) 
        else:
            # var is not a defined variable
            if var[0] == '_': 
                # if it is a temp
                temps[int(var[2])] = res
            else: 
                # it wasnt defined
                print("Error: '", var, "' is not defined", sep='')
                exit() 

def is_number(n):
    try:
        # Type-casting the string to `float`.
        # If string is not a valid `float`, 
        # it'll raise `ValueError` exception
        float(n)    
    except ValueError:
        return False
    return True

def save_to_array(res, var):
    element = variables.get(var[0])
    if element is not None:
        params = []
        for i in var[1]:
            params.append(parseop(i))
        params = tuple(params)
        if element[0] == 'float':
            element[1][params] = float(res) 
        else:
            element[1][params] = int(res) 
    else:
        # it wasnt defined
        print("Error: '", var[0], "' is not defined", sep='')
        exit() 

def get_element_of_array(var):
    element = variables.get(var[0])
    if element is not None:
        params = []
        for i in var[1]:
            params.append(parseop(i))
        params = tuple(params)
        return element[1][params]  
    else:
        # it wasnt defined
        print("Error: '", var[0], "' is not defined", sep='')
        exit() 
       

temps = [None]*20
n = len(quadruples)
pc = 0
execution_stack = []

while pc < n:
    q = quadruples[pc]
    opcode = q[1]
    if opcode == '+':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 + op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '-':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 - op2
        saveres(res, q[4])
        pc += 1
    elif opcode == 'or':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 or op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '%':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 % op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '*':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 * op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '**':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 ** op2
        saveres(res, q[4])
        pc += 1
    elif opcode == 'and':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 and op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '/':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 / op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '>':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 > op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '<':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 < op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '>=':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 >= op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '<=':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 <= op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '==':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 == op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '!=':
        op1 = parseop(q[2])
        op2 = parseop(q[3])
        res = op1 != op2
        saveres(res, q[4])
        pc += 1
    elif opcode == '=':
        op1 = parseop(q[2])
        saveres(op1, q[3])
        pc += 1
    elif opcode == 'print':
        for i in q[2]:
            print(parseop(i), end=' ') 
        print()
        pc += 1
    elif opcode == 'prints':
        for i in q[2]:
            print(parseop(i), end=' ')
        print(" ", end='') 
        pc += 1
    elif opcode == 'input':
        for i in q[2]:
            t = input()
            if (is_number(t)):
                op = t
            else: 
                op = parseop(t)
            saveres(op, i)
        pc += 1
    elif opcode == 'goto':
        pc = q[2]
    elif opcode == 'gotoF':
        if not parseop(q[2]):
            # if false.. goto..
            pc = q[3]
        else:
            pc += 1
    elif opcode == 'gotoP':
        execution_stack.append(pc + 1)
        pc = q[2]
    elif opcode == 'returnP':
        pc = execution_stack.pop()
    elif opcode == 'return':
        pc = execution_stack[-1]
    elif opcode == 'gotoV':
        if parseop(q[2]):
            # if true.. goto..
            pc = q[3]
        else:
            pc += 1
    else: 
        break

