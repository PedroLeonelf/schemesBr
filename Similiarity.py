
from difflib import SequenceMatcher
from pysinonimos.sinonimos import Search
import RecorderScores as RS
from nltk.corpus import wordnet

metaScore = 0.7
#-----------------------
entityScore = 0.6
nodeScore = 0.4
#-----------------------
cardinalityScore = 0.2
entityNodeScore = 0.8
#-----------------------
synonymScore = 0.7
attributeSimiliarity = True
english_text = False
utilizeSynonym = False


def average(vector, lenSize):
    if vector == []:
        return 0
    return round(sum(vector)/lenSize,2)

import time



def graphSimiliarity(graph1, graph2):

    inicio = time.time()

    scores = entitiesSimiliarity(graph1, graph2) # first part
    scoreList = []
    for score in scores:
        print(f'\n{score[0]} -- {score[1]} \nscoreName:{score[2]}\nscoreAttributes:{score[3]} \nAvgScore:{score[4]}' )
        scoreList.append(RS.recordScores(score[0], score[1], score[2], score[3], nodesSimiliarity(graph1.getNo(score[0]), graph2.getNo(score[1]), scores)))# second part) 
    finalScore = matchNodes(scoreList)
    print(f'Final Medias:{finalScore}')
    print(f"Graph similarity is {average(finalScore, len(graph1.getNos())) * 100}%")
    fim = time.time()
    print((fim - inicio)/60)
    return average(finalScore, len(graph1.getNos())) * 100
    
            
def entitiesSimiliarity(graph1, graph2):
    scores = []
    for node1 in graph1.getNos():
        for node2 in graph2.getNos():
            scores.append(entitySimiliarity(node1.getValor(), node2.getValor()))
    return scores



#### string similiarity functions#################################################################

def mainComparatorStrings(string1, string2):
    print(f"{string1} == {string2}")

    isSimiliarityRate = lcs_init(string1, string2)
    if isSimiliarityRate > 0.8:
        return isSimiliarityRate
    sinonymRate = (isSinonym(string1, string2) if not english_text else is_sinonym_english(string1,string2)) if utilizeSynonym else 0  
    maximo = max(isSimiliarityRate, sinonymRate)
    print(f"Valor maior:{maximo}\n")

    return maximo


def lcs(string1, string2):
    m, n = len(string1), len(string2)
    L = [[None]*(n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif string1[i-1] == string2[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    return L[m][n]

def lcs_init(string1, string2):
    return lcs(string1 ,string2) / min(len(string1),len(string2))


def isSinonym(word1, word2):
    try:
        request = word1 in Search(word2).synonyms() or word2 in Search(word1).synonyms()
    except:
        request = False
    return synonymScore if request else 0


def is_sinonym_english(word1, word2):
    for syn in wordnet.synsets(word1):
        if word2 in syn.lemma_names():
            return True
    return False

def presentInSinonymList(string, list):
    try:
        return synonymScore if string in list else 0
    except:
        return 0

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
    bigger = 0
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




def AttributesSimiliarity(entity1, entity2):
    score = 0
    for attribute in entity1.getAtributos():
        score += checkAttributeSimiliarity(attribute.getNome().lower().strip(), entity2.getAtributos())
    score /= max(len(entity1.getAtributos()), len(entity2.getAtributos()))
    return score

def checkAttributeSimiliarity(attribute, attributes):
    vector = []
    firstAttribute = attributes[0].getNome().lower()
    if attribute == 'none' and firstAttribute != 'none' or firstAttribute == 'none' and attribute != 'none':
        return 0
    for attr in attributes:
        vector.append(mainComparatorStrings(attr.getNome().lower().strip(), attribute))
    return max(vector)

def checkNoAttribute(attribute, attributes):
    return attribute == 'none' and attributes.getNome().lower() == 'none'




#--------------------------------------------------------------------------------------------------------------


#cardinalities
#edges
#entities
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



    
    
