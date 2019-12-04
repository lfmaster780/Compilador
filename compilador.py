from Lexico.lexer import Token
from Lexico.lexer import Scanner
from Sintatico.parser import Parser

print("FOI")
ent = input()
lexer = Scanner(ent)
resultado = lexer.scanTokens()
parser = Parser()
parser.iniciar(resultado)
print(parser.tabelaSimbolos)
#print(len(parser.escopos))
