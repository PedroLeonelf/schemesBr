#("Aluno", "key cpf", "nome")
import Atributo as atribute

class Entidade:
    def  __init__(self, parametros):

        self.nomeEntidade = parametros[0].title()
        self.atributos = []
        self.especializacao = []
        self.relacionamentos = []
        atributosParametrizados = parametros[1:]
        self.draw = True
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
    
    def setRelacionamento(self, relacionamento):
        self.relacionamentos.append(relacionamento)
    
    def getRelacionamentos(self):
        return self.relacionamentos

    def getSpecialization(self):
        return self.especializacao
    
    def setSpecialization(self, especializacao):
        self.especializacao.append(especializacao)  

    def __str__(self):
        return f'Entity:{self.nomeEntidade}'
    


# entidade = Entidade(["Aluno", "key cpf", "nome"])
# for atributo in entidade.getAtributos():
#     print(atributo.isIdentifier())



