import xml.etree.ElementTree as ET


class xmlToCode:
    def __init__(self) -> None:
        tree = ET.parse('xml/xmlteste.xml')
        self.root = tree.getroot()
        self.entityName = []
        self.relationshipNames = []
        self.attributes = []
        self.connections = []

    # nomes das entidades
    def getEntityNames(self) -> None:
        for entity in self.root.iter('Entidade'): 
            for item in entity.iter('Texto'):
                self.entityName.append(item.text)

    # nomes dos relacionamentos
    def getRelationshipNames(self) -> None:
        for relationship in self.root.iter('Relacionamento'):
            for item in relationship.iter('Texto'):
                self.relationshipNames.append(item.text)

    # atributos valor e identificador 
    def getAttributes(self) -> None:
        for attrb in self.root.iter('Atributo'):
            for itemName, itemKey in zip(attrb.iter('Texto'), attrb.iter('Identificador')):
                self.attributes.append({'name' : itemName.text, 'key' : itemKey.attrib['Valor']})
    
    # conexoes
    def getConnections(self) -> None:
        for connection in self.root.iter('Ligacao'):
            for item in connection.iter('Ligacoes'):
                self.conecctions.append({'first' : item.attrib['PontaA'], 'second' : item.attrib['PontaB']})

            
    



obj = xmlToCode()

obj.getConnections()