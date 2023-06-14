import testData as data

import pandas as pd

# import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler


from sklearn.neural_network import MLPClassifier

# from sklearn.metrics import accuracy_score
# from sklearn.metrics import plot_confusion_matrix
# from sklearn.metrics import classification_report

# from sklearn.model_selection import GridSearchCV

trainX = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7', '8'])
trainY = pd.DataFrame(columns=['value'])

testX = trainX.copy()
testY = trainY.copy()


values = []

for trdata in data.trainingSet:
    for i in range(len(trdata[0])):
        for j in range(len(trdata[0][i])):
            values.append(trdata[0][i][j])
    trainX.loc[len(trainX)] = values
    trainY.loc[len(trainY)] = [trdata[1]]
    values = []

for trdata in data.testSet:
    for i in range(len(trdata[0])):
        for j in range(len(trdata[0][i])):
            values.append(trdata[0][i][j])
    testX.loc[len(testX)] = values
    testY.loc[len(testY)] = [trdata[1]]
    values = []

#trainX, testX, trainY, testY = train_test_split(x, y, test_size = 0.2)

mlp_clf = MLPClassifier(hidden_layer_sizes=(150,100,50),
                        max_iter = 300,activation = 'relu',
                        solver = 'adam')

mlp_clf.fit(trainX, trainY)

y_pred = mlp_clf.predict(testX)



for i in range(7):
    for j in range(3):
        for k in range(3):
            print(testX.iat[i, j*3+k], end= '')
        print()
    print(y_pred[i])
#print(testX.iat[3, 0])
#print(y_pred)


