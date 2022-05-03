#['Compra', 'Cliente [1:N]', 'Produto [1:N]')]
import Atributo
class Relation:
    
    def __init__(self, argumentos):
        self.nome = argumentos[0][0].upper() + argumentos[0][1:].lower()
        self.entidadesRelacionadas = []
        self.atributos = []
        entidades_a_ser_relacionadas = argumentos[1:]
        for entidade in entidades_a_ser_relacionadas:
            parametros = entidade.split(' ')
            self.entidadesRelacionadas.append(EntidadeRelacionada(parametros[0], parametros[1]))
        self.checaMuitosParaMuitos()
        
    def getNome(self):
        return self.nome
    
    def getEntidadesRelacionadas(self):
        return self.entidadesRelacionadas
    
    def getMuitoParaMuitos(self):
        return self.muitoParaMuitos
    
    def checaMuitosParaMuitos(self):
        cont = 0
        self.muitoParaMuitos = False
        for entidadeRelacionada in self.entidadesRelacionadas:
            if entidadeRelacionada.getCardinalidade().upper() == '[1:N]':
                cont+=1
            if cont == 2:
                self.muitoParaMuitos = True
                return
    
    def setAtributos(self, atributos):
        for atr in atributos:
            self.atributos.append(Atributo.Atributo(atr.strip()))
    
    def setNome(self, nome):
        self.nome = nome
    
    def getAtributos(self):
        return self.atributos

            

class EntidadeRelacionada:
    def __init__(self, nome, cardinalidade):
        self.nome = nome[0].upper() + nome[1:].lower()
        self.cardinalidade = cardinalidade
        
    def getNome(self):
        return self.nome
    
    def getCardinalidade(self):
        return self.cardinalidade


relacionamento = Relation(['Compra', 'Cliente [1:1]', 'Produto [1:N]'])



