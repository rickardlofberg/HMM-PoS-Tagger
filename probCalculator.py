"""
Takes the name of a corpus to check and retirns two dictionaries
one with word probability given tag
the other tag probability given previous tag
"""
def probability(corpus):
    wordTagCount = dict()
    tagBigrams = dict()
    tagCount = dict()

    # Read each line in corpus
    # Each line should have a tag and an output. No output is represented as ''
    for line in open(corpus, "r"):
        tag = line.split()[0]
        word = line.split()[1]

        # To avoid bigrams where start is the second part
        if tag != 'start':
            # Build bigram
            tagBigram = prevTag + " " + tag

            # Build and update dictionary
            tagBigrams[tagBigram] = tagBigrams.get(tagBigram, 0) + 1
    
        # If the tag has output, create/update tag -> output count dictionary
        if word != "''":
            if wordTagCount.get(tag, -1) == -1:
                wordTagCount[tag] = {word : 1}
            else:
                wordTagCount[tag][word] = wordTagCount[tag].get(word, 0) + 1

        # To get P(ti-1,ti) all tags which can be in pos1 of bigram is counted
        if tag != 'slut':
            tagCount[tag] = tagCount.get(tag, 0) + 1
  
        prevTag = tag

    # Calculate probabilities
    tagProb = dict()
    wordTagProb = dict()

    # P(Ti-1, ti)
    for bigram in tagBigrams:
        firstPosTag = bigram.split()[0]
        tagProb[bigram] = tagBigrams[bigram] / tagCount[firstPosTag]

    # Given tag get prob for word
    for tag in wordTagCount:
        wordTagProb[tag] = {}
        for word in wordTagCount[tag]:
            wordTagProb[tag][word] = float(wordTagCount[tag][word] / tagCount[tag])

    return tagProb, wordTagProb

#print(probability("corpus.txt"))
with open("prob.txt", "w") as PB:
    x = 0
    for i in probability("corpus.txt"):
        if x == 0:
            PB.write("Transition probability:\n")
        elif x == 1:
            PB.write("Emission probability:\n")
        x += 1
        for t, v in sorted(i.items()):
            PB.write(str(t) + "\t" + str(v)  + "\n")
