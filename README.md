# HMM-PoS-Tagger

A project to build a Part-of-Speech tagger which can train on different corpuses. Program is written for Python and the tagging is based on HMM (Hidden Markov Model) and implemented with the Viterbi Algorithm.

You can read more about these in Wikipedia or from the book which I used Speech and Language Processing by Dan Jurafsky and James H. Margin.

HMM: https://en.wikipedia.org/wiki/Hidden_Markov_model
Viterbi: https://en.wikipedia.org/wiki/Viterbi_algorithm
Speech and Language Processing: https://web.stanford.edu/~jurafsky/slp3/

## The Code
The code consists of four parts which all will be descripbed here. 

## corpCreate.py
In brief corpCreate.py is used to create a corpus in the format which the other parts are used. This is for testing and understanding, it only has two "PoS-tags" and three words. 
The output will be written to a file and the user can also choose the amount of "sentences" to write. The format of the outputfile is a tab seperated file with the word to the left and PoS-tag to the right. This is the format which is also used by probCalc.py to calculate the probabilties needed for tagging.
An example of running this program is:

python3 corpCreate.py myCorpus 10000 

Which will write 10 000 "sentences" to the file myCorpus.


## probCalc.py 
Is the part of the code which parses data to get the probabilities and can either be used to a tagging objekt or printed for inspection or later use. An example invoction is:

python3 provCalc.py myCorpus myProbabilites

which read the data from myCorups and calculate the probabilites and write them to the file myProbabilites.

## tagger.py
This part can't be run by itself but holds an object which have probabilites as parameters, once it has been initilised it can be used to tag sentences.

## n-fold.py
Is used to do a 10-fold cross validation, you can give this both the data you want to use for training and testing since it will internally divid it into 10-parts. It will do this 10 times and will in total do ten 10-fold cross validations. It divides the data by using random which is initilised with a different seed every time to make experiments repeatable. An example of how to invoke it is:

python3 n-fold.py myCorp

