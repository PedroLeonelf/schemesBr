class recordScores:
    def __init__(self, entidade1, entidade2, scoreName, scoreAttributes, scoreNode) -> None:
        self.entidade1 = entidade1
        self.entidade2 = entidade2
        self.scoreName = scoreName
        self.scoreAttributes = scoreAttributes
        self.scoreNode = scoreNode
        self.MaxValueComparator = 0.6
        self.MediumValueComparator = 0.3
        self.MinValueComparator = 0.1
    
    def __str__(self) -> str:
        return f"{self.entidade1} --> {self.entidade2}, scoreName:{self.scoreName}, scoreAttribute:{self.scoreAttributes}, scoreNodes:{self.scoreNode}"
    
    # def getAvg(self, nodePercent, entityPercent):
    #     return self.scoreNode * nodePercent + (max(self.scoreName, self.scoreAttributes) * self.MaxValueComparator + min(self.scoreName, self.scoreAttributes) * self.MinValueComparator) * entityPercent
    def getAvg(self):
        max,med,min = self.getMaxMediumMinScores()
        return round(self.MaxValueComparator * max + self.MediumValueComparator * med + self.MinValueComparator * min, 2)
    
    def getMaxMediumMinScores(self):
        Max = max(self.scoreName, self.scoreAttributes, self.scoreNode)
        Min = min(self.scoreName, self.scoreAttributes, self.scoreNode)
        Med = None
        vet = [Max, Med, Min]
        Med = self.scoreName if self.scoreName not in vet else None
        Med = self.scoreAttributes if self.scoreAttributes not in vet else self.scoreNode
        return Max,Med,Min








class ScoreRecords:
    def __init__(self) -> None:
        self.records = []

    
    def add(self, recorder):
        self.records.append(recorder)

    def getRepeteadRecords(self):
        repeatedRecords = []
        for idx in range(0,len(self.records)-1):
            for idz in range(idx + 1,len(self.records)):
                if(self.records[idx].entidade1 == self.records[idz].entidade1):
                    repeatedRecords.append(self.records[idx].entidade1)
        return repeatedRecords

    def getAllRecords(self,entity1):
        vect = []
        for record in self.records:
            if record.entidade1 == entity1:
                vect.append(record)
        return vect
    
    def getBiggerScore(self,vect):
        bigger = [0,None]
        for record in vect:
            media = record.getAvg()
            if media > bigger[0]:
                bigger[0], bigger[1] = media, record
        return bigger[1]

    def excludeNonBiggerScores(self,biggerScore):
        for record in self.records:
            if record.entidade1 == biggerScore.entidade1 and record != biggerScore:
                self.records.remove(record)
    
    def matchScores(self): #part3
        repetitiveScores = self.getRepeteadRecords()
        for repetiveScore in repetitiveScores:
            self.excludeNonBiggerScores(self.getBiggerScore(self.getAllRecords(repetiveScore)))
    

    def printAllRecords(self):
        for record in self.records:
            print(record)


    def getAvgScores(self):
        vect = []
        for rec in self.records:
            print(f'Nome1:{rec.entidade1} Nome2:{rec.entidade2} scoreName:{rec.scoreName} scoreAttrb{rec.scoreAttributes} scoreNode{rec.scoreNode}')
            vect.append(rec.getAvg())
        return vect
                
                
                
                
                
                
                
                
                
                
                
                
# sr = ScoreRecords(0.6, 0.4)
# sr.add(recordscores('ent1', 'ent2', 10, 10, 1)) 
# sr.add(recordscores('ent2', 'ent3', 10, 10, 1)) 
# sr.add(recordscores('ent1', 'ent2', 10, 10, 10)) 
# sr.add(recordscores('ent2', 'ent2', 10, 10, 10)) 
# sr.printAllRecords()
# print("-----------------")
# sr.matchScores()
# sr.printAllRecords()


