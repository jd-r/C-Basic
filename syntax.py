from lexer import tokens
import ply.yacc as yacc
import numpy as np

variables = {}
functions = {}
operands = []
jumps = []

temps = ['_T19', '_T18', '_T17', '_T16', '_T15', '_T14', '_T13', '_T12, ''_T11', '_T10', '_T9', '_T8', '_T7', '_T6', '_T5', '_T4', '_T3', '_T2', '_T1', '_T0']
orig_temps = ['_T19', '_T18', '_T17', '_T16', '_T15', '_T14', '_T13', '_T12, ''_T11', '_T10', '_T9', '_T8', '_T7', '_T6', '_T5', '_T4', '_T3', '_T2', '_T1', '_T0']

counter = 0

quadruples = []

# List of accepted syntax
def p_main(p):
    '''main : block main
            | block'''


# Main Block
def p_block(p):
    '''block : declaration
             | function
             | assignment
             | callfunction
             | expressions
             | if
             | while
             | dowhile
             | for
             | print
             | input
             | printq
             | prints
             | return '''


# Declare variables
def p_declaration(p):
    '''declaration : type ids
                   | type arrays'''

recenttype = ""
# Declare a single value
def p_type(p):
    '''type : INT
            | FLOAT'''
    global recenttype
    recenttype = p[1]

def p_ids(p):
    '''ids : sorm COMMA ids
           | sorm'''
def p_sorm(p):
    '''sorm : moreids
            | subdeclare'''
def p_moreids(p):
    '''moreids : ID'''
    variables[p[1]] = [recenttype, None]
def p_subdeclare(p):
    '''subdeclare : assignment'''
    global counter
    i = quadruples[counter - 1][-1]
    variables[i] = [recenttype, None]


def p_arrays(p):
    '''arrays : arrayorsub COMMA arrays
              | arrayorsub'''
def p_arrayorsub(p):
    '''arrayorsub : array 
                  | subdeclarem'''
# Declare arrays
def p_array(p):
    '''array : ID args'''
    global cnt, recenttype
    vals = []
    for i in range(cnt):
        vals.append(operands.pop())
    vals.reverse()
    variables[p[1]] = [recenttype, np.zeros(vals)]
    cnt = 0

cnt = 0
def p_args(p):
    '''args : LSQUARED expression RSQUARED args
            | LSQUARED expression RSQUARED'''
    global cnt
    cnt += 1

def p_subdeclarem(p):
    '''subdeclarem : ID args EQUALS arrvalue'''
    global cnt, recenttype, values
    vals = 1
    vals_l = []
    b_l = []
    for i in range(values):
        vals_l.append(operands.pop())
    for i in range(cnt):
        element = operands.pop()
        vals *= element
        b_l.append(element)
    if values != vals:
        print("Error: the number values to assign don't match declaration")
        return
        # exit()
    
    b_l.reverse()    
    vals_l.reverse()
    array = np.array(vals_l).reshape(b_l)
    variables[p[1]] = [recenttype, array]
    values = 0
    cnt = 0

def p_arrvalue(p):
    'arrvalue : LCURLY value RCURLY'
values = 0
def p_value(p):
    '''value : numberorid COMMA value
             | numberorid'''
    global values
    values += 1


# Functions
def p_function(p):
    'function : functionaux LCURLY main RCURLY'
    global counter
    q = [counter, "returnP"]
    quadruples.append(q)
    counter += 1
    dir1 = jumps.pop()
    quadruples[dir1][-1] = counter

def p_return(p):
    'return : RETURN'
    global counter
    q = [counter, "return"]
    quadruples.append(q)
    counter += 1

def p_functionaux(p):
    'functionaux : FUNCTION ID PARENS'
    global counter
    jumps.append(counter)
    q = [counter, "goto", None]
    quadruples.append(q)
    counter += 1
    functions[p[2]] = counter


# Assignment
def p_assignment(p):
    '''assignment : normalassignment 
                  | plusplus
                  | minusminus'''


def p_normalassignment(p):
    'normalassignment : idorarrayid EQUALS expression'
    global counter
    op1 = operands.pop()
    q = [counter, "=", op1, p[1]]
    quadruples.append(q)
    if op1 in orig_temps:
        temps.append(op1)
    counter += 1

