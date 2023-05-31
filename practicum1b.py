import testData as data
import math
import time
import numpy as np

inputVector = np.array([0 for i in range(9)])

outputVector = np.array([0 for i in range(2)])

weightMatrix = np.matrix([[1 for i in range(len(outputVector))] for j in range(len(inputVector))])


def setOutput():
    global outputVector
    outputVector = np.matmul(inputVector, weightMatrix)

def costFunc(outVec, modelVec):
    return sum([(lambda x: x * x) (zipped[0] - zipped[1]) for zipped in zip(outVec, modelVec)])

def computeAveragecost():
    accumaltedCost = 0
    for trainingItem in data.trainingSet:
        for i in range(data.nrOfRows):
            for j in range(data.nrOfColumns):
                np.put(inputVector, (i * 3 + j), trainingItem[0][i][j])
        print(inputVector)
        setOutput()
        print(outputVector)
        accumaltedCost += costFunc(softMax(outputVector), data.outputDict[trainingItem[1]])
    return accumaltedCost / len(data.trainingSet)

def softMax(inVec):
        squarer = lambda t: t ** 2
        vfunc = np.vectorize(squarer)
        expVec = inVec.copy()
        vfunc(expVec)
        expVec = [math.exp(inScal) for inScal in inVec]
        aSum = sum(expVec)
        return [expScal / aSum for expScal in expVec]

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
        weightMatrix.itemset((bestWeight[0], bestWeight[1]), (bestWeight[0], bestWeight[1]) + learningRate)
    print("After", itterations, "itterations, average cost =", computeAveragecost(), "(", time.time()-startTime, "s)")

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

def printWeight():
    for weights in weightMatrix:
        for weight in weights:
            print(weight)

trainNetwork(0.001)
testNetwork()
printWeight()