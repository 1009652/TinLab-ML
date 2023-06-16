import Practicum1.testData as data
import math
import time

def softMax(inVec):
        expVec = [math.exp(inScal) for inScal in inVec]
        aSum = sum(expVec)
        return [expScal / aSum for expScal in expVec]

class Node:
    def __init__(self, isHiddenLayer = False):
        self.links = []
        self.value = 0
        self.isHiddenLayer = isHiddenLayer

    def addLink(self, link):
        self.links.append(link)

    def setValue(self, value):
        self.value = value

    # Returns the value from this node, if this node is a hidden layer,
    # the sigmoid of the value is returned.
    def getValue(self):
        value = self.value
        for link in self.links:
            value += link.getValue()
        
        if(self.isHiddenLayer):
            return self.sigmoid(value)
        else:
            return value

    def sigmoid(self, x):
        return 1/(1 + math.exp(-x))

class Link:
    def __init__(self, inputNode, outputNode, weight = 0):
        self.weight = weight
        self.node = inputNode
        outputNode.addLink(self)

    def getValue(self):
        return self.node.getValue() * self.weight
    
    def setNode(self, node):
        self.node = node
    
    def setWeight(self, weight):
        self.weight = weight

class Network:
    def __init__(self):
        self.inputNodes = [[Node() for i in range(3)] for j in range(3)]
        self.hiddenNodes = [Node(True) for i in range(9)]
        self.outputNodes = [Node() for i in range(2)]
        self.links = []

        for nodes in self.inputNodes:
            for inputNode in nodes:
                for hiddenNode in self.hiddenNodes:
                    self.links.append(Link(inputNode, hiddenNode))

        for hiddenNode in self.hiddenNodes:
            for outputNode in self.outputNodes:
                self.links.append(Link(hiddenNode, outputNode))

    # Calculates the average cost of all the training set data.
    def computeAveragecost(self):
        accumaltedCost = 0
        for trainingItem in data.trainingSet:
            for iRow in range(data.nrOfRows):
                for iColumn in range(data.nrOfColumns):
                    self.inputNodes[iRow][iColumn].setValue(trainingItem[0][iRow][iColumn])
            accumaltedCost += self.costFunc(softMax([outputNode.getValue() for outputNode in self.outputNodes]), data.outputDict[trainingItem[1]])
        return accumaltedCost / len(data.trainingSet)

    # Calculates the cost of the output nodes and the target vector.
    def costFunc(self, outVec, modelVec):
        return sum([(lambda x: x * x) (zipped[0] - zipped[1]) for zipped in zip(outVec, modelVec)])

    # Calculates the softmax
    def softMax(self, inVec):
        expVec = [math.exp(inScal) for inScal in inVec]
        aSum = sum(expVec)
        return [expScal / aSum for expScal in expVec]

    # Trains the network by going over the weights increases it with the learning rate and 
    # calculating the average cost, then setting the weight back. After looping
    # over all the weights, the weight which had the biggest inpack is increased or decreased
    # with the learning rate. This continues until the average cost falls below the max cost.
    def trainNetwork(self, learningRate):
        average = 1
        bestLink = 0
        itterations = 0
        startTime = time.time()
        while(average > data.maxCost):
            bestDifference = 0
            itterations += 1
            for i in range(len(self.links)):
                self.links[i].setWeight(self.links[i].weight + learningRate)
                currentAverageCost = self.computeAveragecost()
                difference = average - currentAverageCost

                if(abs(difference) > abs(bestDifference)):
                    bestDifference = difference
                    average = currentAverageCost
                    bestLink = i

                self.links[i].setWeight(self.links[i].weight - learningRate)

            if(bestDifference > 0):
                self.links[bestLink].setWeight(self.links[bestLink].weight + learningRate)
            else:
                self.links[bestLink].setWeight(self.links[bestLink].weight - learningRate)
            print(average)  
        print("After", itterations, "itterations, average cost =", self.computeAveragecost(), "(", time.time()-startTime, "s)")
    
    #Tests the network with the test data, by setting the input nodes, and calculating
    # the cost from the cost Function, if the cost is more than 0.5 compared to the 
    # guess in the data, the cost function is calculated again relative to the opposite
    # option (so X, or O)
    def testNetwork(self):
        for testItem in data.testSet:
            for iRow in range(data.nrOfRows):
                for iColumn in range(data.nrOfColumns):
                    self.inputNodes[iRow][iColumn].setValue(testItem[0][iRow][iColumn])
            cost = self.costFunc(self.softMax([outputNode.getValue() for outputNode in self.outputNodes]), data.outputDict[testItem[1]])
            guess = testItem[1]

            if(cost > 0.5):
                if(guess == 'X'):
                    guess = 'O'
                else:
                    guess = 'X'
                cost = self.costFunc(self.softMax([outputNode.getValue() for outputNode in self.outputNodes]), data.outputDict[guess])

            for i in testItem[0]:
                print(i)

            print("Guess is:", guess, "with a certainty of", 100 - (cost * 200))
            print()

network = Network()
network.trainNetwork(0.01)
network.testNetwork()

