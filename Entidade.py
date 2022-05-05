#("Aluno", "key cpf", "nome")
import Atributo as atribute

class Entidade:
    def  __init__(self, parametros):
        self.nomeEntidade = parametros[0][0].upper() + parametros[0][1:].lower()
        self.atributos = []
        self.especializacao = []
        atributosParametrizados = parametros[1:]
        for atributo in atributosParametrizados:
            self.atributos.append(atribute.Atributo(atributo))
        
    def getAtributos(self):
        return self.atributos
        
    def getNome(self):
        return self.nomeEntidade
    
    def setNome(self, nome):
        self.nomeEntidade = nome
    
    def setAtributo(self, atributo):
        self.atributos.append(atribute.Atributo(atributo))
    
    def setAtributos(self, atributos):
        for atributo in atributos:
            self.setAtributo(atributo)
    

    def getSpecialization(self):
        return self.especializacao
    
    def setSpecialization(self, especializacao):
        self.especializacao.append(especializacao)  

    def __str__(self):
        return f'Entity:{self.nomeEntidade}'
    


# entidade = Entidade(["Aluno", "key cpf", "nome"])
# for atributo in entidade.getAtributos():
#     print(atributo.isIdentifier())



