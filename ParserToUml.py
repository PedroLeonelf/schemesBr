from pathlib import Path



class ParserToUml:
    
    def __init__(self, modelo):
        self.model = modelo
        self.inicializateArchive()
        self.fileLocation = "content/text_file.txt"
        self.fixNonAlphaNumeric()
        self.translateToUml()
        self.writeUmlText()
    
    def inicializateArchive(self):
        myfile = Path('content/text_file.txt')
        myfile.touch(exist_ok=True)

        f = open(myfile)
        f.close()

    def translateToUml(self):
        self.text = []
        self.translateEntities(self.model.getEntidades())
        self.translateRelationships(self.model.getRelacionamentos())
        # print(self.text)
    
    def writeUmlText(self):
        with open(self.fileLocation, "w") as file:
            file.write("allowmixing\n")
            file.write("@startuml\n")
        with open(self.fileLocation, "a") as file:
            for linha in self.text:
                file.write(f"{linha}\n")
            file.write("@enduml")
    
    def fixNonAlphaNumeric(self):
        for entidade, relacionamento in zip(self.model.getEntidades(), self.model.getRelacionamentos()):
            if '-' in entidade.getNome():
                entidade.setNome(entidade.getNome().replace('-', '_'))
            if '-' in relacionamento.getNome():
                relacionamento.setNome(relacionamento.getNome().replace('-', '_')) 
                


    def translateEntities(self, entities):
        for entity in entities:
            if entity.draw:
                self.text.append(f"Entity {entity.getNome()}" + '{')
                self.translateAtributes(entity.getAtributos())
                self.text.append("}")
            if entity.especializacao != []:
                for special in entity.especializacao:
                    self.text.append(f'usecase {special}')
                    self.text.append(f"{entity.getNome()} --> {special}")

    
        
    

    def translateAtributes(self, atributes):
        keyAtribute = self.getKeyAtribute(atributes=atributes)
        if keyAtribute != None:
            if keyAtribute.getCardinalidade() != None:
                self.text.append(f"+ {keyAtribute.getNome()} {keyAtribute.getCardinalidade()}\n--")
            else:
                self.text.append(f"+ {keyAtribute.getNome()}\n--")
        for atribute in atributes:
            if atribute != keyAtribute:
                if atribute.getCardinalidade() != None:
                    self.text.append(f"- {atribute.getNome()} {atribute.getCardinalidade()}")
                elif atribute.getCardinalidade() == None:
                    self.text.append(f"- {atribute.getNome()}")
                
    
    def getKeyAtribute(self, atributes):
        for atribute in atributes:
            if atribute.isIdentifier():
                return atribute
    

    def translateRelationships(self, relationships):
        for relation in relationships:
            if relation.getMuitoParaMuitos():
                self.text.append(f"Class {relation.getNome()} "+ "{")
                self.getRelationAttributes(relation)
                self.text.append('}')
            else:
                self.text.append(f"package {relation.getNome()} <<Cloud>> " + '{\n' + '}')
            self.translateRelatedEntities(relation.getEntidadesRelacionadas(), relation.getNome())
    
    def getRelationAttributes(self, relation):
        if relation.getAtributos() == []:
            return 
        self.translateAtributes(relation.getAtributos())

        

    def translateRelatedEntities(self, relatedEntities, relationName):
        if len(relatedEntities) == 2:
            self.text.append(f"{relatedEntities[0].getNome()} {self.getCardinalityArrow(relatedEntities[0].getCardinalidade().upper())}> {relationName} : {relatedEntities[0].getCardinalidade().upper()}")
            self.text.append(f"{relationName} <{self.getInversedCardinalityArrow(relatedEntities[1].getCardinalidade().upper())} {relatedEntities[1].getNome()} : {relatedEntities[1].getCardinalidade().upper()}")

    def getCardinalityArrow(self, cardinality):
        if cardinality == '[0:1]':
            return '|o-'
        elif cardinality == '[1:1]':
            return '||-'
        elif cardinality == '[0:N]':
            return '}o-'    
        elif cardinality == '[1:N]':
            return '}|-'
    
    def getInversedCardinalityArrow(self, cardinality):
        if cardinality == '[0:1]':
            return '|o-'[::-1]
        elif cardinality == '[1:1]':
            return '||-'[::-1]
        elif cardinality == '[0:N]':
            return '-o{'    
        elif cardinality == '[1:N]':
            return '-|{'



            