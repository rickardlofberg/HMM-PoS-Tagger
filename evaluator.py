import probCalculator as PB
import trellisHMM2 as HMM


"""
Takes a corpusfile as param
returns a list with tupples parsed corpusfile
"""
def corpusParser(corpusToParse):
    corpusData = list()

    fileHandle = open(corpusToParse, "r")
    # Read each file in corpus
    for line in fileHandle:
        tag, output = line.split()
        corpusData.append((tag, output))
        
    # Close FH
    fileHandle.close()

    return corpusData


"""
Takes the paresed Corpus and returns a split which is roughly correct
corpus should be provide in the format as given by corpusParser function
corpus needs to have start/slut -tags to show where sentences start and ends
"""
def corpusSplitter(corpusToSplit, splitPercentage):
    # Find an estimate on where to split
    splitEstimate = int(len(corpusToSplit) * splitPercentage)

    splitPlace = int()

    for splitPlacement in range(splitEstimate - 5, len(corpusToSplit), 1):
        if corpusToSplit[splitPlacement][0] == 'start':
            splitPlace = splitPlacement
            break
    
    return corpusToSplit[:splitPlace], corpusToSplit[splitPlace:]

"""
Takes a tagged corpus in format as a list of tupples with tag and output
and return a list of tupples (sequence str, correct output)
"""
def prepareForValidate(corpusToTest):
    # List of tupples
    tuppleListOfSeq = list()
    sequence = ""
    correctTagSeq = ""

    for tag, output in corpusToTest:
        correctTagSeq += tag + " "
        if output != "''":
            sequence += output + " "
        if tag == 'slut':
            tuppleListOfSeq.append((sequence.rstrip(), correctTagSeq.rstrip()))
            correctTagSeq = ""
            sequence = ""
    return tuppleListOfSeq


##### This code is not correct since it's training on the whole corpus for now #####
"""
evaluates the accuracy

"""
def corpusEvaluator(trainingData, testCorpus):
    bigramTagProb = trainingData[0]
    tagWordProb = trainingData[1]
    correct = 0
    incorrect = 0
    for sequence in testCorpus:
        if HMM.mostLikelyPath(sequence[0], bigramTagProb, tagWordProb)[1] == sequence[1]:
            correct += 1
        else:
            print(HMM.mostLikelyPath(sequence[0], bigramTagProb, tagWordProb)[1])
            print(sequence[1])
            print("---------------")
            incorrect += 1

    return correct, incorrect


#print(len(corpusParser("corpus.txt")))
#a,b =(corpusSplitter(corpusParser("corpus.txt"), 0.8))
#print(a[len(a)-1], b[0])
#for i in a:
#    print(i)

#print(prepareForValidate(b))

a,dataToEvaluate =(corpusSplitter(corpusParser("corpus.txt"), 0.8))
fixedData = prepareForValidate(dataToEvaluate)
probs = PB.probability("corpus.txt")
print(corpusEvaluator(probs, fixedData))
