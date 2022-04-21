#key cpf [1:1]
#nome
#telefones [1:N]
class Atributo:
    def __init__(self, parametros):
        parametros = parametros.split(' ')
        self.avaliaKey(parametros)
        self.defineNome(parametros)
        self.defineCardinalidade(parametros)
    
    def avaliaKey(self, parametros):
        if parametros[0] == 'key':
            self.key = True
        else:
            self.key = False
    
    def defineNome(self, parametros):
        if self.key:
            self.nome = parametros[1]
        else:
            self.nome = parametros[0]
        
    def defineCardinalidade(self, parametros):
        for item in parametros:
            if item[0] == '[':
                self.cardinalidade = item
                return
        self.cardinalidade = None
    
    
    def getNome(self):
        return self.nome
    
    def isIdentifier(self):
        return self.key
    
    def getCardinalidade(self):
        return self.cardinalidade


