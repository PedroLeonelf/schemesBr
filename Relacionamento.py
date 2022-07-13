#['Compra', 'key Cliente [1:N]', 'Produto [1:N]')]
import Atributo
class Relation:
    
    def __init__(self, argumentos):
        self.nome = argumentos[0].title()
        self.entidadesRelacionadas = []
        self.atributos = []
        entidades_a_ser_relacionadas = argumentos[1:]
        for entidade in entidades_a_ser_relacionadas:
            parametros = entidade.split(' ')
            if len(parametros) == 2:
                self.entidadesRelacionadas.append(EntidadeRelacionada(parametros[0], parametros[1]))
            elif len(parametros) == 3:
                self.entidadesRelacionadas.append(EntidadeRelacionada(parametros[1], parametros[2], True))
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
    
    def setAtributo(self, atributo):
        self.atributos.append(Atributo.Atributo(atributo))
    
    def getAtributos(self):
        return self.atributos
    
    def getCardinalidades(self):
        vect = []
        for entidade in self.entidadesRelacionadas:
            vect.append(entidade.getCardinalidade())
        return vect
            

class EntidadeRelacionada:
    def __init__(self, nome, cardinalidade, key = False):
        self.nome = nome[0].upper() + nome[1:].lower()
        self.cardinalidade = cardinalidade
        self.key = key
        
    def getNome(self):
        return self.nome
    
    def getCardinalidade(self):
        return self.cardinalidade
    
    def getKey(self):
        return self.key


relacionamento = Relation(['Compra', 'key Cliente [1:1]', 'Produto [1:N]'])
print(relacionamento.getEntidadesRelacionadas()[1].getKey())



