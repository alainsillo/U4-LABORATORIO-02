import re

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo      # KEYWORD, IDENTIFIER, NUMBER, etc.
        self.valor = valor    # El texto tal cual: int, main, +, (, etc.
        self.linea = linea    # Número de renglón donde apareció

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, linea={self.linea})"


class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.linea = 1

        # Especificación de tokens (el orden importa)
        self.patrones = [
            # Comentarios multilínea
            ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),

            # Comentarios de una línea
            ('COMMENT', r'//.*'),

            ('KEYWORD',   r'\b(if|else|while|for|return|int|float|char|void|main)\b'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER',    r'\d+(\.\d+)?'),
            ('STRING',    r'\".*?\"'),
            ('OPERATOR',  r'==|!=|<=|>=|\+|\-|\*|/|=|<|>'),
            ('DELIMITER', r'[;,\(\)\{\}]'),
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE',   r'\n'),
            ('ERROR',     r'.')
        ]

    def tokenizar(self):
        tokens = []
        while self.pos < len(self.codigo):
            encontrado = False
            for tipo, patron in self.patrones:
                regex = re.compile(patron)
                match = regex.match(self.codigo, self.pos)

                if match:
                    valor = match.group(0)

                    if tipo == 'NEWLINE':
                        self.linea += 1
                    elif tipo not in ['WHITESPACE', 'NEWLINE', 'COMMENT', 'COMMENT_MULTI']:
                        tokens.append(Token(tipo, valor, self.linea))

                    self.pos = match.end()
                    encontrado = True
                    break

            if not encontrado:
                # Avanza un carácter si nada coincidió (evita ciclo infinito)
                self.pos += 1

        return tokens


def clasificar_token(token: Token):
    """
    Regresa (lexema, categoria) para la tabla de símbolos.
    Lexema: abreviatura (PR, ID, NUM, etc.)
    Categoría: descripción (PALABRA_RESERVADA, IDENTIFICADOR, etc.)
    """

    if token.tipo == 'KEYWORD':
        return ('PR', 'PALABRA_RESERVADA')

    if token.tipo == 'IDENTIFIER':
        return ('ID', 'IDENTIFICADOR')

    if token.tipo == 'NUMBER':
        return ('NUM', 'NUMERO')

    if token.tipo == 'STRING':
        return ('CAD', 'CADENA')

    if token.tipo == 'OPERATOR':
        if token.valor == '+':
            return ('MAS', 'OPERADOR_ARITMÉTICO')
        elif token.valor == '-':
            return ('MENOS', 'OPERADOR_ARITMÉTICO')
        elif token.valor == '*':
            return ('POR', 'OPERADOR_ARITMÉTICO')
        elif token.valor == '/':
            return ('ENTRE', 'OPERADOR_ARITMÉTICO')
        elif token.valor == '=':
            return ('ASIG', 'OPERADOR_ASIGNACIÓN')
        elif token.valor in ['==', '!=', '<', '>', '<=', '>=']:
            return ('REL', 'OPERADOR_RELACIONAL')
        else:
            return ('OP', 'OPERADOR')

    if token.tipo == 'DELIMITER':
        if token.valor == '(':
            return ('PA', 'AGRUPACIÓN')
        elif token.valor == ')':
            return ('PC', 'AGRUPACIÓN')
        elif token.valor == '{':
            return ('LLA', 'AGRUPACIÓN')
        elif token.valor == '}':
            return ('LLC', 'AGRUPACIÓN')
        elif token.valor == ';':
            return ('PYC', 'FIN_INSTRUCCION')
        elif token.valor == ',':
            return ('COMA', 'SEPARADOR')
        else:
            return ('DELIM', 'DELIMITADOR')

    if token.tipo == 'ERROR':
        return ('ERR', 'ERROR_LEXICO')

    # Por si falta algo
    return (token.tipo, 'OTRO')


def leer_archivo_entrada(nombre_archivo: str) -> str:
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        return f.read()


def generar_tabla_simbolos(tokens, nombre_salida: str):
    """
    Genera un archivo de texto con la tabla de símbolos:
    Renglón | Token | Lexema | Categoría
    """
    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write("Renglón\tToken\tLexema\tCategoría\n")
        for token in tokens:
            lexema, categoria = clasificar_token(token)
            f.write(f"{token.linea}\t{token.valor}\t{lexema}\t{categoria}\n")


def main():
    archivo_entrada = "codigo_fuente.txt"
    archivo_salida_tabla = "tabla_simbolos.txt"

    print("Leyendo archivo de entrada:", archivo_entrada)
    codigo = leer_archivo_entrada(archivo_entrada)

    lexer = AnalizadorLexico(codigo)
    tokens = lexer.tokenizar()

    print("\nTOKENS ENCONTRADOS:\n")
    for t in tokens:
        print(f"Línea {t.linea:<3}  Tipo: {t.tipo:<10}  Valor: {t.valor}")

    generar_tabla_simbolos(tokens, archivo_salida_tabla)
    print(f"\nTabla de símbolos generada en: {archivo_salida_tabla}")


if __name__ == "__main__":
    main()
