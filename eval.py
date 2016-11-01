from probCalc import probability as PB
from tagger import Tagger

corpus = "suc"

uni, bi, tri, word = PB(corpus)
tagger = Tagger(uni, bi, tri, word)


with open(corpus, 'r') as corp:
    listOfTags = []
    sentence = []
    correctTag = []
    tagSeq = []
    for line in corp:
        if line == '\n':
            correctTag.append(tagSeq)
            listOfTags.append(tagger.tagSentence(sentence))
            sentence = []
            tagSeq = []
        else:
            sentence.append(line.split()[0])
            tagSeq.append(line.split()[1])


#print(len(correctTag))
#print(len(listOfTags))
correct = 0
incorrect = 0

for i1 in range(len(correctTag)):
    for i2 in range(len(correctTag[i1])):
        if correctTag[i1][i2] == listOfTags[i1][i2]:
            correct += 1
        else:
            incorrect += 1
 
print(correct)
print(incorrect)
print("{} is correct".format(round(correct / (correct + incorrect), 2)))
