from difflib import SequenceMatcher
from tkinter import YView
from pysinonimos.sinonimos import Search
import time


def mainComparatorStrings(string1, string2, sinList = []):
    print(f"{string1} == {string2}")
    if sinList == []:
        isPresentRate = isPresentInSentence(string1, string2)
        if isPresentRate:
            return 1
        isSimiliarityRate = similiarityBetweenStrings(string1, string2)
        if isSimiliarityRate > 0.9:
            return 1
        isSinonymRate = isSinonym(string1, string2)
        
        maximo = max(isPresentRate, isSimiliarityRate, isSinonymRate)
    else:
        maximo = max(similiarityBetweenStrings(string1, string2), isPresentInSentence(string1, string2), presentInSinonymList(string1, sinList))
    print(f"Valor maior:{maximo}\n")

    return maximo

def similiarityBetweenStrings(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()

def isSinonym(word1, word2):
    try:
        request = word1 in Search(word2).synonyms()
    except:
        request = False
    return 1 if request else 0

def isPresentInSentence(string1, string2):
    if '_' in string1 or '-' in string1 or '_' in string2 or '-' in string2:
        if isPresentInSentenceWithInterval(string1, string2):
            return 1
    menor = getSmallerString(string1, string2)
    maior = string1 if string1 != menor else string2
    return 1 if menor in maior or abbreviationDetector(string1,string2) else 0

def isPresentInSentenceWithInterval(string1, string2):
    if '_' in string1:
        retorno = isPresentWithThisInterval(string1, string2, '_')
    elif '-' in string1:
        retorno = isPresentWithThisInterval(string1, string2, '-')
    if '_' in string2:
        retorno = isPresentWithThisInterval(string2, string1, '_')
    elif '-' in string2:
        retorno = isPresentWithThisInterval(string2, string1, '-')
    return retorno

def isPresentWithThisInterval(string1, string2, interval):
    if interval in string1:
        for str in string1.split(interval):
            if isPresentInSentence(str, string2):
                return 1

    return 0

from nltk.corpus import wordnet
def sinonimoIngles(word1, word2):
    for syn in wordnet.synsets(word1):
        if word2 in syn.lemma_names():
            return True
    return False


# from nltk.corpus import wordnet

# inicio = time.time()
# for syn in wordnet.synsets("good"):
#     for name in syn.lemma_names():
#         print(name)
# fim = time.time()
# print(fim - inicio)

def getSmallerString(str1, str2):
    return str1 if len(str1) < len(str2) else str2


def abbreviationDetector(string1, string2):
    menor = getSmallerString(string1, string2)
    maior =  string1 if string1 != menor else string2
    contNextChar = 0
    for idx in range(len(menor)):
        if menor[idx] not in maior[contNextChar:]:
            return 0
        else:
            contNextChar += maior[contNextChar:].find(menor[idx]) + 1
            print(maior[contNextChar:])
    return 1    


# inicio = time.time()

# print(similiarityBetweenStrings('rio panama', 'Liu Kang'))

# fim = time.time()

def presentInSinonymList(string, list):
    try:
        return synonymScore if string in list else 0
    except:
        return 0

def checkAttributeSimiliarity(attribute, attributes):
    if attribute == 'None' and attributes[0] != 'None':
        return 0  
    vector = []
    sinList = Search(attribute).synonyms()
    for attr in attributes:
        vector.append(mainComparatorStrings(attribute, attr, sinList))
    return max(vector) if not attribute == attributes[0] else 0.7


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
  




print(similiarityBetweenStrings('qtd', 'quantidade')) #sim 46%

# print(abbreviationDetector('cpf', 'codigo_pessoa_fisica')) #sim 100%

#print(abbreviationDetector('quantidade_componentes', 'quant'))  #sim 100%

# print(similiarityBetweenStrings('quantidade', 'quant_componente'))#sim 46%



