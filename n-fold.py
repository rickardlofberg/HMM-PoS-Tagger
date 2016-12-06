from probCalc import probability as PB
from tagger import Tagger
import sys
import os.path
from random import random, seed

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
def dividList(alist, n, startSeed):
    """Divide a list into n equal parts (almost) and returns a list with each part as a list in the list"""
    seed(startSeed)
    
    # Create a table of tables with n internal tables to hold output data
    data = [[] for _ in range(n)] 

    # Copy the input data to not corrupt the list
    inData = alist.copy()
    
    # While there is still data in the list
    while len(inData) != 0:
        for i in range(n):
            try: # To escape issues if all values are removed
                # Remove a sentence from inData
                getSent = inData.pop(int(random() * len(inData)))
                # Append to sublist i
                data[i].append(getSent)
            except:
                pass

    return data

def evaluate(n, corpus):
    """Runs the n-fold validation on a corpus"""
    if n < 1:
        n = 10
        print("n was to low and has been set to 10\n")

    # Get all the data
    sentences, correctTags, tagData = corpusReader(corpus)
    allCor = []
    allIncor = []


    for check in range(1, n+1):
        # Divide all the data
        divSent = dividList(sentences, n, check)
        divTags = dividList(correctTags, n, check)
        divTrain = dividList(tagData, n, check)
        # To count the total of incorrect and correct tags
        correctlyTagged = []
        incorrectlyTagged = []

        print("Check {} doing {}-fold on {}\n".format(check, n, corpus))

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

        allCor.extend(correctlyTagged)
        allIncor.extend(incorrectlyTagged)

        # Total in numbers..
        print("\n{} out of {} was correctly tagged.".format(sum(correctlyTagged), sum(correctlyTagged) + sum(incorrectlyTagged)))

        # .. and percentage
        print("\nFor a total of {}% correctness.".format(round(sum(correctlyTagged) / (sum(correctlyTagged) + sum(incorrectlyTagged))*100, 2)))

    # Total in numbers..
    print("\n{} out of {} was correctly tagged.".format(sum(allCor), sum(allCor) + sum(allIncor)))

    # .. and percentage
    print("\nFor a total of {}% correctness.".format(round(sum(allCor) / (sum(allCor) + sum(allIncor))*100, 2)))



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

