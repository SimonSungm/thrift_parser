import ply.lex as lex

reserved = {
    'namespace': 'NAMESPACE',
    'struct': 'STRUCT',
    'service': 'SERVICE',
    'optional': 'OPTIONAL',
    'required': 'REQUIRED',
    'void': 'VOID',
    'include': 'INCLUDE',
    'i16': 'I16',
    'i32': 'I32',
    'i64': 'I64',
    'bool': 'BOOL',
    'string': 'STRING',
    'enum': 'ENUM',
}

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'COLON',
    'COMMA',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'STRING_LITERAL',
] + list(reserved.values())

t_COLON = r':'
t_COMMA = r','
t_EQUALS = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_STRING_LITERAL(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1]  # 去掉引号
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_\.]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'(//.*)|(/\*(.|\n)*?\*/)'
    pass

def t_error(t):
    print(f"非法字符 '{t.value[0]}' 在第 {t.lineno} 行")
    t.lexer.skip(1)

lexer = lex.lex()
