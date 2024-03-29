import xml.etree.ElementTree as ET



class xmlToCode:
    def __init__(self) -> None:
        self.fileName = 'xml/translatedText.txt'
        self.entities = []
        self.relationships = []
        self.attributes = []
        self.connections = []
        self.cardinalities = []
    
    def translateFile(self, path):
        tree = ET.parse(path, parser = ET.XMLParser(encoding = 'iso-8859-5'))
        self.root = tree.getroot()
        self.initializeGets()
    
    def initializeGets(self) -> None:
        self.getSpecializations()
        self.getEntities()
        self.getRelationships()
        self.getAttributes()
        self.getConnections()
        self.linkEntities()
        self.linkRelationships()
        self.getConnections()
        self.getCardinalities()
        self.linkCardinalities()
        self.linkSpecializations()
       
        self.translate()

    # nomes das entidades
    def getEntities(self) -> None:
        for entity in self.root.iter('Entidade'): 
            item = entity.find('Texto')
            position = entity.find('Bounds')
            self.entities.append({'specializationLeader' : -1,'Name':item.text.replace(' ', '_'), 'id' : entity.attrib['ID'], 'attributes' : [], 'position' : [position.attrib['Left'], position.attrib['Top']], 'specializations' : [], 'cardinalities': [0,0]})

    # nomes dos relacionamentos
    def getRelationships(self) -> None:
        for relationship in self.root.iter('Relacionamento'):
            for item in relationship.iter('Texto'):
                self.relationships.append({'Name' : item.text.replace(' ', '_'), 'id' : relationship.attrib['ID'], 'entities' : [], 'cardinalities' : []})

    # atributos valor e identificador 
    def getAttributes(self) -> None:
        for attrb in self.root.iter('Atributo'):
            for itemName, itemKey in zip(attrb.iter('Texto'), attrb.iter('Identificador')):
                self.attributes.append({'Name' : itemName.text.replace(' ', '_'), 'key' : itemKey.attrib['Valor'], 'id' : attrb.attrib['ID']})

    # pega os atributos pelo nome 
    def getAttributeByName(self, name) -> dict:
        for attribute in self.attributes:
            if attribute['Name'] == name:
                return attribute
    
    # cardinalidades seus valores e posições
    def getCardinalities(self) -> None:
        for cardinality in self.root.iter('Cardinalidade'):
            item = cardinality.find('Card')
            position = cardinality.find('Bounds')
            self.cardinalities.append({'value' : self.getCardinalityValue(item.attrib['Valor']), 'id' : cardinality.attrib['ID'], 'position' : [position.attrib['Left'], position.attrib['Top']]})
    
    def getCardinalityValue(self, value) -> str:
        if value == '0':
            return '1:1'
        elif value == '1':
            return '0:1'
        elif value == '2':
            return '1:N'
        elif value == '3':
            return '0:N'
    

    # especializações
    def getSpecializations(self) -> None:
        self.specializations = []
        for specialization in self.root.iter('Especializacao'):
            position = specialization.find('Bounds')
            self.specializations.append({'id':specialization.attrib['ID'], 'position' : [position.attrib['Left'], position.attrib['Top']]})
        
      
        
    


    # conexoes
    def getConnections(self) -> None:
        for connection in self.root.iter('Ligacao'):
            for item in connection.iter('Ligacoes'):
                self.defineConnection(item.attrib['PontaA'], item.attrib['PontaB'])
        self.connections = [dict(t) for t in {tuple(d.items()) for d in self.connections}] # avoid duplicates

    # printar conexoes
    def printConnections(self) -> None:
        for connection in self.connections:
            print(connection)
    
    # definir conexoes
    def defineConnection(self, pointA, pointB) -> None:
        self.connections.append({'PontaA' : self.getConnection(pointA), 'typeA' : self.getType(pointA), 'PontaB' : self.getConnection(pointB), 'typeB' : self.getType(pointB)})
  
    def defineSpecializations(self) -> None:
        for entity in self.entities:
            if entity['specializationLeader'] == 1:
                self.findSpecializations(entity)
    
    def findSpecializations(self, entityLeader) -> None:
        for entity in self.entities:
            if entity['specializationLeader'] == 0 and entity['entityLeader'] == entityLeader['Name']:
                entityLeader['attributes'].extend(entity['attributes'])
                entityLeader['specializations'].append(entity['Name'])
    



    # definir uma conexao
    def getConnection(self, point) -> str:
        for entity in self.entities:
            if entity['id'] == point:
                return entity['Name']
        for relationship in self.relationships:
            if relationship['id'] == point:
                return relationship['Name']  
        for attribute in self.attributes:
            if attribute['id'] == point:
                return attribute['Name']
        for special in self.specializations:
            if special['id'] == point:
                return special['id']


    
    # definir tipo de conexao
    def getType(self, point) -> str:
        for entity in self.entities:
            if entity['id'] == point:
                return 'Entity'
        for relationship in self.relationships:
            if relationship['id'] == point:
                return 'Relationship'
        for attribute in self.attributes:
            if attribute['id'] == point:
                return 'Attribute'
        for special in self.specializations:
            if special['id'] == point:
                return 'Specialization'
    
    # linkar entidades
    def linkEntities(self) -> None:
        for connection in self.connections:
            if connection['typeA'] == 'Entity' and connection['typeB'] == 'Attribute' or connection['typeA'] == 'Attribute' and connection['typeB'] == 'Entity':
                self.linkEntityAttribute(connection)
    
    def linkEntityAttribute(self, connection) -> None:
        entity = connection['PontaA'] if connection['typeA'] == 'Entity' else connection['PontaB']
        attribute = connection['PontaA'] if connection['typeA'] == 'Attribute' else connection['PontaB']
        for item in self.entities:
            if item['Name'] == entity:
                item['attributes'].append(self.getAttributeByName(attribute))

    def linkRelationships(self) -> None:
        for connection in self.connections:
            if connection['typeA'] == 'Relationship' and connection['typeB'] == 'Entity' or connection['typeA'] == 'Entity' and connection['typeB'] == 'Relationship':
                self.linkRelationshipEntities(connection)    
        
    def linkRelationshipEntities(self, connection) -> None:
        
        relationship = connection['PontaA'] if connection['typeA'] == 'Relationship' else connection['PontaB']
        entity = connection['PontaA'] if connection['typeA'] == 'Entity' else connection['PontaB']
        for item in self.relationships:
            if item['Name'] == relationship:
                item['entities'].append(entity)
    
    def returnEntitySpecial(self, entityName):
        for entity in self.entities:
            if entity['Name'] == entityName and entity['specializationLeader'] == 0:
                return entity['entityLeader']
        return entityName

    
    def linkCardinalities(self) -> None:
        
        
        for entityLink in self.entities:
            self.linkCardinality(entityLink)
    
    def linkCardinality(self, entityLink) -> None:
        minorDiff = self.getDiffPosition(self.cardinalities[0], self.entities[0])
        for cardinality in self.cardinalities:
            
            for entity in self.entities:
                diff = self.getDiffPosition(cardinality, entity)
                if diff < minorDiff: 
                    minorDiff = diff
                    entityLink = entity
          
            self.defineCardinalityInRelationship(entityLink, cardinality)
    
    def linkSpecializations(self) -> None:
        connections = []
        for connection in self.connections:
            if connection['typeA'] == 'Specialization' and connection['typeB'] == 'Entity' or connection['typeA'] == 'Entity' and connection['typeB'] == 'Specialization':
                self.defineSpecialization(connection)
                connections.append(connection)
        self.linkEntitySpecializations(connections)
        self.entities = sorted(self.entities, key=lambda d: d['specializationLeader'], reverse=True)
        self.defineSpecializations() 
    
    def linkEntitySpecializations(self, connections):
        for connection in connections:
            entityName = connection['PontaA'] if connection['typeA'] == 'Entity' else connection['PontaB']
            self.markEntitySpecialization(entityName)
        

    def markEntitySpecialization(self, entityName):
        for entity in self.entities:
            if entity['Name'] == entityName and entity['specializationLeader'] == 0:
                entity['entityLeader'] = self.getEntityLeader(entity['specialId'])
    
    def getEntityLeader(self, entityId):
        for entity in self.entities:
            if entity['specialId'] == entityId and entity['specializationLeader'] == 1:
                return entity['Name']
    
    def defineSpecialization(self, connection) -> None:
        entity = connection['PontaA'] if connection['typeA'] == 'Entity' else connection['PontaB']
        specialId = connection['PontaA'] if connection['typeA'] == 'Specialization' else connection['PontaB']
        self.setEntityAsSpecial(entity, specialId)

    def setEntityAsSpecial(self, entityName, specialization) -> None:
        for entity in self.entities:
            if entity['Name'] == entityName and self.entityIsAbove(entity, specialization):
                entity['specializationLeader'] = 1
            elif entity['Name'] == entityName:
                entity['specializationLeader'] = 0
            entity['specialId'] = specialization
        


    def entityIsAbove(self, entity, specializationId) -> bool:
        specialization = self.findSpecialization(specializationId)
        specialPos = specialization['position'][1]
        entityPos = entity['position'][1]
        # print(specialPos, entityPos)
        return specialPos > entityPos
    
    def findSpecialization(self, id) -> dict:
        for special in self.specializations:
            if special['id'] == id:
                return special



    def defineCardinalityInRelationship(self, entity, cardinality) -> None:
        for relationship in self.relationships:
            # print(relationship['entities'], cardinality)    
            if entity['Name'] in relationship['entities']  and len(relationship['cardinalities']) < 2:
                relationship['cardinalities'].append(cardinality['value'])
                return
   
    

    def getDiffPosition(self, cardinality, entity) -> int:
        diff = abs(int(cardinality['position'][0]) - int(entity['position'][0])) + abs(int(cardinality['position'][1]) - int(entity['position'][1]))
        return diff
    
    def translate(self) -> None:
        with open(self.fileName, 'w') as file: None # cria ou esvazia o arquivo
        for entity in self.entities:
            self.translateEntity(entity)
        self.translateSpecializations()
        for relationship in self.relationships:
            self.translateRelationship(relationship)
    
    def translateEntity(self, entity) -> None:
        
        if entity['specializationLeader'] != 0:
            self.writeEntity(entity)

    
    def translateSpecializations(self) -> None:
        for entity in self.entities:
            if entity['specializationLeader'] == 1:
                self.writeSpecialization(entity)
                
    
    def writeSpecialization(self, entity):
        nameLeader = entity['Name']
        string = ''
        last = entity['specializations'][-1]
        for special in entity['specializations']:
            string += special
            if special != last:
                string += ', '
        with open(self.fileName, 'a') as file:
            file.write(f'specialization({nameLeader},{string})\n')

    def writeEntity(self, entity):
        name = entity['Name']
        if entity['attributes'] == []:
            with open(self.fileName, 'a') as file:
                file.write(f'entity({name})\n')
        else:
            attributes = self.parseAttributes(entity['attributes'])
            with open(self.fileName, 'a') as file:
                file.write(f'entity({name}, {attributes})\n')    
    
    def translateRelationship(self, relationship) -> None:
        name = relationship['Name']
        entitie1, entitie2 = relationship['entities'][0] , relationship['entities'][1]
        # print(relationship)
        cardinality1, cardinality2 = relationship['cardinalities'][0] , relationship['cardinalities'][1]
        
        with open(self.fileName, 'a') as file:
            file.write(f'relation({name}, {entitie1} [{cardinality1}], {entitie2} [{cardinality2}])\n')


    def parseAttributes(self, attributes) -> str:
        vect = ''
        for attribute in attributes:
            name = attribute['Name']
            vect += f'key {name}' if attribute['key'] == 'true' else name
            if attribute != attributes[-1]:
                vect += ', '
        return vect
            
        
    def printEntities(self) -> None:
        for entity in self.entities:
            print(entity)

    def printAttributes(self) -> None:
        for attribute in self.attributes:
            print(attribute)
    
    def printRelationships(self) -> None:
        for relationship in self.relationships:
            print(relationship)
    
    def printCardinalities(self) -> None:
        for cardinality in self.cardinalities:
            print(cardinality)
            
        


xml = xmlToCode()
xml.translateFile('xml/conceitual.xml')

# xml.printCardinalities()
# xml.printEntities()
# xml.printCardinalities()
# xml.printRelationships()
# xml.printConnections()