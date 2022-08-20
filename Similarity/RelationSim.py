from Similarity.Utility import *

def relationsSimilarity(relations1, relations2, scores) -> dict:
    dict = {}
    for relation1 in relations1:
        for relation2 in relations2:
            dict[f'{relation1.getNome().lower()}-{relation2.getNome().lower()}'] = compareRelations(relation1, relation2, scores)
    return dict

def compareRelations(relation1, relation2, entitiesScore) -> float:
    name1, name2 = relation1.getNome(), relation2.getNome()
    nameSim = mainComparatorStrings(name1, name2)
    if relation1.getAtributos() == []: relation1.setAtributo('none')
    if relation2.getAtributos() == []: relation2.setAtributo('none')
    attribt = AttributesSimiliarity(relation1, relation2)
    cardinaliScore = checkCardinality(relation1, relation2)
    neighboorScore = checkNeighborScore(relation1, relation2, entitiesScore)

    return truncate((nameSim + attribt + cardinaliScore + neighboorScore) / 4)
    
def checkCardinality(relation1, relation2) -> float:
    vect = []
    for cardinality in relation1.getCardinalidades():
        if cardinality in relation2.getCardinalidades():
            vect.append(1)
            continue
        vect.append(0)
    return sum(vect)/len(vect)


def checkNeighborScore(relation1, relation2, scores) -> float:
    entities1,entities2 = relation1.getEntidadesRelacionadas(), relation2.getEntidadesRelacionadas()
    vect = []
    for entity in entities1:
        vect.append(neighboorsEntityScore(entity, entities2, scores))
    return sum(vect)/len(vect)

def neighboorsEntityScore(entity1, entities2, scores) -> float:
    vect = []
    for entity2 in entities2:
        vect.append(scores[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] * 0.8 + 0.2 * (entity1.getKey() == entity2.getKey()))
    return max(vect)



