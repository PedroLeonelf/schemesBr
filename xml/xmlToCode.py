from tokenize import String
from turtle import position
from typing import Dict
import xml.etree.ElementTree as ET


class xmlToCode:
    def __init__(self) -> None:
        tree = ET.parse('xml/xmlteste.xml')
        self.root = tree.getroot()
        self.entities = []
        self.relationships = []
        self.attributes = []
        self.connections = []
        self.cardinalities = []

    # nomes das entidades
    def getentities(self) -> None:
        for entity in self.root.iter('Entidade'): 
            item = entity.find('Texto')
            position = entity.find('Bounds')
            self.entities.append({'Name':item.text.replace(' ', '_'), 'id' : entity.attrib['ID'], 'attributes' : [], 'position' : [position.attrib['Left'], position.attrib['Top']]})

    # nomes dos relacionamentos
    def getRelationships(self) -> None:
        for relationship in self.root.iter('Relacionamento'):
            for item in relationship.iter('Texto'):
                self.relationships.append({'Name' : item.text.replace(' ', '_'), 'id' : relationship.attrib['ID'], 'entities' : []})

    # atributos valor e identificador 
    def getAttributes(self) -> None:
        for attrb in self.root.iter('Atributo'):
            for itemName, itemKey in zip(attrb.iter('Texto'), attrb.iter('Identificador')):
                self.attributes.append({'Name' : itemName.text.replace(' ', '_'), 'key' : itemKey.attrib['Valor'], 'id' : attrb.attrib['ID']})

    # pega os atributos pelo nome 
    def getAttributeByName(self, name) -> Dict:
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
        

    # conexoes
    def getConnections(self) -> None:
        for connection in self.root.iter('Ligacao'):
            for item in connection.iter('Ligacoes'):
                
                self.defineConnection(item.attrib['PontaA'], item.attrib['PontaB'])

    # printar conexoes
    def printConnections(self) -> None:
        for connection in self.connections:
            print(connection)
    
    # definir conexoes
    def defineConnection(self, pointA, pointB) -> None:
        self.connections.append({'PontaA' : self.getConnection(pointA), 'typeA' : self.getType(pointA), 'PontaB' : self.getConnection(pointB), 'typeB' : self.getType(pointB)})

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
            
        


obj = xmlToCode()
obj.getentities()
obj.getRelationships()
obj.getAttributes()
obj.getConnections()
obj.linkEntities()
obj.linkRelationships()
obj.getConnections()
obj.getCardinalities()
obj.printCardinalities()
obj.printEntities()
obj.printRelationships()