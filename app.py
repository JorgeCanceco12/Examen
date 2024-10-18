from flask import Flask, request, render_template
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# Definición de tokens
tokens = (
    'IDENTIFICADOR',
    'VARIABLE',
    'PALABRA_RESERVADA',
    'SIMBOLO',
    'CADENA',
    'NUMERO',
)

# Definición de las expresiones regulares para cada token
t_IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_VARIABLE = r'\$[a-zA-Z_][a-zA-Z0-9_]*'
t_PALABRA_RESERVADA = r'\b(main|public|class|for|int|String|printf|scanf|System\.out\.print|return)\b'
t_SIMBOLO = r'[{}();,]'
t_CADENA = r'\"(\\.|[^\\"])*\"'
t_NUMERO = r'\d+'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Error de lexing en el token: {t.value}")

# Construir el analizador léxico
lexer = lex.lex()

# Definición de la gramática para el análisis sintáctico
def p_program(p):
    '''program : statement_list'''
    pass

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    pass

def p_statement(p):
    '''statement : PALABRA_RESERVADA
                 | IDENTIFICADOR
                 | VARIABLE
                 | CADENA
                 | SIMBOLO
                 | declaration'''
    pass

def p_declaration(p):
    '''declaration : PALABRA_RESERVADA IDENTIFICADOR SIMBOLO
                   | PALABRA_RESERVADA IDENTIFICADOR SIMBOLO statement_list SIMBOLO'''
    pass

def p_error(p):
    print("Error de parsing en el código")

# Construir el analizador sintáctico
parser = yacc.yacc()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicializar las listas para los tokens
    tokens_result = {
        'symbols': [],
        'variables': [],
        'identifiers': [],
        'reserved_words': [],
        'numbers': [],
        'strings': [],
    }
    syntax_check = ""

    if request.method == 'POST':
        code_input = request.form['code']
        action = request.form.get('action')

        if action == "lexico":
            # Análisis léxico
            lexer.input(code_input)
            for token in lexer:
                if token.type == 'SIMBOLO':
                    tokens_result['symbols'].append(token.value)
                elif token.type == 'VARIABLE':
                    tokens_result['variables'].append(token.value)
                elif token.type == 'IDENTIFICADOR':
                    tokens_result['identifiers'].append(token.value)
                elif token.type == 'PALABRA_RESERVADA':
                    tokens_result['reserved_words'].append(token.value)
                elif token.type == 'NUMERO':
                    tokens_result['numbers'].append(token.value)
                elif token.type == 'CADENA':
                    tokens_result['strings'].append(token.value)

        elif action == "sintactico":
            # Análisis sintáctico
            try:
                result = parser.parse(code_input)
                syntax_check = "El código está correctamente estructurado."
            except Exception as e:
                syntax_check = "Error en el código: " + str(e)

        elif action == "limpiar":
            # Limpiar los resultados
            code_input = ""
            tokens_result = {key: [] for key in tokens_result.keys()}
            syntax_check = ""

    return render_template('index.html', tokens=tokens_result, syntax_check=syntax_check)

if __name__ == '__main__':
    app.run(debug=True)
