"""
This is a program that generates a sequence of "hej", "mu", "kvack" given the probabilites below
Output is saved to a file, one line per sequence and the amount of sequences can be choosen
"""
import random

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

    # Loop thorugh states until new state is found
    for newState in stateDict[currentState].keys():
        # Add probability to sum
        stateSum += stateDict[currentState][newState]

        # If sum is bigger than number return state
        if stateSum > stateNumber:
            return newState



## These are the options for the code
####################################################################################

# All possible state transitions given current state > new state > prob of new state
stateTransitions = {'start' : {'ko' : 0.5, 'anka' : 0.5},
                    'ko' : {'ko' : 0.5, 'anka' : 0.3, 'slut' : 0.2},
                    'anka' : {'ko' : 0.3, 'anka' : 0.5, 'slut' : 0.2}}

# All possible observations given current state > observation > probability of observation
observations = {'ko' : {'hej' : 0.1, 'mu' : 0.9},
                'anka' : {'hej' : 0.4, 'kvack' : 0.6}}

# Number of lines (sequences in file)
numberOfSequences = 10

# Filename to print to
outputFileName = "kvackMu.txt"

#######################################################################################


# This runs the code

outputFile = open(outputFileName, 'w')

for i in range(numberOfSequences):
    # Startint state and sequence
    state = 'start'
    sequence = ""

    # Create new sequence
    while state != 'slut':
        state = randomState(stateTransitions, state)
        if state != 'slut':
            sequence += randomState(observations, state) + " "
    
    # Write sequence to file
    outputFile.write(sequence + "\n")

# Close file
outputFile.close()
