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

    def iniciar(self,tokenlist):
        self.erroSintatico = False
        novoescopo = Escopo(self.escopoatual, -1)
        self.escopos.append(novoescopo)
        self.tokens = tokenlist
        self.decls()

    def erro(self,l):
        print("Erro Sintatico")
        print("Esperado ",end="")
        for k in l:
            print(k,end=" ")

        print("Obteve",self.tokens[self.tokenAtual])

        self.erroSintatico = True

        print(self.tokenAtual)

    def type(self):
        if self.match_token("VOID") or self.match_token("INT") or self.match_token("BOOL"):
            return True
        else:
            self.erro(["VOID","INT","BOOL"])
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
            self.consumir()

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
        elif self.type():
            listaparams.append(self.tokens[self.tokenAtual].tipo)
            self.param()
            if self.match_token("VIRGULA"):
                self.consumir()
                self.params()
            elif self.match_token("RPAREN"):
                self.params()
            else:
                self.erro(["VIRGULA","RPAREN"])
        else:
            self.erro(["RPAREN"])
        return listaparams

    def param(self):
        if self.type():
            self.consumir()
            if self.match_token("ID"):
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

    def stm(self):
        if self.match_token("ID"):
            if self.tokens[self.tokenAtual+1].tipo == "ATRIBUICAO":
                self.consumir()
                if self.match_token("ATRIBUICAO"):
                    self.consumir()
                    self.expr()#################
            elif self.tokens[self.tokenAtual+1].tipo == "VOID" or self.tokens[self.tokenAtual+1].tipo == "INT" or self.tokens[self.tokenAtual+1].tipo == "BOOL":
                self.var_decl()
            else:
                self.expr()
                if self.match_token("PONTOVIRGULA"):
                    self.consumir()
                else:
                    self.erro(["PONTOVIRGULA"])

        elif self.match_token("IF"):
            self.consumir()
            if self.match_token("LPAREN"):
                self.consumir()
                self.expr()#####
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
                self.expr()#####
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
                if self.match_token("ID"):
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

        elif self.match_token("RETURN"):
            self.consumir()
            self.expr()
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
            if self.type():
                lista.append(self.tokens[self.tokenAtual].tipo)
                self.consumir()
                if self.match_token("PONTOVIRGULA"):
                    self.consumir()
                else:
                    self.erro(["PONTOVIRGULA"])

        else:
            self.erro(["ID"])
        lista.append(self.escopos[self.escopoatual])
        self.tabelaSimbolos.append(lista)

    def post_if(self):
        if self.match_token("ELSE"):
            self.consumir()
            self.stm()

    def expr(self):
        if self.match_token("NUMERO"):
            self.consumir()
            self.op_na()
            if self.match_token("NUMERO") and not self.erroSintatico:
                self.consumir()
                self.expr()

            else:
                self.erro(["NUMERO"])

        elif self.match_token("ID"):
            self.consumir()
            self.operator()
            if not self.erroSintatico:
                self.expr_id()

        else:
            print("")
            #self.erro(["NUMERO","ID"])

    def expr_id():
        if self.match_token("BOOLEAN"):
            self.consumir()
            self.expr()
        elif self.match("NUMERO"):
            self.consumir()
            self.expr()
        elif self.match("ID"):
            self.consumir()
            self.expr()
        else:
            self.erro(["BOOLEAN","ID","NUMERO"])

    def operator(self):
        if self.match_token("ATRIBUICAO"):
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
            self.consumir()

        elif self.match_token("MULT"):
            self.consumir()

        elif self.match_token("RESTO"):
            self.consumir()

        elif self.match_token("DIV"):
            self.consumir()

        elif self.match_token("NOT"):
            self.consumir()

        elif self.match_token("DIFERENTE"):
            self.consumir()

        elif self.match_token("IGUAL"):
            self.consumir()

        elif self.match_token("AND"):
            self.consumir()

        elif self.match_token("OR"):
            self.consumir()

        elif self.match_token("MENOR"):
            self.consumir()

        elif self.match_token("MENORIGUAL"):
            self.consumir()

        elif self.match_token("MAIOR"):
            self.consumir()

        elif self.match_token("MAIORIGUAL"):
            self.consumir()

        elif self.match_token("SUB"):
            self.consumir()

        else:
            self.erro(["SOMA","MULT","RESTO","SUB","DIV","NOT","DIFERENTE","IGUAL","MENOR","MENORIGUAL","MAIO","MAIORIGUAL","AND","OR"])
