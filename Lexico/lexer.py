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

    def scanTokens(self):
        while (not self.isAtEnd()):
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token("EOF", "", None, self.line))
        for k in self.tokens:
            if k.tipo == "ID":
                if k.lexema == "while":
                    k.tipo = k.lexema.upper()
                if k.lexema == "for":
                    k.tipo = k.lexema.upper()
                if k.lexema == "return":
                    k.tipo = k.lexema.upper()
                if k.lexema == "if":
                    k.tipo = k.lexema.upper()
                if k.lexema == "else":
                    k.tipo = k.lexema.upper()
                if k.lexema == "bool":
                    k.tipo = k.lexema.upper()
                if k.lexema == "int":
                    k.tipo = k.lexema.upper()
                if k.lexema == "void":
                    k.tipo = k.lexema.upper()
                if k.lexema == "break":
                    k.tipo = k.lexema.upper()
                if k.lexema == "continue":
                    k.tipo = k.lexema.upper()
                if k.lexema == "return":
                    k.tipo = k.lexema.upper()
                if k.lexema == "fun":
                    k.tipo = k.lexema.upper()
                if k.lexema == "print":
                    k.tipo = k.lexema.upper()
                if k.lexema == "true" or k.lexema == "false":
                    k.tipo = "BOOLEAN"

        return self.tokens

    def scanToken(self):
        c = self.advance();
        if c =='(':
            self.addToken("LPAREN")
        elif c ==')':
            self.addToken("RPAREN")
        elif c =='{':
            self.addToken("LBRACE")
        elif c =='}':
            self.addToken("RBRACE")
        elif c ==',':
            self.addToken("VIRGULA")
        elif c =='+':
            self.addToken("SOMA")
        elif c == '-':
            self.addToken("SUB")
        elif c ==';':
            self.addToken("PONTOVIRGULA")
        elif c =='*':
            self.addToken("MULT")
        elif c == '/':
            self.addToken("DIV")
        elif c == ("%"):
            self.addToken("RESTO")
        elif c == '=':
            if self.match('='):
                self.addToken("IGUAL")
            else:
                self.addToken("ATRIBUICAO")

        elif c == '!':
            if self.match("="):
                self.addToken("DIFERENTE")
            else:
                self.addToken("NOT")

        elif c == '<':
            if self.match("="):
                self.addToken("MENORIGUAL")
            else:
                self.addToken("MENOR")
        elif c == '>':
            if self.match("="):
                self.addToken("MAIORIGUAL")
            else:
                self.addToken("MAIOR")
        elif c == '&' and self.match('&'):
            self.addToken("AND")
        elif c == '|' and self.match('|'):
            self.addToken("OR")
        elif c == " " or c == '\t' or c == '\r':
            None
        elif c == '\n':
            self.line+=1
        elif self.isDigit(c):
            self.number()
        elif self.isAlpha(c):
            self.identifier()
        else:
            print("Caractere", c, "invalido na linha", self.line)
            raise Exception()

    def match(self,expected):
        if self.isAtEnd():
            return False
        if (self.texto[self.current] != expected):
            return False;

        self.current+=1
        return True

    def advance(self):
        self.current+=1
        return self.texto[self.current - 1]

    def addToken(self, type, literal = None):
        text = self.texto[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))


    def peek(self):
        if (self.isAtEnd()):
            return '\0'

        return self.texto[self.current]

    def isDigit(self,c):
      return c >= '0' and c <= '9'

    def number(self):
        while (self.isDigit(self.peek())):
            self.advance()

        self.addToken("NUMERO",int(self.texto[self.start:self.current]))

    def identifier(self):
        while (self.isAlphaNumeric(self.peek())):
            self.advance()

        self.addToken("ID",str(self.texto[self.start:self.current]))

    def isAlpha(self,c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

"""
ent = input()
scan = Scanner(ent)
resultado = scan.scanTokens()
for k in resultado:
    print(k)
"""
