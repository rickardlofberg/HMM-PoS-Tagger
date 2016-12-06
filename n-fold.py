from probCalc import probability as PB
from tagger import Tagger
import sys
import os.path
from random import random, seed

seed = 1

def corpusReader(corpus):
    """A function which parses a corpus and returns three lists. one with all the sentences, one with all the correct tags and a one with both"""

    # Read the corpus and create two lists with all the data
    with open(corpus, 'r') as corp:
        sentences = [] # All the sentences
        correctTags = [] # Correct tags
        tagData = [] # Sentences with word and tags

        # Initiate temporary data holders
        words, tags, oneTag = [], [], []

        # Read corpus
        for line in corp:
            # Sentences are marked by newlines
            if line == '\n':
                # Add correct tags to list
                correctTags.append(tags)
                # Add words to list of sentence
                sentences.append(words)
                # Add tagdata
                tagData.append(oneTag)

                # Reset words and tags
                words, tags, oneTag  = [], [], []
            else:
                # Add correct tags and words
                words.append(line.split()[0])
                tags.append(line.split()[1])
                bothTags = (line.split()[0], line.split()[1])
                oneTag.append(bothTags)
    print(len(sentences))
    return sentences, correctTags, tagData

# Breaks a list into n parts and returns a list of the parts
def dividList(alist, n):
    """Divide a list into n equal parts (almost) and returns a list with each part as a list in the list"""
    # Used for first n-1 parts
    n1 = int(len(alist) / n)
    # Used for last part to make sure which will get the rest to make it divide even
    n2 = int((len(alist) / n) + len(alist) % n)

    # Get the first n-1 parts
    data = [alist[i:i+n1] for i in range(0, len(alist)-n2, n1)]
    # Get the last part + extra modulo lists
    data.extend([alist[i:i+n2] for i in range(len(alist)-n2, len(alist), n2)])
    return data

def evaluate(n, corpus):
    """Runs the n-fold validation on a corpus"""
    if n < 1:
        n = 10
        print("n was to low and has been set to 10\n")

    # Get all the data
    sentences, correctTags, tagData = corpusReader(corpus)

    # Divide all the data
    divSent = dividList(sentences, n)
    divTags = dividList(correctTags, n)
    divTrain = dividList(tagData, n)
    # To count the total of incorrect and correct tags
    correctlyTagged = []
    incorrectlyTagged = []

    print("Calculation {}-fold on {}\n".format(n, corpus))

    # For each part to evaluate
    for i in range(0, n):
        # Get the parts to train on
        trainingParts = divTrain[:i] + divTrain[i+1:]
        train = []

        # They need to be formatted so that we can use the Tagger
        for index in range(len(trainingParts)):
            train.extend(trainingParts[index])
        
        # Get the testing and evaluation data
        testingData = divSent[i]
        evaluationData = divTags[i]
        
        # Do some training
        uni, bi, tri, word = PB(train)
        tagger = Tagger(uni, bi, tri, word)
        
        # Reset counts
        correctTagCount = 0
        incorrectTagCount = 0

        # Go through each sentence and tag it
        for index in range(len(testingData)):
            tagged = tagger.tagSentence(testingData[index])
            for tag in range(len(tagged)):
                # If correct
                if evaluationData[index][tag] == tagged[tag]:
                    correctTagCount += 1
                else:
                    incorrectTagCount += 1
            
        # Print to let you know I haven't forgotten about you.
        print("{}-fold was tagged {}% correctly.".format(i+1, round(correctTagCount / (correctTagCount + incorrectTagCount)*100,2 )))

        # Save n-fold counts
        correctlyTagged.append(correctTagCount)
        incorrectlyTagged.append(incorrectTagCount)

    # Total in numbers..
    print("\n{} out of {} was correctly tagged.".format(sum(correctlyTagged), sum(correctlyTagged) + sum(incorrectlyTagged)))

    # .. and percentage
    print("\nFor a total of {}% correctness.".format(round(sum(correctlyTagged) / (sum(correctlyTagged) + sum(incorrectlyTagged))*100,2 )))


if __name__ == '__main__':
    """Run script with args corpus and amount of folds """
    try: # Corpus to read from
        corpus = sys.argv[1]
    except:
        corpus = None
        print("No corpus to evaluate")

    try: # n-fold
        n = int(sys.argv[2]) # If output file
    except:
        n = 10
        
    if os.path.isfile(corpus):
        evaluate(n, corpus)
    else:
        print("{} not found.".format(corpus))

