from Lexico.lexer import Token
from Lexico.lexer import Scanner
from Sintatico.parser import Parser

arquivo = open("entrada.txt", "r")
ent = ""
for k in arquivo.readlines():
    ent += k
lexer = Scanner(ent)
resultado = lexer.scanTokens()
parser = Parser()
try:
    parser.iniciar(resultado)
    print("Codigo Valido")
    print("-------------")
    print(parser.tabelaSimbolos)
    for k in range(len(parser.tabelaSimbolos)):
        if(parser.tabelaSimbolos[k][0] == "FUN" or parser.tabelaSimbolos[k][0] == "VAR"):
            print(parser.tabelaSimbolos[k][1], parser.tabelaSimbolos[k][-1].id)
    for k in range(len(parser.escopos)):
        print(parser.escopos[k].id, parser.escopos[k].escopomaior, parser.escopos[k].aberto)
except:
    print("Codigo invalido")

arquivo.close()
