import ply.yacc as yacc
import os
from thrift_lexer import tokens, lexer

thrift_definitions = {
    'namespaces': [],
    'structs': [],
    'services': [],
    'enums': [],
    'includes': []
}

current_dir = ""
current_namespace = None

def parse_file(filename):
    global current_dir, current_namespace
    previous_dir = current_dir
    previous_namespace = current_namespace  # 保存之前的namespace状态

    current_dir = os.path.dirname(os.path.abspath(filename))
    with open(filename, 'r') as f:
        data = f.read()
    parser = yacc.yacc()
    parser.parse(data, lexer=lexer.clone())

    current_dir = previous_dir
    current_namespace = previous_namespace

def p_thrift_file(p):
    '''thrift_file : thrift_file definition
                   | definition'''
    pass

def p_definition(p):
    '''definition : namespace
                  | struct
                  | service
                  | enum
                  | include'''
    pass

def p_include(p):
    'include : INCLUDE STRING_LITERAL'
    included_file = os.path.join(current_dir, p[2])
    thrift_definitions['includes'].append(included_file)
    parse_file(included_file)

def p_namespace(p):
    'namespace : NAMESPACE IDENTIFIER IDENTIFIER'
    global current_namespace
    current_namespace = {'language': p[2], 'name': p[3]}
    thrift_definitions['namespaces'].append({'language': p[2], 'name': p[3]})

def p_enum(p):
    'enum : ENUM IDENTIFIER LBRACE enum_field_list RBRACE'
    enum_namespace = current_namespace['name'] if current_namespace else None
    thrift_definitions['enums'].append({
        'name': p[2],
        'fields': p[4],
        'namespace': enum_namespace
    })

def p_enum_field_list(p):
    '''enum_field_list : enum_field_list enum_field
                       | enum_field'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_enum_field(p):
    '''enum_field : IDENTIFIER EQUALS NUMBER COMMA
                  | IDENTIFIER EQUALS NUMBER'''
    p[0] = {'name': p[1], 'value': p[3]}


def p_const_value(p):
    '''const_value : NUMBER
                   | BOOL_VALUE
                   | STRING_LITERAL
                   | IDENTIFIER'''
    p[0] = p[1]

def p_struct(p):
    'struct : STRUCT IDENTIFIER LBRACE field_list RBRACE'
    struct_namespace = current_namespace['name'] if current_namespace else None
    thrift_definitions['structs'].append({
        'name': p[2],
        'fields': p[4],
        'namespace': struct_namespace
    })

def p_field_list(p):
    '''field_list : field_list field
                  | field'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_field(p):
    '''field : NUMBER COLON field_req field_type IDENTIFIER EQUALS const_value COMMA
             | NUMBER COLON field_req field_type IDENTIFIER EQUALS const_value SEMICOLON
             | NUMBER COLON field_req field_type IDENTIFIER EQUALS const_value
             | NUMBER COLON field_req field_type IDENTIFIER COMMA
             | NUMBER COLON field_req field_type IDENTIFIER SEMICOLON
             | NUMBER COLON field_req field_type IDENTIFIER'''
    field_dict = {
        'id': p[1],
        'requiredness': p[3],
        'type': p[4],
        'name': p[5],
        'default': None
    }
    if len(p) == 9 or len(p) == 8:
        field_dict['default'] = p[7]
    p[0] = field_dict

def p_field_req(p):
    '''field_req : OPTIONAL
                 | REQUIRED
                 | empty'''
    p[0] = p[1] if p[1] else 'default'

def p_field_type(p):
    '''field_type : IDENTIFIER
                  | STRING
                  | BOOL
                  | I16
                  | I32
                  | I64'''
    p[0] = p[1]

def p_service(p):
    'service : SERVICE IDENTIFIER LBRACE function_list RBRACE'
    thrift_definitions['services'].append({'name': p[2], 'functions': p[4]})

def p_function_list(p):
    '''function_list : function_list function
                     | function'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_function(p):
    '''function : function_type IDENTIFIER LPAREN param_list RPAREN COMMA
                | function_type IDENTIFIER LPAREN param_list RPAREN'''
    p[0] = {
        'return_type': p[1],
        'name': p[2],
        'params': p[4]
    }

def p_function_type(p):
    '''function_type : VOID
                     | IDENTIFIER'''
    p[0] = p[1]

def p_param_list(p):
    '''param_list : param_list field
                  | field
                  | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"语法错误在 '{p.value}' 第 {p.lineno} 行")
    else:
        print("语法错误在文件末尾")

parser = yacc.yacc()
