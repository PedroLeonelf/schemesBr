class Nodo:
    def __init__(self,valor):
        self.valor = valor
        self.arestas = []
    
    def __str__(self):
        return f'{self.valor}'
    
    def getArestas(self):
        return self.arestas
    
    def adicionaAresta(self, aresta):
        self.arestas.append(aresta)
    
    def getValor(self):
        return self.valor

    

class Aresta:
    def __init__(self, nodo1, nodo2, valor):
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.valor = valor
    
    def __str__(self):
        return f'{self.nodo1} --> {self.nodo2}'
    
    def getNodo(self):
        return self.nodo2
    
    def getValor(self):
        return self.valor
    
class Grafo:
    def __init__(self, primeiroNo = None):
        self.primeiroNo = primeiroNo
        self.nodos = []
    

    def adiciona(self, valor):
        no = Nodo(valor)
        if self.primeiroNo == None:
            self.primeiroNo = no
        self.nodos.append(no)
    

    def getNo(self, valor):
        for no in self.nodos:
            if valor == no.getValor():
                return no
        return None
    
    def getNoPorNome(self, nome):
        for no in self.nodos:
            if no.getValor().getNome().lower() == nome.lower():
                return no

    def getNos(self):
        return self.nodos


    def adicionaAresta(self, nodo1, nodo2, valor1, valor2):
        no1, no2 = self.getNo(nodo1), self.getNo(nodo2)
        if no1 == None or no2 == None:
            no1, no2 = self.getNoPorNome(nodo1), self.getNoPorNome(nodo2)
        
        if no1 == None or no2 == None:
            print(f'Erro nos nomes da relação entre:{nodo1} e {nodo2}')
            exit(-1)
        no1.adicionaAresta(Aresta(no1, no2, valor1))
        no2.adicionaAresta(Aresta(no2, no1, valor2))
    

    def getNoPorEntidade(self, nomeEntidade):
        for no in self.nodos:
            if no.getValor().getNome() == nomeEntidade:
                return no