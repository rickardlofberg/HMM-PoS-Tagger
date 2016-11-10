import sys
import os.path
import random
"""
This program will calculate the probabilities which are needed to PoS-tag sentences and consists of two functions.
1. probability() : Takes a list of lists, where the nested list represent a sentence and each word is represented as a tuple with (word, tag). It will return four dictionaries with the required probabilities.
2. calcluateProb() : Is an umbrella for probability. If the user has a tab separated file of corpus data this function will read that file and write data and gives the possibility to write the calculations to a file.
Main : This is to run the program form the command line. It requires a corpus but will write the data to a file if one isn't provided.
"""


def probability(listOfTuples):
    """Takes a list with lists representing sentences with (word - tag) and calculate the probability for unigrams, bigrams, trigrams and a word belonging to a PoS tag"""
    unigrams = dict() # Structure : {unigram : count}
    bigrams = dict() # Structure : {bigram : count}
    trigrams = dict() # Structure : {trigram : count}
    wordIsPoS = dict() # Structure : {word1 : {unigram : count}, word2 : {unigram : count}}

    # Current word
    word = ''

    # Filler tags to be used to mark sentence starts and ends
    startTag = 'start' # Filler start tag2Prob
    endTag = 'end' # Filler end tag

    # Tags to keep track of previous tags
    #t2 = startTag # This is T-2, i.e. two tags ago
    t2 = '' # This is T-2, i.e. two tags ago
    t1 = startTag # This is T-1, i.e one tag ago
    t0 = '' # This is t0, i.e. the current tag
    """ Example if "The dog ate" have the tags "ART NN VB" and we are checking ate:
    t2 is "ART"
    t1 is "NN"
    t0 is "VB" (The one we are currently iterating on)
    """

    # For each sentence (list)
    for sent in listOfTuples:
        # Add filler endtag to sentence
        sentence = sent
        sentence.append(('',''))

        # For each (word, pos)-tag tuple
        for tagWord in sentence:
            # If reached end of sentence
            if tagWord[1] == '': 
                # Add a starttag to dict
                unigrams[startTag] = unigrams.get(startTag, 0) + 1
                word, t0 = '', endTag
            else:
                word, t0 = tagWord
                
            # Trigram, bigram and unigram count
            trigram = ' '.join([t2, t1, t0]).strip() # Create trigram
            trigrams[trigram] = trigrams.get(trigram, 0) + 1 # Increase trigram count
            bigram = ' '.join([t1, t0]) # Create bigram 
            bigrams[bigram] = bigrams.get(bigram, 0) + 1 # Increase bigram count
            unigrams[t0] = unigrams.get(t0, 0) + 1 # Increase unigram count

            # Word counter
            wordIsPoS[word] = wordIsPoS.get(word, {t0 : 0}) # If not key for word, add word
            wordIsPoS[word][t0] = wordIsPoS[word].get(t0, 0) + 1 # Increase word PoS-tag count

            # Update tags
            if word == '': # End of sentence
                t2 = ''
                t1 = startTag
            else:
                t2 = t1
                t1 = t0

    """After counting we calculate the probabilities"""
    # Same structure as above dictionaries but these hold probabilities instead of count
    uniProb = dict()
    biProb = dict()
    triProb = dict()
    wordProb = dict()

    # Unigram probabilities
    for unigram in unigrams:
        uniProb[unigram] = unigrams[unigram] / sum(unigrams.values())

    # Bigram probability
    for bigram in bigrams:
        biProb[bigram] = bigrams[bigram] / unigrams[bigram.split(' ')[0]]

    # Trigram probability
    for trigram in trigrams:
        bx = ' '.join(trigram.split(' ')[0:2])
        #print(bx)
        #print(bigbx)
        triProb[trigram] = trigrams[trigram] / bigrams[bx]
        #triProb[trigram] = trigrams[trigram] / unigrams[trigram.split(' ')[0]]

    # Word has pos probability
    for word in wordIsPoS:
        wordProb[word] = {}
        for tag in wordIsPoS[word]:
            wordProb[word][tag] = wordIsPoS[word][tag] / sum(wordIsPoS[word].values())

    return uniProb, biProb, triProb, wordProb


def calcluateProb(corpus=None, outputFile=None):
    """Reads a corpus which is tab separated in a "word tab tag" format. If outputFile is given, probabilities are written to it.
    The unigram, bigram, trigram and wordPos probability is always returned as four dictionaries."""

    # Make sure it has a file to read from
    if not os.path.isfile(corpus):
        return None

    data = [] # Holds the sentences to be calculated
    senTag = [] # Represent a sentence
    w, t = '', '' # Word and tag
    with open(corpus, 'r') as C:
        for line in C:
            if line == '\n': # If new sentence
                data.append(senTag)
                senTag = []
            else: # Add word - tag data for each sentence
                try: # If user gives bad data program doesn't break
                    w, t = line.strip().split('\t')
                    senTag.append((w, t))
                except:
                    pass

    if outputFile: # If output file
        # Write to output file
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

    return probability(data)

if '__main__' == __name__:
    """If the program is run as main the user needs to provide a corpus file."""
    
    try: # Corpus to read from
        corpus = sys.argv[1]
    except:
        corpus = None
        print("No corpus to parse")

    try: # File to save to
        output = sys.argv[2] # If output file
    except:
        # Otherwise create an output file which is not in dir
        output = "prob{}".format(int(random.random()*100))
        while os.path.isfile(output):
            output = "prob{}".format(int(random.random()*100))

    if corpus:
        calcluateProb(corpus, output)
        print("The probabilities from {} has been written to {}.".format(corpus, output))
