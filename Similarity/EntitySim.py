from Similarity.Utility import *


class EntitySim:
    def __init__(self) -> None:
        self.scoreAttributes = {}
        self.scoreName = {}

    def entitiesSimiliarity(self,entities1, entities2) -> dict:
        dict = {}
        for entity1 in entities1:
            for entity2 in entities2:
                dict[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] = self.entitySimiliarity(entity1, entity2)
        return dict

    def entitySimiliarity(self,entity1, entity2) -> float:
        name1, name2 = entity1.getNome().lower(), entity2.getNome().lower()
        nameSim = self.nameSimilarity(name1, name2, entity1, entity2)
        attributeSim = AttributesSimiliarity(entity1, entity2)
        self.scoreAttributes[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] = attributeSim
        self.scoreName[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] = nameSim
        return truncate(max(nameSim,attributeSim))
        # retorna mais alto entre a similaridade de nome e atributos

    def nameSimilarity(self, name1, name2, entity1, entity2) -> float:
        lst1 = [name1] + entity1.especializacao
        lst2 = [name2] + entity2.especializacao
        return self.mostBiggerScore(lst1, lst2)

    
    def mostBiggerScore(self, lst1, lst2) -> float:
        bigger = 0
        for item1 in lst1:
            for item2 in lst2:
                numberGet = mainComparatorStrings(item1, item2)
                if numberGet > bigger:
                    bigger = numberGet
        return bigger




