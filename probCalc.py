"""
Takes a corpus and calculate the probability for unigrams, bigrams, trigrams and a word belonging to a PoS tag
"""
def probability(corpus):
    unigrams = dict() # Structure : {unigram : count}
    bigrams = dict() # Structure : {bigram : count}
    trigrams = dict() # Structure : {trigram : count}
    wordIsPoS = dict() # Structure : {word1 : {unigram : count}, word2 : {unigram : count}}

    # Current word var
    word = ''

    # Filler tags to be used to mark sentence beginings and ends
    startTag = 'start' # Filler start tag2Prob
    endTag = 'end' # Filler ender tag

    # Tags to keep track of previous tags
    t2 = startTag # This is T-2, i.e. two tags ago
    t1 = startTag # This is T-1, i.e one tag ago
    t0 = '' # This is t0, i.e. the current tag
    """ Example if "The dog ate" have the tags "ART NN VB" and we are checking dog:
    t2 is "ART"
    t1 is "NN"
    t0 is "VB" (The one we are currently iteretaing on)
    """

    # We expect the corpus to be a tab seperated file with a "word - PoS-tag" structure
    with open(corpus, 'r') as corp:
        """Parse and count he corpus"""
        for line in corp:
            # If line is a sentence seperator
            if line == "\n":
                # Add a starttag to dict
                unigrams[startTag] = unigrams.get(startTag, 0) + 1
                word, t0 = '', endTag
            else:
                # Update word and current PoS tag
                word, t0 = line.strip().split("\t")

            # Trigram, bigram and unigram count
            trigram = ' '.join([t2, t1, t0]) # Create trigram
            trigrams[trigram] = trigrams.get(trigram, 0) + 1 # Add to dict
            bigram = ' '.join([t1, t0]) # Create bigram 
            bigrams[bigram] = bigrams.get(bigram, 0) + 1 # Add to dict
            unigrams[t0] = unigrams.get(t0, 0) + 1

            # Word counter
            if wordIsPoS.get(word, -1) == -1: # If no word create word
                wordIsPoS[word] = {t0 : 0}
            wordIsPoS[word][t0] = wordIsPoS[word].get(word, 0) + 1 # Always update

            # Set next iteration to have filler start tags
            if line == "\n":
                t2 = startTag
                t1 = startTag
            else:
                # Update tags
                t2 = t1
                t1 = t0

    """After counting we calculate the probabilities"""
    uniProb = dict()
    biProb = dict()
    triProb = dict()
    wordProb = dict()

    # Unigram probabilites
    for unigram in unigrams:
        uniProb[unigram] = unigrams[unigram] / sum(unigrams.values())

    # Bigram probability
    for bigram in bigrams:
        biProb[bigram] = bigrams[bigram] / unigrams[bigram.split(' ')[0]]

    # Trigram probabilty
    for trigram in trigrams:
        triProb[trigram] = trigrams[trigram] / unigrams[trigram.split(' ')[0]]

    # Word has pos probabiliy
    for word in wordIsPoS:
        wordProb[word] = {}
        for tag in wordIsPoS[word]:
            wordProb[word][tag] = wordIsPoS[word][tag] / sum(wordIsPoS[word].values())

    return uniProb, biProb, triProb, wordProb

def calcluateProb(corpus="suc", outputFile="prob.txt"):
    """This is used to create a more human readable file to check output"""
    with open(outputFile, 'w') as PB:
        x = 0
        for i in probability(corpus):
            if x == 0:
                PB.write("Transition unigram probability:\n")
            elif x == 1:
                PB.write("Transition bigram probability:\n")
            elif x == 2:
                PB.write("Transition trigram probability:\n")
            elif x == 3:
                PB.write("Emission probability:\n")
            x += 1
            for t, v in sorted(i.items()):
                PB.write(str(t) + "\t" + str(v)  + "\n")
                    
if '__main__' == __name__:
    calcluateProb()






