import probCalculator as PB

"""
Helper function that converts a word probability for each tag to a more readable format
"""
def tagWordProbUpdater(tagWordProb):
    # Change dictionarty to a word with PoStags as values
    outPossibleTags = dict()
    for tag in tagWordProb:
        for out in tagWordProb[tag]:
            if outPossibleTags.get(out, -1) == -1:
                outPossibleTags[out] = {tag : tagWordProb[tag][out]}
            else:
                outPossibleTags[out][tag] = tagWordProb[tag][out]

    # Add a token ending tag
    outPossibleTags['slut'] = {'' : 1}
    return outPossibleTags


"""
@Param string of words, probability for bigrams of tags and word probability for each tag
@return a tupple with (seq probability, sequence)
"""
def mostLikelyPath(line, bigramProbability, wordProbabilty):
    # Assign probabilities
    outPossibleTags = dict()
    outPossibleTags = tagWordProbUpdater(wordProbabilty)
    bigramTagProb = bigramProbability

    # Assign token start node with value
    preValues = [(1, 'start')]
    newValues = []
    # Add token end tags
    sequence = line.strip() + " slut"
    
    # Check all outputs
    for posibility in sequence.split():

        # Get all possible tags for that output
        for posOutput in outPossibleTags[posibility]:
            posMaxValue = []

            # Check compatable bigrams from previous values with possilbe tags
            for lastNode in preValues:

                # Get bigrams
                if posibility == 'slut':
                    posBigram = str(lastNode[1].split()[-1:][0]) + " slut"
                else:
                    # lastNode[1].split()[-1:][0] is an overcomplex way to get the last value
                    posBigram = str(lastNode[1].split()[-1:][0]) + " " + str(posOutput)

                # If bigram allowed, calculate
                if bigramTagProb.get(posBigram, -1) != -1:
                    if posibility != 'slut':
                        # Assign possible from X to Y combs with pos and prev seq
                        posMaxValue.append((lastNode[0] * bigramTagProb[posBigram] * outPossibleTags[posibility][posOutput], (str(lastNode[1]) + " " + str(posOutput))))
                    else:
                        # Assign possible from X to Y combs with pos and prev seq
                        posMaxValue.append((lastNode[0] * bigramTagProb[posBigram] * outPossibleTags[posibility][posOutput], (str(lastNode[1]) + " " + str(posibility))))

            # Get the new maximum path to node
            newValues.append(max(posMaxValue))
        preValues = newValues
        newValues = []

    return max(preValues)


# Examples of how to get the probability to run the functions

# Get probabilites from corpus
#probs = PB.probability("corpus.txt")
#bigramTagProb = probs[0]
#tagWordProb = probs[1]
#print(mostLikelyPath("mu mu kvack", bigramTagProb, tagWordProb))
