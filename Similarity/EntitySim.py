from Similarity.Utility import *




def entitiesSimiliarity(entities1, entities2) -> dict:
    dict = {}

    for entity1 in entities1:
        for entity2 in entities2:
            dict[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] = entitySimiliarity(entity1, entity2)
    return dict

def entitySimiliarity(entity1, entity2) -> float:

    name1, name2 = entity1.getNome().lower(), entity2.getNome().lower()
    nameSim = mainComparatorStrings(name1, name2)
    attributeSim = AttributesSimiliarity(entity1, entity2)
    return truncate(max(nameSim,attributeSim))