def p_idorarrayid(p):
    '''idorarrayid : ID
                   | arrayid'''
    p[0] = p[1]

def p_plusplus(p):
    'plusplus : ID PLUSPLUS'
    global counter
    q = [counter, "+", p[1], 1, p[1]]
    quadruples.append(q)
    counter += 1


def p_minusminus(p):
    'minusminus : ID MINUSMINUS'
    global counter
    q = [counter, "-", p[1], 1, p[1]]
    quadruples.append(q)
    counter += 1


# Call function
def p_callfunction(p):
    'callfunction : ID PARENS'
    global counter
    q = [counter, "gotoP", functions[p[1]]]
    quadruples.append(q)  
    counter += 1

# Expressions
def p_expression_plus(p):
    'expression : expression PLUS term'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "+", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp) 
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_expression_minus(p):
    'expression : expression MINUS term'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "-", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1


def p_expression_or(p):
    'expression : expression OR term'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "or", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_expression_term(p):
    'expression : term'

# Terms of expressions

def p_term_power(p):
    'term : term POWER factor'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "**", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_term_times(p):
    'term : term TIMES factor'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "*", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_term_div(p):
    'term : term DIVIDE factor'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "/", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_term_mod(p):
    'term : term MOD factor'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "%", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_term_eq(p):
    'term : term AND factor'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "and", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_term_factor(p):
    'term : factor'

# Factors of expressions
def p_factor_numorid(p):
    'factor : numberorid'

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'

def p_factor_greater(p):
    'factor : numberorid GREATER numberorid'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, ">", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_factor_less(p):
    'factor : numberorid LESS numberorid'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "<", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_factor_greatere(p):
    'factor : numberorid GREATEREQ numberorid'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, ">=", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_factor_lesse(p):
    'factor : numberorid LESSEQ numberorid'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "<=", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_factor_equale(p):
    'factor : numberorid EQUALEQ numberorid'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "==", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_factor_not(p):
    'factor : numberorid NOTEQ numberorid'
    global counter
    op2 = operands.pop()
    op1 = operands.pop()
    temp = temps.pop()
    q = [counter, "!=", op1, op2, temp]
    quadruples.append(q)
    operands.append(temp)
    if op1 in orig_temps:
        temps.append(op1)
    if op2 in orig_temps:
        temps.append(op2)
    counter += 1

def p_numberorid(p):
    '''numberorid : NUMBER 
                  | ID
                  | arrayid'''
    operands.append(p[1])

def p_arrayid(p):
    'arrayid : ID args'
    global cnt
    array = []
    for i in range(cnt):
        array.append(operands.pop())
    array.reverse()
    new_array = (p[1], tuple(array))
    cnt = 0
    p[0] = new_array
    

# if
def p_if(p):
    'if : IF LPAREN expression RPAREN if_aux1 LCURLY main RCURLY else'
    # Action 3
    global counter
    dir2 = jumps.pop()
    quadruples[dir2][-1] = counter 


def p_else(p):
    '''else : ELSE if_aux2 LCURLY main RCURLY
            | ELSE if_aux2 block
            | empty'''

def p_if_aux1(p):
    'if_aux1 : empty'
    # Action 1
    global counter
    re = operands.pop()
    q = [counter, "gotoF", re, None]
    quadruples.append(q)
    jumps.append(counter)
    counter += 1

def p_if_aux2(p):
    'if_aux2 : empty'
    # Action 2
    global counter
    dir1 = jumps.pop()
    q = [counter, "goto", None]
    quadruples.append(q)
    jumps.append(counter)
    counter += 1
    quadruples[dir1][-1] = counter


# while
def p_while(p):
    'while : WHILE while_aux1 LPAREN expression RPAREN while_aux2 LCURLY main RCURLY'
    # Action 3
    global counter
    dir1 = jumps.pop()
    dir2 = jumps.pop()
    q = [counter, "goto", dir2]
    quadruples.append(q)
    counter += 1
    quadruples[dir1][-1] = counter



def p_while_aux1(p):
    'while_aux1 : empty'
    # Action 1
    jumps.append(counter)

def p_while_aux2(p):
    'while_aux2 : empty'
    # Action 2
    global counter
    t = operands.pop()
    q = [counter, "gotoF", t, None]
    quadruples.append(q)
    jumps.append(counter)
    counter += 1



