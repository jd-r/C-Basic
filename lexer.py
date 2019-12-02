import ply.lex as lex

# resultado del analisis
result = []

reserved = {
    'if'      : 'IF',
    # 'then'    : 'THEN',
    'else'    : 'ELSE',
    'do'      : 'DO',
    'while'   : 'WHILE',
    'for'     : 'FOR',
    'int'     : 'INT',
    'float'   : 'FLOAT',
    'input'   : 'INPUT',
    'print'   : 'PRINT',
    'prints'   : 'PRINTS',
    'function': 'FUNCTION',
    'printq'  : 'PRINTQ',
    'return'  : 'RETURN',
    # 'true'    : 'TRUE',
    # 'false'   : 'FALSE'
}

# List of token names.
tokens = ['ID', 'EQUALS', 'COMMA', 'SEMIC',
          'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY', 'LSQUARED', 'RSQUARED', 'PARENS',
          'OR','AND','EQUALEQ', 'NOTEQ', 'GREATER', 'LESS', 'GREATEREQ', 'LESSEQ',
          'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
          'MOD', 'PLUSPLUS', 'MINUSMINUS',
          'STRING', 'POWER'
          ] + list(reserved.values())

# Regular expression rules for simple tokens
t_EQUALS  = r'='
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'\%'
t_POWER = r'(\*{2})'

t_OR      = r'\|\|'
t_AND     = r'\&\&'
t_EQUALEQ = r'=='
t_NOTEQ   = r'\!='
t_GREATER = r'>'
t_LESS    = r'<'
t_GREATEREQ = r'>='
t_LESSEQ   = r'<='

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LSQUARED = r'\['
t_RSQUARED = r'\]'
t_LCURLY  = r'{'
t_RCURLY  = r'}'
t_PARENS = r'\(\)'

t_COMMA   = r','
t_SEMIC   = ';'


# Regular expression rules

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
    

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_STRING(t):
    r'\"((?!\").)*\"'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    # t.lexer.lineno += 1
    pass

def t_comments(t):
    r'/\*(.|\n)*?\*/'
    pass

def t_comments_ONELine(t):
    r'//(.)*'
    pass
    

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s' " % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex(debug=0)

if __name__ == '__main__':
    data = """ // a b c
               // b d e
               c f     """

    lexer.input(data)

    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        result.append(tok.type)
    print(result)
