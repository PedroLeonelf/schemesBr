
from Similarity.Utility import average, truncate


alpha = 0.6
beta = 0.3
gama = 0.1

def defineFinalScore(scoreEntitties, scoreAttribute, scoreStructure, entidades) -> float:
    repeteadDic = integrateDics(scoreEntitties, scoreAttribute, scoreStructure)
    finalDict = getMostBiggerDictionaries(repeteadDic, entidades)
    return average(finalDict.values())


def integrateDics(nameDict, attributeDict, structureDict) -> dict:
    dict = {}
    for (k1,v1),(k2,v2),(k3,v3) in zip(nameDict.items(), attributeDict.items(), structureDict.items()):
        dict[k1] = calculateMedia(v1,v2,v3)
    return dict 

def calculateMedia(v1,v2,v3):
    vect = [v1,v2,v3]
    vect.sort()
    return truncate(vect[2] * alpha + vect[1] * beta + vect[0] * gama)

def getMostBiggerDictionaries(dic, entities) -> dict:
    dict = {}
    for entity in entities:
        entityName = entity.getNome().lower()
        vect = []        
        for k,v in dic.items():
            if  entityName == k.split('-')[0]:
                vect.append(v)
        dict[entityName] = max(vect)
    return dict 