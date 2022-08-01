
from Similarity.RelationSim import *
from Similarity.Utility import *
from Similarity.EntitySim import *
from Similarity.StructureSim import *
from Similarity.finalCalc import defineFinalScore
metaScore = 0.7
#-----------------------
entityScore = 0.6
nodeScore = 0.4
#-----------------------
cardinalityScore = 0.2
entityNodeScore = 0.8
#-----------------------
synonymScore = 1
attributeSimiliarity = True
english_text = False
utilizeSynonym = False

import time



def graphSimiliarity(modelo1, modelo2) -> float:

    inicio = time.time()
    
    entitySimObj = EntitySim()
    entitiesScores = entitySimObj.entitiesSimiliarity(modelo1.getEntidades(), modelo2.getEntidades())
    relationsScores = relationsSimilarity(modelo1.getRelacionamentos(), modelo2.getRelacionamentos(), entitiesScores)
    structureObj = Structure(modelo1, modelo2, entitiesScores, relationsScores)
    structureScore = structureObj.getScores()
    finalScore = defineFinalScore(entitySimObj.scoreName, entitySimObj.scoreAttributes, structureScore)
    print(finalScore)

    # return average(finalScore, len(graph1.getNos())) * 100
    
            
# def entitiesSimiliarity(graph1, graph2):
#     scores = []
#     for node1 in graph1.getNos():
#         for node2 in graph2.getNos():
#             scores.append(entitySimiliarity(node1.getValor(), node2.getValor()))
#     return scores




#################################################################################################
#name
#atribbutes
#first part ---------------------------------------------------------------------------------------------------
def entitySimiliarity(entity1, entity2): #first part 
    scoreList, scoreName, scoreAttributes = [entity1, entity2], 0, 0
    name1, name2 = entity1.getNome().lower().strip(), entity2.getNome().lower().strip()
    scoreName = nameSimilarity(name1, name2, entity1, entity2)
    scoreAttributes += AttributesSimiliarity(entity1, entity2)
    scoreList.append(round(scoreName,2))
    scoreList.append(round(scoreAttributes,2))
    scoreList.append(round((scoreName+scoreAttributes)/2,2)) 
    return scoreList

def nameSimilarity(name1, name2, entity1, entity2):
    entityNamesSim = mainComparatorStrings(name1, name2)
    if entity1.getSpecialization() == [] and entity2.getSpecialization() == []:
        return entityNamesSim
    elif entity1.getSpecialization() != [] and entity1.getSpecialization() != []:
        return max(getBiggerScoreFromSpecializations(entity1, entity2), getBiggerScoreFromName(entity1, name2), getBiggerScoreFromName(entity2, name1), entityNamesSim)
    elif entity1.getSpecialization() != []:
        return max(getBiggerScoreFromName(entity1, name2), entityNamesSim)
    elif entity2.getSpecialization() != []:
        return max(getBiggerScoreFromName(entity2, name1), entityNamesSim)

def getBiggerScoreFromSpecializations(entity1, entity2):
    bigger = 0
    for specialization1 in entity1.getSpecialization():
        for specialization2 in entity2.getSpecialization():
            actual = mainComparatorStrings(specialization1, specialization2)
            bigger = actual if actual > bigger else bigger
    return bigger

def getBiggerScoreFromName(entity, name):
    bigger = 0
    for specialization in entity.getSpecialization():
        actual = mainComparatorStrings(specialization, name)
        bigger = actual if actual > bigger else bigger
    return bigger












#--------------------------------------------------------------------------------------------------------------


#cardinalities
#edges
#entities
#relations
def nodesSimiliarity(node1, node2, scores):# beginning of second part

    scoreVector = []
    nodesScore = nodeSimiliarity(node1, node2, scores)
    for nodeScore in nodesScore:
        scoreVector.append(nodeScore[2])
    return average(scoreVector, len(scoreVector))
    

def nodeSimiliarity(node1, node2, scores): #part 2
    scoreList = checkNeighborSimiliarity(node1.getArestas(), node2.getArestas(), scores)
    
    for score in scoreList:
        print(f"    -{score[0]} - {score[1]} similarity:{score[2]}")
    return scoreList

def getSimilarityMostBigger(vector):
    try:
        return max(vector)
    except:
        bigger = []
        for item in vector:
            bigger.append(item[2])
        for item in vector:
            if item[2] == max(bigger):
                return item

def checkNeighborSimiliarity(edges1, edges2, scores):
    scoreListNeighbor = []
    for edge1 in edges1:
        tmpvet = []
        for edge2 in edges2:
            score = 0
            print(f"edge1: {edge1.getValor()} edge2:{edge2.getValor()}")
            if edge1.getValor().lower()[2] == edge2.getValor().lower()[2]: #only max cardinality
                score += cardinalityScore
            score += checkEntitySimilarityNeighbor(edge1.getNodo().getValor(), edge2.getNodo().getValor(), scores)
            tmpvet.append([edge1.getNodo(), edge2.getNodo(), round(score,2)])
        scoreListNeighbor.append(getSimilarityMostBigger(tmpvet))
    return scoreListNeighbor

def checkEntitySimilarityNeighbor(entity1, entity2, scores):
    for score in scores:
        if score[0] == entity1 and score[1] == entity2:
            return max(score[2], score[3]) * entityNodeScore






    
    




# ====================================================================================================== part 3

def matchNodes(scoreList):
    recordList = RS.ScoreRecords()
    for record in scoreList:
        recordList.add(record)
    recordList.matchScores()
    avgScores = recordList.getAvgScores()
    print(f"Matched scores:{len(avgScores)}")
    return avgScores



    
    