# do while
def p_dowhile(p):
    'dowhile : DO do_aux LCURLY main RCURLY WHILE LPAREN expression RPAREN SEMIC'
    # Action 2
    global counter
    t = operands.pop()
    dir = jumps.pop()
    q = [counter, "gotoV", t, dir]
    quadruples.append(q)
    counter += 1

def p_do_aux(p):
    'do_aux : empty'
    # Action 1
    jumps.append(counter)


# for
def p_for(p):
    'for : FOR LPAREN assignordeclare SEMIC expression SEMIC foraux1 assignment foraux2 RPAREN LCURLY main RCURLY'
    global counter
    dir2 = jumps.pop()
    dir1 = jumps.pop()
    q = [counter, "goto", dir1 + 1]
    quadruples.append(q)
    counter += 1
    quadruples[dir1 - 1][-1] = counter

    quadruples[dir2][-1] = dir1 - 2

def p_assignordeclare(p):
    '''assignordeclare : assignment
                       | declaration'''

def p_foraux1(p):
    'foraux1 : empty'
    global counter
    t = operands.pop()
    q = [counter, "gotoF", t, None]
    quadruples.append(q)
    counter += 1

    q = [counter, "goto", None]
    quadruples.append(q)
    jumps.append(counter)
    counter += 1

def p_foraux2(p):
    'foraux2 : empty'
    global counter
    dir1 = jumps[-1]

    q = [counter, "goto", None]
    quadruples.append(q)
    jumps.append(counter)
    counter += 1

    quadruples[dir1][-1] = counter


# print
def p_print(p):
    'print : PRINT printaux LPAREN expressions RPAREN'
    global counter, printcnt
    printvars = []
    for i in range(printcnt):
        printvars.append(operands.pop())
    printvars.reverse()
    q = [counter, "print", printvars]
    quadruples.append(q)
    counter += 1
    printcnt = 0

# print
def p_prints(p):
    'prints : PRINTS printaux LPAREN expressions RPAREN'
    global counter, printcnt
    printvars = []
    for i in range(printcnt):
        printvars.append(operands.pop())
    printvars.reverse()
    q = [counter, "prints", printvars]
    quadruples.append(q)
    counter += 1
    printcnt = 0

def p_printaux(p):
    'printaux : empty'
    global counter
    p[0] = counter

def p_expressions(p):
    '''expressions : stringorexpression COMMA expressions
                   | stringorexpression''' 

printcnt = 0
def p_stringorexpression(p):
    '''stringorexpression : string
                          | expression'''
    global printcnt
    printcnt += 1

def p_string(p):
    'string : STRING'
    operands.append(p[1])

def p_input(p):
    'input : INPUT LPAREN input_ids RPAREN'
    global counter, inputcnt
    inputvars = []
    for i in range(inputcnt):
        inputvars.append(operands.pop())
    inputvars.reverse()
    q = [counter, "input", inputvars]
    quadruples.append(q)
    counter += 1
    inputcnt = 0


inputcnt = 0
def p_input_ids(p):
    '''input_ids : numberorid COMMA input_ids
                 | numberorid'''
    global inputcnt
    inputcnt += 1

# inputvars = []
# def p_idorarray(p):
#     '''idorarray : ID
#                  | ID args'''
#     global cnt
#     if cnt != 0:
#         vals = []
#         for i in range(cnt):
#             vals.append(operands.pop())
#         inputvars.append((p[1], vals))
#     else: 
#         inputvars.append(p[1])


# Useful functions
# Epsilon
def p_empty(p):
    'empty :'
    pass


def p_printq(p):
    'printq : PRINTQ PARENS'
    for quad in quadruples:
        for q in quad:
            print(q, end=' ')
        print()

def printq():
    for quad in quadruples:
        for q in quad:
            print(q, end=' ')
        print()


# Error rule for syntax errors
def p_error(p):
    print("SyntaxError: invalid syntax")
    exit()


# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    print("C Basic v0.0.0")
    # while True:
    #     try:
    #         s = input('>> ')
    #     except EOFError:
    #         break
    #     if not s: 
    #         continue
    #     parser.parse(s)

    data = """  //for(int i=0; i<j+1; i++) { 
                //    print("caca") 
                //} 
                i < 3 + 1"""
    parser.parse(data)
    printq()
