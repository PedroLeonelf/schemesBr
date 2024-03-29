
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
    entitySimObj = EntitySim()
    entitiesScores = entitySimObj.entitiesSimiliarity(modelo1.getEntidades(), modelo2.getEntidades())
    structureObj = Structure(modelo1, modelo2, entitiesScores)
    structureScore = structureObj.getScores()
    finalScore = defineFinalScore(entitySimObj.scoreName, entitySimObj.scoreAttributes, structureScore, modelo1.getEntidades())
    return finalScore * 100