"""
This is a program that generates a sequence of "hello", "mu", "quack" given the probabilities below
Output is saved to a file, one line per sequence and the amount of sequences can be chosen
"""
import random
import sys
import os.path

"""
Takes a dictionary of dictionaries, outer dict key = current state, value = dict 
of new states and their probabilities
returns a new state
"""
def randomState(stateDict, currentState):
    # Get a random number
    stateNumber = random.random()

    # Initiate a sum at zero to decide next state
    stateSum = 0.0

    # Loop through states until new state is found
    for newState in stateDict[currentState].keys():
        # Add probability to sum
        stateSum += stateDict[currentState][newState]

        # If sum is bigger than number return state
        if stateSum > stateNumber:
            return newState

## These are the options for the code
####################################################################################

# All possible state transitions given current state > new state > prob of new state
stateTransitions = {'start' : {'cow' : 0.5, 'duck' : 0.5},
                    'cow' : {'cow' : 0.5, 'duck' : 0.3, 'slut' : 0.2},
                    'duck' : {'cow' : 0.3, 'duck' : 0.5, 'slut' : 0.2}}

# All possible observations given current state > observation > probability of observation
observations = {'cow' : {'hello' : 0.1, 'mu' : 0.9},
                'duck' : {'hello' : 0.4, 'quack' : 0.6}}

#######################################################################################

def createCorpus(corpusName, sentences=None):
    """This code will generate a controlled corpus for testing
    If the user wants to specify the amount of sequences they need to name the output."""
    if not sentences:
        sentences = 1000
    
    with open(corpusName, 'w') as out:
        for i in range(sentences):
            state = 'start'
            while state != 'slut':
                state = randomState(stateTransitions, state)
                if state != 'slut':
                    out.write(randomState(observations, state) + "\t" + state + "\n")
            out.write("\n") 

if '__main__' == __name__:
    """Takes arguments to create the corpus.
    1. If only a number is given a corpus with a random name is create with that number of sequences.
    2. If only a string is given a 1000 sequences will be written to a file with that name.
    3. If string and number is given both of the above apply. """
    try:
        in1 = None
        in1 = sys.argv[1]
        in1 = int(in1)
    except:
        if not isinstance(in1, str):
            in1 = None

    if in1 and isinstance(in1, int) == False:
        corpName = in1
    else:
        # Make up corp name
        corpName = "corpus{}.txt".format(int(random.random()*100))
        while os.path.isfile(corpName):
            corpName = "corpus{}.txt".format(int(random.random()*100))

    # Amount of sequences
    try:
        seq = int(sys.argv[2])
    except:
        if isinstance(in1, int):
            seq = in1
        else:
            seq = 1000
    print(corpName, seq)
    createCorpus(corpName, seq)
    print("A corpus of {} sequences has been written to {}".format(seq, corpName))
