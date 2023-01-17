from pysinonimos.sinonimos import Search
from nltk.corpus import wordnet

#-----------------------
cardinalityScore = 0.2
entityNodeScore = 0.8
#-----------------------
synonymScore = 1
english_text = False
utilizeSynonym = False


#### string similiarity functions#################################################################
def mainComparatorStrings(string1, string2):
    

    isSimiliarityRate = lcs_init(string1, string2)
    if isSimiliarityRate > 0.9:
        return isSimiliarityRate
    sinonymRate = (isSinonym(string1, string2) if not english_text else is_sinonym_english(string1,string2)) if utilizeSynonym else 0  
    maximo = max(isSimiliarityRate, sinonymRate)
    # print(f"{string1} == {string2}")
    # print(f"Valor maior:{maximo} {lcs_init(string1,string2)}\n")
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

### Attribute similarity
def AttributesSimiliarity(entity1, entity2):
    score = 0
    if entity1.getAtributos()[0].getNome().lower() == 'none' and entity2.getAtributos()[0].getNome().lower() == 'none': return 1
    for attribute in entity1.getAtributos():
        score += checkAttributeSimiliarity(attribute.getNome().lower().strip(), entity2.getAtributos(), attribute.isIdentifier())
    
    score /= max(len(entity1.getAtributos()), len(entity2.getAtributos()))
    return score

def checkAttributeSimiliarity(attribute, attributes, key):
    
    vector = []
    firstAttribute = attributes[0].getNome().lower()
    
    if attribute == 'none' and firstAttribute != 'none' or firstAttribute == 'none' and attribute != 'none':
        return 0
    for attr in attributes:
        vector.append(mainComparatorStrings(attr.getNome().lower().strip(), attribute) * 0.8 + equalKey(attr.isIdentifier(),key) * 0.2)
    return max(vector)

def equalKey(key1, key2):
    # print(key1,key2)
    if key1 == key2:
        return 1
    return 0

def truncate(number):
    return round(number, 2)

def average(vector, lenSize = None):
    if vector == []:
        return 0
    if lenSize == None : lenSize = len(vector)

    return round(sum(vector)/lenSize,2)
