import testData as data
import math
import time
import numpy as np

inputVector = np.array([0 for i in range(9)])

outputVector = np.array([0 for i in range(2)])

weightMatrix = np.matrix([[1 for i in range(len(outputVector))] for j in range(len(inputVector))])

# Calculates the output vector by multiplying the inputVector with the weightMatrix.
def setOutput():
    global outputVector
    outputVector = np.dot(inputVector, weightMatrix)

# Calculates the cost of the output vector and the set vector.
def costFunc(outVec, modelVec):
    return sum([(outVec[i] - modelVec[i]) ** 2 for i in range(len(outVec))])

# Calculates the sigmoid
def sigmoid(inVec):
    return [(1/(1 + np.exp(-inVec.item(x)))/2) for x in range(len(inVec) + 1)]

# Calculates the average cost of all the training set data.
def computeAveragecost():
    accumaltedCost = 0
    for trainingItem in data.trainingSet:
        for i in range(data.nrOfRows):
            for j in range(data.nrOfColumns):
                np.put(inputVector, (i * 3 + j), trainingItem[0][i][j])
        setOutput()
        accumaltedCost += costFunc(sigmoid(outputVector), data.outputDict[trainingItem[1]])
    return accumaltedCost / len(data.trainingSet)

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
                weightMatrix.itemset((i, j), weightMatrix.item(i, j) + learningRate)
                currentAverageCost = computeAveragecost()
                if(currentAverageCost < average):
                    average = currentAverageCost
                    bestWeight = (i, j)
                
                weightMatrix.itemset((i, j), weightMatrix.item(i, j) - learningRate)
        weightMatrix.itemset((bestWeight[0], bestWeight[1]), weightMatrix.item(bestWeight[0], bestWeight[1]) + learningRate)
        print(average)
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
        cost = costFunc(sigmoid(outputVector), data.outputDict[testItem[1]])
        guess = testItem[1]

        if(cost > 0.5):
            if(guess == 'X'):
                guess = 'O'
            else:
                guess = 'X'
            setOutput()
            cost = costFunc(sigmoid(outputVector), data.outputDict[guess])

        for i in testItem[0]:
            print(i)

        print("Guess is:", guess, "with a certainty of", 100 - (cost * 200))
        print()

#Prints all the weights calculated for the neural network
def printWeight():
    for weights in weightMatrix:
        for weight in weights:
            print(weight)

trainNetwork(0.1)
testNetwork()
printWeight()