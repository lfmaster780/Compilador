class Escopo():
    def __init__(self, id, escopomaior):
        self.id = id
        self.escopomaior = escopomaior
        self.aberto = True
    def fecharEscopo(self):
        self.aberto = False

class Parser():

    def __init__(self):

        self.tokenAtual = 0
        self.tokens = []
        #self.escopo = False
        self.tabelaSimbolos = [ ]
        self.escopoatual = 0
        self.escopomax = 0
        self.escopos = []
        self.erroSintatico = False
        self.tipoEsperado = ""
        self.tipoAtual = ""
        self.exprAtual = []
        self.varfunc = []
        self.funcatual = ""
        self.funescopo = 0

    def iniciar(self,tokenlist):
        self.erroSintatico = False
        novoescopo = Escopo(self.escopoatual, -1)
        self.escopos.append(novoescopo)
        self.tokens = tokenlist
        self.decls()

    def buscar(self,lexema):
        tipo = "VOID"
        for k in range(len(self.tabelaSimbolos)):
            if self.tabelaSimbolos[k][1] == lexema and self.tabelaSimbolos[k][0] == "VARFUNC":
                if self.tabelaSimbolos[k][3] == self.funcatual:
                    return self.tabelaSimbolos[k][2].upper()

            elif self.tabelaSimbolos[k][1] == lexema and self.tabelaSimbolos[k][0] == "VAR":
                if self.tabelaSimbolos[k][3].id == self.escopoatual:
                    return self.tabelaSimbolos[k][2].upper()
        print("Item "+lexema+" nao exite nesse escopo")
        return tipo

    def gerartipo(self):
        print(self.exprAtual)
        chave=self.exprAtual[0]
        resultado = "VOID"
        for k in range(0,len(self.exprAtual)-2,2):

            op = self.exprAtual[k+1]
            tipo2 = self.exprAtual[k+2]
            print(k, chave, op, tipo2, chave == tipo2)
            if chave == tipo2:
                if op == "OPINT":
                    print("É INT")
                    resultado = "INT"
                else:
                    resultado = "BOOL"
            else:
                "INVALIDO"
            print (resultado)
            chave = resultado

        return resultado

    def erro(self,l):
        print("Erro Sintatico")
        print("Esperado ",end="")
        for k in l:
            print(k,end=" ")

        print("Obteve",self.tokens[self.tokenAtual])

        self.erroSintatico = True

        print(self.tokenAtual)
        raise TypeError

    def type(self):
        if self.match_token("VOID") or self.match_token("INT") or self.match_token("BOOL"):
            return True
        else:
            self.erro(["VOID","INT","BOOL"])
            return False

    def typeID(self):
        if self.match_token("INT") or self.match_token("BOOL"):
            return True
        else:
            self.erro(["INT","BOOL"])
            return False

    def match_token(self, t):
        return self.tokens[self.tokenAtual].tipo == t

    def consumir(self):
        self.tokenAtual += 1

    def decls(self):
        if self.match_token("EOF"):
            return

        if self.match_token("FUN") or self.match_token("ID"):
            self.decl()
            self.decls()

        else:
            self.erro(["ID","FUN"])

    def decl(self):
        if self.match_token("FUN"):
            self.func_decl()
        else:
            self.var_decl()

    def func_decl(self):
        lista = []
        if self.match_token("FUN"):
            lista.append("FUN")
            self.consumir()
        else:
            self.erro(["FUN"])
            return
        if self.match_token("ID"):
            lista.append(self.tokens[self.tokenAtual].lexema)
            self.funcatual = self.tokens[self.tokenAtual].lexema
            self.consumir()
            ###CHECAR SE EXITE FUN DO MSM NOME
            if self.match_token("RETURN"):
                self.consumir()
                if self.type():
                    lista.append(self.tokens[self.tokenAtual].tipo)
                    self.consumir()
                else:
                    return
                if self.match_token("LPAREN"):
                    self.consumir()
                    listaparametros = self.params()
                    lista.append(listaparametros)
                    lista.append(self.escopos[self.funescopo])
                    self.funescopo = 0
                else:
                    self.erro("LPAREN")

            else:
                self.erro(["RETURN"])

        else:
            self.erro(["ID"])
        self.tabelaSimbolos.append(lista)

    def params(self):
        listaparams = []
        if self.match_token("RPAREN"):
            self.consumir()
            self.block()
            print(self.funescopo)
        elif self.typeID():
            listaparams.append(self.tokens[self.tokenAtual].tipo)
            self.param()
            self.varfunc.append(listaparams[-1])
            self.varfunc.append(self.funcatual)
            if self.match_token("VIRGULA"):
                if(len(self.varfunc) > 0):
                    self.tabelaSimbolos.append(self.varfunc)
                    self.varfunc = []
                self.consumir()
                self.params()
            elif self.match_token("RPAREN"):
                if(len(self.varfunc) > 0):
                    self.tabelaSimbolos.append(self.varfunc)
                    self.varfunc = []
                self.params()
            else:
                self.erro(["VIRGULA","RPAREN"])
        else:
            self.erro(["RPAREN"])
        return listaparams

    def param(self):
        if self.typeID():
            self.varfunc.append("VARFUNC")
            self.consumir()
            if self.match_token("ID"):
                self.varfunc.append(self.tokens[self.tokenAtual].lexema)
                self.consumir()
            else:
                self.erro(["ID"])

    def block(self):
        if self.match_token("LBRACE"):
            if(self.escopoatual+1 > self.escopomax):
                if(self.escopos[self.escopoatual].aberto):
                    novoescopo = Escopo(self.escopoatual+1, self.escopoatual)
                    self.escopomax = self.escopoatual+1
                    self.escopoatual += 1
                else:
                    novoescopo = Escopo(self.escopoatual+1, -1)
                    self.escopomax = self.escopoatual+1
                    self.escopoatual += 1
            else:
                if(self.escopos[self.escopoatual].aberto):
                    novoescopo = Escopo(self.escopomax+1, self.escopoatual)
                    self.escopomax = self.escopomax+1
                    self.escopoatual = self.escopomax
                else:
                    novoescopo = Escopo(self.escopoatual+1, -1)
                    self.escopomax = self.escopomax+1
                    self.escopoatual = self.escopomax
            self.escopos.append(novoescopo)
            if(self.funescopo == 0):
                self.funescopo = self.escopoatual
            self.consumir()
            self.stm_list()

            if self.match_token("RBRACE"):
                self.escopos[self.escopoatual].fecharEscopo()
                self.escopoatual = self.escopos[self.escopoatual].escopomaior + 1
                self.consumir()
            else:
                self.erro(["RBRACE"])
        else:
            self.erro(["LBRACE"])

    def stm_list(self):
        if self.match_token("RBRACE"):
            return
        elif self.match_token("ID") or self.match_token("IF") or self.match_token("WHILE") or self.match_token("PRINT") or self.match_token("BREAK") or self.match_token("CONTINUE") or self.match_token("RETURN") or self.match_token("LBRACE"):
            self.stm()
            self.stm_list()
        else:
            self.erro(["RBRACE","ID","WHILE","PRINT","LBRACE","RETURN","IF","BREAK","CONTINUE"])

    def paramC(self):
        listaparams = []
        if self.match_token("RPAREN"):
            self.consumir()
        if self.match_token("ID"):
            self.consumir()
            self.paramC()
        if self.match_token("VIRGULA"):
            self.consumir()
            self.paramC()
        elif self.match_token("RPAREN"):
            self.paramC()
        elif self.match_token("NUMERO"):
            self.consumir()
            self.paramC()
        else:
            self.erro(["VIRGULA","RPAREN","ID"])
        return listaparams

    def stm(self):
        if self.match_token("ID"):
            if self.tokens[self.tokenAtual+1].tipo == "ATRIBUICAO":
                try:
                    self.tipoEsperado = self.buscar(self.tokens[self.tokenAtual].lexema)#$$
                except:
                    return

                self.consumir()
                if self.match_token("ATRIBUICAO"):
                    self.consumir()
                    self.exprAtual = [] #Inicio da expressao
                    self.expr()#################
                    #fun android return int(int a, int b){ print(a); a int; a = 10+5;}
                    self.tipoAtual = self.gerartipo()
                    if self.match_token("PONTOVIRGULA"):
                        self.consumir()
                    else:
                        self.erro(["PONTOVIRGULA"])
                    if self.tipoEsperado != self.tipoAtual:
                        print("Erro Semantico",self.tokenAtual,self.tokens[self.tokenAtual+1].tipo)
                        print("Esperado:",self.tipoEsperado,"Obteve:",self.tipoAtual)
                        raise TypeError
            elif self.tokens[self.tokenAtual+1].tipo == "INT" or self.tokens[self.tokenAtual+1].tipo == "BOOL":
                self.var_decl()
            elif self.tokens[self.tokenAtual+1].tipo == "LPAREN":
                self.consumir()
                self.paramC()
            else:
                self.exprAtual = [] #Inicio da expressao
                self.expr()
                if self.match_token("PONTOVIRGULA"):
                    self.tipoAtual = self.gerartipo()
                    self.consumir()
                else:
                    self.erro(["PONTOVIRGULA"])

        elif self.match_token("IF"):
            self.consumir()
            if self.match_token("LPAREN"):
                self.consumir()
                self.tipoEsperado = "BOOL"
                self.exprAtual = []
                self.expr()#####
                self.tipoAtual = self.gerartipo()
                if self.tipoAtual != self.tipoEsperado:
                    print("Erro Semantico")
                    print("Esperado:",self.tipoEsperado,"Obteve:",self.tipoAtual)
                    raise TypeError
                if self.match_token("RPAREN"):
                    self.consumir()
                    self.stm()
                    self.post_if()########
                else:
                    self.erro(["RPAREN"])
            else:
                self.erro(["LPAREN"])

        elif self.match_token("WHILE"):
            self.consumir()
            if self.match_token("LPAREN"):
                self.consumir()
                self.tipoEsperado = "BOOL"
                self.exprAtual = []
                self.expr()#####
                self.tipoAtual = self.gerartipo()
                if self.tipoAtual != self.tipoEsperado:
                    print("Erro Semantico")
                    print("Esperado:",self.tipoEsperado,"Obteve:",self.tipoAtual)
                    raise TypeError
                if self.match_token("RPAREN"):
                    self.consumir()
                    self.stm()
                else:
                    self.erro(["RPAREN"])
            else:
                self.erro(["LPAREN"])

        elif self.match_token("PRINT"):
            self.consumir()
            if self.match_token("LPAREN"):
                self.consumir()
                if self.match_token("ID") or self.match_token("NUMERO"):
                    self.consumir()
                    if self.match_token("RPAREN"):
                        self.consumir()
                        if self.match_token("PONTOVIRGULA"):
                            self.consumir()
                        else:
                            self.erro(["PONTOVIRGULA"])
                    else:
                        self.erro(["RPAREN"])
                else:
                    self.erro(["ID"])
            else:
                self.erro(["LPAREN"])

        elif self.match_token("BREAK"):
            self.consumir()
            if self.match_token("PONTOVIRGULA"):
                self.consumir()
            else:
                self.erro(["PONTOVIRGULA"])

        elif self.match_token("CONTINUE"):
            self.consumir()
            if self.match_token("PONTOVIRGULA"):
                self.consumir()
            else:
                self.erro(["PONTOVIRGULA"])

        elif self.match_token("RETURN"):########
            self.consumir()
            self.tipoEsperado = self.tipoFunc()
            self.exprAtual = []
            self.expr()#####
            self.tipoAtual = self.gerartipo()
            if self.tipoAtual != self.tipoEsperado:
                print("Erro Semantico")
                print("Esperado:",self.tipoEsperado,"Obteve:",self.tipoAtual)
                raise TypeError
            if self.match_token("PONTOVIRGULA"):
                self.consumir()
            else:
                self.erro(["PONTOVIRGULA"])

        elif self.match_token("LBRACE"):
            self.block()
        else:
            self.erro(["RBRACE","ID","WHILE","PRINT","LBRACE","RETURN","IF","BREAK","CONTINUE"])

    def var_decl(self):
        lista = []
        if self.match_token("ID"):
            lista.append("VAR")
            lista.append(self.tokens[self.tokenAtual].lexema)
            self.consumir()
            if self.typeID():
                lista.append(self.tokens[self.tokenAtual].tipo)
                self.consumir()
                if self.match_token("PONTOVIRGULA"):
                    self.consumir()
                else:
                    self.erro(["PONTOVIRGULA"])

        else:
            self.erro(["ID"])
        self.funescopo = self.escopoatual
        lista.append(self.escopos[self.escopoatual])
        self.tabelaSimbolos.append(lista)

    def post_if(self):
        if self.match_token("ELSE"):
            self.consumir()
            self.stm()

    def expr(self):
        if self.match_token("NUMERO"):
            self.consumir()
            self.exprAtual.append("INT")
            self.op_na()
            if self.match_token("NUMERO") and not self.erroSintatico:
                self.consumir()
                self.exprAtual.append("INT")
                if self.match_token("SOMA") or self.match_token("MULT") or self.match_token("RESTO") or self.match_token("SUB") or self.match_token("DIV") or self.match_token("NOT") or self.match_token("DIFERENTE") or self.match_token("IGUAL") or self.match_token("MENOR") or self.match_token("MENORIGUAL") or self.match_token("MAIOR") or self.match_token("MAIORIGUAL") or self.match_token("AND") or self.match_token("OR"):
                    self.op_na()
                    self.expr()
                elif self.match_token("PONTOVIRGULA"):
                    return
                else:
                    self.erro(["OPERADOR"])
            else:
                self.erro(["NUMERO"])

        elif self.match_token("ID"):

            self.exprAtual.append(self.buscar(self.tokens[self.tokenAtual].lexema))
            self.consumir()
            self.op_na()
            if not self.erroSintatico:
                self.expr_id()


    def expr_id(self):
        if self.match_token("BOOLEAN"):
            self.exprAtual.append("BOOL")
            self.consumir()
            if self.match_token("ATRIBUICAO") or self.match_token("SOMA") or self.match_token("MULT") or self.match_token("RESTO") or self.match_token("SUB") or self.match_token("DIV") or self.match_token("NOT") or self.match_token("DIFERENTE") or self.match_token("IGUAL") or self.match_token("MENOR") or self.match_token("MENORIGUAL") or self.match_token("MAIOR") or self.match_token("MAIORIGUAL") or self.match_token("AND") or self.match_token("OR"):
                self.op_na()
                self.expr()
        elif self.match_token("NUMERO"):
            self.exprAtual.append("INT")
            self.consumir()
            if self.match_token("ATRIBUICAO") or self.match_token("SOMA") or self.match_token("MULT") or self.match_token("RESTO") or self.match_token("SUB") or self.match_token("DIV") or self.match_token("NOT") or self.match_token("DIFERENTE") or self.match_token("IGUAL") or self.match_token("MENOR") or self.match_token("MENORIGUAL") or self.match_token("MAIOR") or self.match_token("MAIORIGUAL") or self.match_token("AND") or self.match_token("OR"):
                self.op_na()
                self.expr()
        elif self.match_token("ID"):
            self.exprAtual.append(self.buscar(self.tokens[self.tokenAtual].lexema))
            self.consumir()
            if self.match_token("ATRIBUICAO") or self.match_token("SOMA") or self.match_token("MULT") or self.match_token("RESTO") or self.match_token("SUB") or self.match_token("DIV") or self.match_token("NOT") or self.match_token("DIFERENTE") or self.match_token("IGUAL") or self.match_token("MENOR") or self.match_token("MENORIGUAL") or self.match_token("MAIOR") or self.match_token("MAIORIGUAL") or self.match_token("AND") or self.match_token("OR"):
                self.op_na()
                self.expr()
        else:
            self.erro(["BOOLEAN","ID","NUMERO"])

    def operator(self):
        if self.match_token("ATRIBUICAO"):
            self.exp
            self.consumir()

        elif self.match_token("SOMA"):
            self.op_na()

        elif self.match_token("MULT"):
            self.op_na()

        elif self.match_token("RESTO"):
            self.op_na()

        elif self.match_token("DIV"):
            self.op_na()

        elif self.match_token("NOT"):
            self.op_na()

        elif self.match_token("DIFERENTE"):
            self.op_na()

        elif self.match_token("IGUAL"):
            self.op_na()

        elif self.match_token("AND"):
            self.op_na()

        elif self.match_token("OR"):
            self.op_na()

        elif self.match_token("MENOR"):
            self.op_na()

        elif self.match_token("MENORIGUAL"):
            self.op_na()

        elif self.match_token("MAIOR"):
            self.op_na()

        elif self.match_token("MAIORIGUAL"):
            self.op_na()

        elif self.match_token("SUB"):
            self.op_na()

        else:
            self.erro(["ATRIBUICAO","SOMA","MULT","RESTO","SUB","DIV","NOT","DIFERENTE","IGUAL","MENOR","MENORIGUAL","MAIO","MAIORIGUAL","AND","OR"])

    def op_na(self):
        if self.match_token("SOMA"):
            self.exprAtual.append("OPINT")
            self.consumir()

        elif self.match_token("MULT"):
            self.exprAtual.append("OPINT")
            self.consumir()

        elif self.match_token("RESTO"):
            self.exprAtual.append("OPINT")
            self.consumir()

        elif self.match_token("DIV"):
            self.exprAtual.append("OPINT")
            self.consumir()

        elif self.match_token("NOT"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("DIFERENTE"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("IGUAL"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("AND"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("OR"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("MENOR"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("MENORIGUAL"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("MAIOR"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("MAIORIGUAL"):
            self.exprAtual.append("OPBOOL")
            self.consumir()

        elif self.match_token("SUB"):
            self.exprAtual.append("OPINT")
            self.consumir()

        else:
            self.erro(["SOMA","MULT","RESTO","SUB","DIV","NOT","DIFERENTE","IGUAL","MENOR","MENORIGUAL","MAIO","MAIORIGUAL","AND","OR"])
