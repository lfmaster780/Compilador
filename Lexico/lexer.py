from enum import Enum

class TokenType(Enum):
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    PONTOVIRGULA = ";"
    VIRGULA = ","
    IF="if"
    ELSE="else"
    WHILE="while"
    RETURN="return"
    TYPE_BOOL="bool"
    TYPE_INT="int"
    TYPE_VOID="void"
    BREAK="break"
    CONTINUE="continue"
    TRUE="true"
    FALSE="false"

    ATRIBUICAO = '='

    OR = '||'

    AND = '&&'

    IGUAL = '==' #!=

    COMPARACAO= '<'
                   # | '>'
                   # | '<='
                   # | '>='

    SOMA = '+'
                   # | '-'

    MULT = '*'
                   # | '/'
                   # | '%'

    EOF = ""

class Token:

    def __init__(self, type, lexeme, literal, line):
        self.tipo = type
        self.lexema = lexeme
        self.literal = literal
        self.linha = line

    def __str__(self):
        return str(self.tipo)+", "+str(self.lexema)+", "+str(self.literal)+", "+str(self.linha)


class Scanner(object):

    def __init__(self, texto):
        self.tokens = []
        self.texto = texto
        self.start = 0;
        self.current = 0;
        self.line = 1;

    def isAtEnd(self):
        return self.current >= len(self.texto)

    def scanTokens(self) {
        while (not isAtEnd()):
            self.start = self.current
            scanToken()

        self.tokens.append(Token(EOF, "", None, line))
        return self.tokens
