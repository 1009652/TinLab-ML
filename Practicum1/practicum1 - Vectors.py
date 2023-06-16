import Practicum1.testData as data
import math
import time

inputVector = [0 for i in range(9)]

outputVector = [0 for i in range(2)]

weightMatrix = [[1 for i in range(len(outputVector))] for j in range(len(inputVector))]

# Calculates the output vector by multiplying the inputVector with the weightMatrix.
def setOutput():
    global outputVector
    outputVector = [0 for i in range(2)]
    for i in range(len(weightMatrix[0])):
        for j in range(len(inputVector)):
            outputVector[i] += weightMatrix[j][i] * inputVector[j]

# Calculates the cost of the output vector and the set vector.
def costFunc(outVec, modelVec):
    return sum([(lambda x: x * x) (zipped[0] - zipped[1]) for zipped in zip(outVec, modelVec)])

# Calculates the average cost of all the training set data.
def computeAveragecost():
    accumaltedCost = 0
    for trainingItem in data.trainingSet:
        for i in range(data.nrOfRows):
            for j in range(data.nrOfColumns):
                inputVector[i*3 + j] = trainingItem[0][i][j]
        setOutput()
        accumaltedCost += costFunc(softMax(outputVector), data.outputDict[trainingItem[1]])
    return accumaltedCost / len(data.trainingSet)

# Calculates the softmax
def softMax(inVec):
    expVec = [math.exp(inScal) for inScal in inVec]
    aSum = sum(expVec)
    return [expScal / aSum for expScal in expVec]

# Trains the network by going over the weights increases it with the learning rate and 
# calculating the average cost, then setting the weight back. After looping
# over all the weights, the weight which had the biggest inpack is increased or decreased
# with the learning rate. This continues until the average cost falls below the max cost.
def trainNetwork(learningRate):
    average = 1
    bestWeight = (0, 0)
    itterations = 0
    startTime = time.time()
    while(average > data.maxCost):
        itterations += 1
        for i in range(len(weightMatrix)):
            for j in range(len(weightMatrix[0])):
                weightMatrix[i][j] += learningRate
                currentAverageCost = computeAveragecost()
                if(currentAverageCost < average):
                    average = currentAverageCost
                    bestWeight = (i, j)
                
                weightMatrix[i][j] -= learningRate
        weightMatrix[bestWeight[0]][bestWeight[1]] += learningRate
    print("After", itterations, "itterations, average cost =", computeAveragecost(), "(", time.time()-startTime, "s)")

#Tests the network with the test data, by setting the input nodes, and calculating
# the cost from the cost Function, if the cost is more than 0.5 compared to the 
# guess in the data, the cost function is calculated again relative to the opposite
# option (so X, or O)
def testNetwork():
    for testItem in data.testSet:
        for i in range(data.nrOfRows):
            for j in range(data.nrOfColumns):
                inputVector[i*3 + j] = testItem[0][i][j]
        setOutput()
        cost = costFunc(softMax(outputVector), data.outputDict[testItem[1]])
        guess = testItem[1]

        if(cost > 0.5):
            if(guess == 'X'):
                guess = 'O'
            else:
                guess = 'X'
            setOutput()
            cost = costFunc(softMax(outputVector), data.outputDict[guess])

        for i in testItem[0]:
            print(i)

        print("Guess is:", guess, "with a certainty of", 100 - (cost * 200))
        print()

#Prints all the weights calculated for the neural network
def printWeight():
    for weights in weightMatrix:
        for weight in weights:
            print(weight)

trainNetwork(0.001)
testNetwork()
printWeight()