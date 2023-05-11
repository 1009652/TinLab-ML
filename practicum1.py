import testData as data
import math
import time

class Node:
    def __init__(self):
        self.links = []
        self.value = 0

    def addLink(self, link):
        self.links.append(link)

    def setValue(self, value):
        self.value = value

    def getValue(self):
        value = self.value
        for link in self.links:
            value += link.getValue()
        
        return value

    def sigmoid(self, x):
        return 1/(1 + math.exp(-x))

class Link:
    def __init__(self, inputNode, outputNode, weight = 1):
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
        self.outputNodes = [Node() for i in range(2)]
        self.links = []

        for nodes in self.inputNodes:
            for inputNode in nodes:
                for outputNode in self.outputNodes:
                    self.links.append(Link(inputNode, outputNode))

    def computeAveragecost(self):
        accumaltedCost = 0
        for trainingItem in data.trainingSet:
            for iRow in range(data.nrOfRows):
                for iColumn in range(data.nrOfColumns):
                    self.inputNodes[iRow][iColumn].setValue(trainingItem[0][iRow][iColumn])

            accumaltedCost += self.costFunc(self.softMax([outputNode.getValue() for outputNode in self.outputNodes]), data.outputDict[trainingItem[1]])
        return accumaltedCost / len(data.trainingSet)

    def costFunc(self, outVec, modelVec):
        return sum([(lambda x: x * x) (zipped[0] - zipped[1]) for zipped in zip(outVec, modelVec)])

    def softMax(self, inVec):
        expVec = [math.exp(inScal) for inScal in inVec]
        aSum = sum(expVec)
        return [expScal / aSum for expScal in expVec]

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
                
        print("After", itterations, "itterations, average cost =", self.computeAveragecost(), "(", time.time()-startTime, "s)")
    
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

    def printWeight(self):
        for link in self.links:
            print(link.weight)

network = Network()
network.trainNetwork(0.001)
network.testNetwork()
network.printWeight()