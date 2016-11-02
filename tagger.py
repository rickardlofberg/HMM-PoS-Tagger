class Tagger():

    def __init__(self, uniProb, biProb, triProb, wordProb):
        """Used for HMM tagging of sentences"""
        self.uniProb = uniProb
        self.biProb = biProb
        self.triProb = triProb
        self.wordProb = wordProb
        self.endTag = {'end' : 1.0}

        # Dictionary for when word not found
        self.posTags = dict()
        for tag in self.uniProb.keys():
            self.posTags[tag] = 1 / len(self.uniProb)
          
    def tagSentence(self, sentToTag):
        """Takes a sentence (sequenced list) and returns a list of same length with PoS-tags"""
        # Make sure it's a sentence
        if isinstance(sentToTag, list):
            sentence = sentToTag + [None]
        else:
            return "Sentence not submitted in the corret format"

        # A list which holdes all sequences and there current probabilites
        possibleSeq = list()
        
        # A list to keep track of best path so far and possible best paths
        startFiller = ['start', 'start']
        currentPaths = [(1, startFiller)] # The probability of start = 1 and the first nodes are start
        newPaths = []

        # For each word
        for word in sentence:
            
            # If there are tags for the word use them, otherwise check against all tags
            possibleTags = self.wordProb.get(word, self.posTags)
            if word == None:
                possibleTags = self.endTag

            # For each possible tag for that word
            for tag in possibleTags:
                nodePosValues = []
                
                # Go from all possible previous paths to current tag (node)
                for path in currentPaths:
                    # Create bigram and trigram
                    trigram = ' '.join(path[1][-2:] + [tag])
                    bigram = ' '.join(path[1][-1:] + [tag])
                    #bprint(trigram)

                    # We can calculate emission and old node value here
                    pathProb = path[0] * possibleTags[tag]
                    
                    # If we can calculate with trigram
                    if self.triProb.get(trigram, -1) != -1:
                        pathProb *= self.triProb[trigram]
                    elif self.biProb.get(bigram, -1) != -1: # Try bigram
                        pathProb *= self.biProb[bigram]
                    else: # Otherwise just use unigram
                        pathProb *= self.uniProb[tag]

                    nodePosValues.append((pathProb, path[1] + [tag]))

                newPaths.append(max(nodePosValues))

            currentPaths = newPaths
            newPaths = []

        currentPaths = max(currentPaths)

        # Return the Pos sequence without the two starting tags
        return currentPaths[1][2:-1]

if __name__ == '__main__':        
    import probCalc

    uni, bi, tri, word = probCalc.probability("corpus.txt")
    t = Tagger(uni, bi, tri, word)

