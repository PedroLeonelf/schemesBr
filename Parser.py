import Modelo as model
import Entidade as entity
import Relacionamento as relation

class Parser:

    def getModelo(self):
        return self.modelo
    
    def setLinhas(self, linhas):
        self.linhas = linhas

    
    def traduzLinhas(self):
        self.numeroLinha = 1
        self.modelo = model.Modelo()
        for linha in self.linhas:
            print(linha)
            try:
                self.traduzLinha(linha)
            except Exception as e: 
                print(e)
                self.modelo = None
                return
            self.numeroLinha+=1
        print("Compilation complete.")


    def traduzLinha(self, linha):
        if linha == '\n':
            return
        linha = linha.strip()
        self.linhaAtual = linha
        if linha[:7].lower() + linha[-1] ==  "entity()":
            self.defineEntidade(linha[7:-1])
        elif linha[:9].lower() + linha[-1] == "relation()":
            self.defineRelacionamento(linha[9:-1])
        elif linha[:10].lower() + linha[-1] == "attribute()":
            self.defineAtributacao(linha[10:-1])
        else:
            self.levantaErro(f"Illegal character in line {self.numeroLinha}")

    

    def defineEntidade(self, linha):
        self.checaVazio(linha)
        self.checaNome(linha, "Entity")
        self.checaKey(linha)

        self.checaCardinalidade(linha)
        self.checaArgumentoGrande(linha, "Entity")
        
        self.modelo.adicionaEntidade(self.criaEntidade(linha))
        
        
    

    def checaVazio(self, linha):
        if linha == "":
            self.levantaErro(f"Entity is empty in {self.linhaAtual} line {self.numeroLinha}.")
            
        self.checaArgumentoVazio(linha)

    def checaArgumentoVazio(self, linha):
        for argumento in linha.split(','):
            palavras = argumento.strip().split(' ')
            for palavra in palavras:
                if palavra == '':
                    self.levantaErro(f"Parameter empty in {self.linhaAtual}, line {self.numeroLinha}")
                    
    
    def checaNome(self, linha, type):
        nome = linha.split(',')[0]
        if len(nome.strip().split()) > 1:
            self.levantaErro(f"{type} name can't have more than one word in {self.linhaAtual}, line {self.numeroLinha}")
        elif self.nomeNaoUnico(nome):
            self.levantaErro(f"{type} name {nome} is duplicated.")
    

    def nomeNaoUnico(self, nome):
        for entity in self.getModelo().getEntidades():
            if entity.getNome() == nome:
                return True

        for relation in self.getModelo().getRelacionamentos():
            if relation.getNome() == nome:
                return True
            
        return False
            
    
    def checaKey(self, linha):
        contKeys = 0
        for palavra in linha.split(','):
            palavras = palavra.strip().split(' ')
            if palavras[0].lower() == "key" and len(palavras) == 1:
                self.levantaErro(f"You can't have a entity atribute named 'key' in {self.linhaAtual}")
            if len(palavras) > 2 and palavras[0].lower() != 'key':
                self.whiteSpaceError(palavras)
            elif len(palavras) > 1 and palavras[0].lower() != 'key' and palavras[1][0] != '[':
                self.whiteSpaceError(palavras)
            elif palavras[0].lower() == "key":
                contKeys+=1
            
            if (len(palavras) > 1 and palavras[0].lower() == 'key' and palavras[1][0] == '[') or '[' in palavras[0]:
                self.levantaErro(f"Invalid cardinality identifier in {self.linhaAtual}")


            if contKeys > 1:
                self.levantaErro(f"You can't have more than one key identifier in {self.linhaAtual} line {self.numeroLinha}")
                
        
    
    def whiteSpaceError(self, palavras):
            self.levantaErro(f"Whitespace invalid in {self.linhaAtual}, line {self.numeroLinha}")
          
    

                    


    def checaCardinalidade(self, linha):
        for argumento in linha.split(','):
            palavras = argumento.strip().split(' ')
            for palavra in palavras:
                if palavra[0] == '[':
                    if not self.cardinalidadeCorreta(palavra):
                        self.levantaErro(f"Wrong cardinality in {palavra}, line: {self.linhaAtual}")
                        

    def cardinalidadeCorreta(self, cardinalidade):
        return cardinalidade.lower() in ('[0:1]', '[1:1]', '[0:n]', '[1:n]')
    

    def checaArgumentoGrande(self, linha, type):
        for argumento in linha.split(','):
            palavras = argumento.strip().split(' ')
            if (len(palavras) > 3 and type == "Entity") or (len(palavras) > 2 and type == "Relation"):
                self.levantaErro(f"Too big entry in {argumento}, line {self.numeroLinha}")
    

    def checaArgumentos(self, linha):
        if len(linha.split(',')) < 3:
            self.levantaErro(f"Few arguments in {self.linhaAtual}")
        elif len(linha.split(',')) > 3:
            self.levantaErro(f"Too many arguments in {self.linhaAtual}")


                

    def criaEntidade(self, linha):
        self.listaParametros = []
        for parametro in linha.split(','):
            self.listaParametros.append(parametro.strip())
        return entity.Entidade(self.listaParametros)
    


    def defineRelacionamento(self, argumentos):
        self.checaRelacionamentoVazio(argumentos)
        self.checaNome(argumentos, "Relation")

        self.checaArgumentoGrande(argumentos, "Relation")
        self.checaArgumentos(argumentos)
        self.checaEntidades(argumentos)
        self.modelo.adicionaRelacionamento(self.criaRelacionamento(argumentos))
    

    def checaRelacionamentoVazio(self, argumentos):
        if argumentos == '':
            self.levantaErro(f"Relation is empty in line {self.numeroLinha}")
        self.checaArgumentoVazio(argumentos)
    

    def checaEntidades(self, argumentos):
        vet = argumentos.split(',')[1:]

        for it in vet:
            palavras = it.strip().split(' ')
            self.avaliaEntidade(palavras[0])
            if len(palavras) == 2:
                self.avaliaCardinalidade(palavras[1])
            elif len(palavras) < 2:
                self.levantaErro(f"No cardinality in {palavras[0]} line: {self.linhaAtual}")
            elif len(palavras) > 2:
                self.levantaErro(f"Too many arguments in {palavras[0]} line: {self.linhaAtual}")
            
            
              
    

    def avaliaEntidade(self, entidade):
        entidade = entidade[0].upper() + entidade[1:].lower()
        for entidadeIndex in self.modelo.getEntidades():
            if entidadeIndex.getNome() == entidade:
                return
        self.levantaErro(f"Entity name {entidade} not exist in {self.linhaAtual}, line {self.numeroLinha}")
    

    def avaliaCardinalidade(self, cardinalidade):
        if cardinalidade.upper() not in ('[1:1]', '[1:N]', '[N:N]', '[0:1]', '[0:N]'):
            self.levantaErro(f"Invalid cardinality in {self.linhaAtual}, line {self.numeroLinha}")
            
    
    def criaRelacionamento(self, argumentos):
        vet = []
        for item in argumentos.split(','):
            vet.append(item.strip())
        return relation.Relation(vet)
    

    def levantaErro(self, erro):
        print(erro)
        1/0
    

    def defineAtributacao(self, argumentos):
        self.validaRelacionamento(argumentos)
        self.validaAtributos(argumentos)
        self.enviaAtributacao(argumentos)

    
    def validaRelacionamento(self, argumentos):
        if argumentos == '':
            self.levantaErro(f"Empty attribute in {self.linhaAtual}")
        nomeRelacionamento = argumentos.split(',')[0]
        nomeRelacionamento = nomeRelacionamento[0].upper() + nomeRelacionamento[1:].lower()
        for relacionamento in self.modelo.getRelacionamentos():
            if relacionamento.getNome() == nomeRelacionamento and relacionamento.getMuitoParaMuitos():
                return
            elif relacionamento.getNome() == nomeRelacionamento and not relacionamento.getMuitoParaMuitos():
                self.levantaErro(f"The relation {argumentos.split(',')[0]} is not N:N --> N:N cardinality")
        self.levantaErro(f"The relation {argumentos.split(',')[0]} is not definied.")

    def validaAtributos(self, argumentos):

        self.checaKey(argumentos)
        self.checaArgumentosVazios(argumentos)

        self.checaCardinalidade(argumentos)
        for argumento in argumentos.split(',')[1:]:
            if len(argumento.split(' ')) > 3 or len(argumento) == 0:
                print(len(argumento), argumento)
                self.levantaErro(f"Wrong entry in {argumento} line {self.linhaAtual}.")
            

    def checaArgumentosVazios(self, argumentos):
        for argumento in argumentos.split(','):
            if argumento.strip() == '':
                self.levantaErro(f"Empty attribute entry in: {self.linhaAtual}")

        

    def enviaAtributacao(self, argumentos):
        relacionamentoAtual = argumentos.split(',')[0]
        relacionamentoAtual = relacionamentoAtual[0].upper() + relacionamentoAtual[1:].lower()
        for relacionamento in self.modelo.getRelacionamentos():
            if relacionamento.getNome() == relacionamentoAtual:
                relacionamento.setAtributos(argumentos.split(',')[1:])
            
            
# parser = Parser(['entity(cliente, key cpf [1:1] , nome [1:1], a)', 'Entity(Produto, key id [1:N], nome, valor)', 'Relation(Compra, cliente [1:N], Produto [1:N])'])
# parser.traduzLinhas()

# for entidade in parser.modelo.getEntidades():
#     print(entidade.getNome())
# for relacionamento in parser.modelo.getRelacionamentos():
#     print(relacionamento.getNome())