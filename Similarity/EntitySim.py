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
        
    def nameSimilarity(self,name1, name2, entity1, entity2):
        entityNamesSim = mainComparatorStrings(name1, name2)
        if entity1.getSpecialization() == [] and entity2.getSpecialization() == []:
            return entityNamesSim
        elif entity1.getSpecialization() != [] and entity1.getSpecialization() != []:
            return max(self.getBiggerScoreFromSpecializations(entity1, entity2), self.getBiggerScoreFromName(entity1, name2), self.getBiggerScoreFromName(entity2, name1), entityNamesSim)
        elif entity1.getSpecialization() != []:
            return max(self.getBiggerScoreFromName(entity1, name2), entityNamesSim)
        elif entity2.getSpecialization() != []:
            return max(self.getBiggerScoreFromName(entity2, name1), entityNamesSim)

    def getBiggerScoreFromSpecializations(self,entity1, entity2):
        bigger = 0
        for specialization1 in entity1.getSpecialization():
            for specialization2 in entity2.getSpecialization():
                actual = mainComparatorStrings(specialization1, specialization2)
                bigger = actual if actual > bigger else bigger
        return bigger

    def getBiggerScoreFromName(self,entity, name):
        bigger = 0
        for specialization in entity.getSpecialization():
            actual = mainComparatorStrings(specialization, name)
            bigger = actual if actual > bigger else bigger
        return bigger


