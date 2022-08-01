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
        nameSim = mainComparatorStrings(name1, name2)
        attributeSim = AttributesSimiliarity(entity1, entity2)
        self.scoreAttributes[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] = attributeSim
        self.scoreName[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] = nameSim
        return truncate(max(nameSim,attributeSim))
        


