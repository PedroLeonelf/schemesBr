from Similarity.Utility import average, truncate

class Structure:
    def __init__(self, model1, model2, entitiesScores) -> None:
        self.model1 = model1
        self.model2 = model2
        self.dict = {}
        for entity1 in model1.getEntidades():
            for entity2 in model2.getEntidades():
                self.dict[f'{entity1.getNome().lower()}-{entity2.getNome().lower()}'] = self.entityStructureSim(entity1, entity2, entitiesScores)
        self.dict

    def getScores(self):
        return self.dict

    def entityStructureSim(self,entity1, entity2, entitiesScores) -> float:
        value = 0
    
        entityNeighboorScore = self.neighboorSim(entity1, entity2, entitiesScores)
        value = (entityNeighboorScore + cardinalityScore) / 2
        return truncate(value)


    def neighboorSim(self,entity1, entity2, scores) -> float:
        entities1, entities2 = self.getNeighboorEntities(entity1.getRelacionamentos(),self.model1,entity1), self.getNeighboorEntities(entity2.getRelacionamentos(),self.model2,entity2)
        vect = []
     
        for entiti1 in entities1:
          
            tmp = []
            for entiti2 in entities2:
                tmp.append(scores[f'{entiti1.getNome().lower()}-{entiti2.getNome().lower()}'])
                print(f'entitie1:{entiti1.getNome().lower()} ent2:{entiti2.getNome().lower()}, tmp:{tmp}')

            if tmp != []:
                vect.append(max(tmp))
           
        return average(vect)



    def getNeighboorEntities(self,relations, model, entity) -> list:
        vect = []
        for relation in relations:
            for entitie in model.getRelacionamentoPorNome(relation).getEntidadesRelacionadas():
                if entitie.getNome() != entity.getNome():
                    vect.append(entitie)
        return vect