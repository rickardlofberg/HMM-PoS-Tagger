"""
Takes a list with lists representing sentences with (pos-tag, word) tupples and calculate the probability for unigrams, bigrams, trigrams and a word belonging to a PoS tag
"""
def probability(listOfTuples):
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

    """Parse and count he corpus"""
    # For each sentece (list)
    for sent in listOfTuples:

        # For each (word, pos)-tag tupple
        for wpTag in sent:
            if wpTag[1] == '':
                # Add a starttag to dict
                unigrams[startTag] = unigrams.get(startTag, 0) + 1
                word, t0 = '', endTag
            else:
                word, t0 = wpTag
                
            # Trigram, bigram and unigram count
            trigram = ' '.join([t2, t1, t0]) # Create trigram
            trigrams[trigram] = trigrams.get(trigram, 0) + 1 # Add to dict
            bigram = ' '.join([t1, t0]) # Create bigram 
            bigrams[bigram] = bigrams.get(bigram, 0) + 1 # Add to dict
            unigrams[t0] = unigrams.get(t0, 0) + 1

            # Word counter
            if wordIsPoS.get(word, -1) == -1: # If no word create word
                wordIsPoS[word] = {t0 : 0}
            wordIsPoS[word][t0] = wordIsPoS[word].get(t0, 0) + 1 # Always update

            if wpTag[1] == '':
                t2 = startTag
                t1 = startTag
            else:
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


def calcluateProb(corpus="suc", outputFile=None):
    """This is used to create a more human readable file to check output"""
    data = []
    senTag = []
    w, t = '', ''
    with open(corpus, 'r') as C:
        for line in C:
            if line == '\n':
                senTag.append(('', ''))
                data.append(senTag)
                senTag = []
            else:
               w, t = line.strip().split('\t')
               senTag.append((w, t))

    if outputFile == None:
        return probability(data)

    with open(outputFile, 'w') as PB:
        x = 0
        for i in probability(data):
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
    calcluateProb("suc", None)

