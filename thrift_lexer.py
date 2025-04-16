import ply.lex as lex

reserved = {
    'namespace': 'NAMESPACE',
    'struct': 'STRUCT',
    'service': 'SERVICE',
    'optional': 'OPTIONAL',
    'required': 'REQUIRED',
    'void': 'VOID',
    'include': 'INCLUDE',
    'byte': 'BYTE',
    'i8': 'I8',
    'i16': 'I16',
    'i32': 'I32',
    'i64': 'I64',
    'bool': 'BOOL',
    'double': 'DOUBLE',
    'string': 'STRING',
    'enum': 'ENUM',
    'const': 'CONST',
    'typedef': 'TYPEDEF',
    'list': 'LIST',
    'set': 'SET',
    'map': 'MAP',
    'oneway': 'ONEWAY',
}

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'COLON',
    'COMMA',
    'SEMICOLON',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'LT',
    'GT',
    'LBRACKET',
    'RBRACKET',
    'EQUALS',
    'STRING_LITERAL',
    'BOOL_VALUE',
    'FLOAT_VALUE',
] + list(reserved.values())

t_COLON = r':'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUALS = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_GT = r'>'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_ignore = ' \t'

def t_STRING_LITERAL(t):
    r'"([^\\"]|\\.)*"|\'([^\\\']|\\.)*\''
    t.value = t.value[1:-1]  # 去掉引号
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_\.]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_FLOAT_VALUE(t):
    r'[-+]?\d*\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'[-+]?\d+'
    t.value = int(t.value)
    return t

def t_BOOL_VALUE(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'(//.*)|(/\*(.|\n)*?\*/)|(\#.*)'
    pass

def t_error(t):
    print(f"非法字符 '{t.value[0]}' 在第 {t.lineno} 行")
    t.lexer.skip(1)

lexer = lex.lex()
