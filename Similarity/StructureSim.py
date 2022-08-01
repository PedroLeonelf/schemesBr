from Similarity.Utility import average, truncate

def modelStructureSim(model1, model2, entitiesScores, relationScores) -> dict:
    dict = {}
    for entity1 in model1.getEntidades():
        for entity2 in model2.getEntidades():
            dict[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] = entityStructureSim(entity1, entity2, entitiesScores, relationScores)
    return dict

def entityStructureSim(entity1, entity2, entitiesScores, relationScores) -> float:
    value = 0
    relationScore = getRelationScores(entity1, entity2, relationScores)
    entityNeighboorScore = neighboorSim(entity1, entity2, entitiesScores)

    value = (relationScore + entityNeighboorScore) / 2
    return truncate(value)

def getRelationScores(entity1, entity2, scores) -> float:
    vect = []
    for relation1 in entity1.getRelacionamentos():
        tmp = []
        for relation2 in entity2.getRelacionamentos():
            
            tmp.append(scores[f'{relation1.lower()}-{relation2.lower()}'])
        
        vect.append(max(tmp))
    
    return average(vect)


def neighboorSim(entity1, entity2, scores) -> float:
    relations1, relations2 = entity1.getRelacionamentos(), entity2.getRelacionamentos()
    vect = []
    for relation in relations1:
        vect.append(relationsNeighboorSim(relation, relations2, scores))
    return average(vect)

def relationsNeighboorSim(relation, relations2, scores)->float:
    vect = []
    name1 = relation.lower()
    for relation2 in relations2:
        key = f'{name1}-{relation2.lower()}'
        print(key, scores.keys())
        if key in scores.keys():
            vect.append(scores[key])
    return max(vect)