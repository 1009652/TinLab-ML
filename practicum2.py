from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np


class Scraper():
    def __init__(self):
        self.df = None
        self.fileName = "Medical Information"

    def fillData(self):
        print("Filling DataTable")
        self.driver = webdriver.Chrome()
        self.driver.get("https://wiztech.nl/mitw/mcr/data_generator.html")
        self.table = self.driver.find_element(By.XPATH, "//table")
        self.rows = self.table.find_elements(By.TAG_NAME, "tr")

        for row in self.rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            dataRow = []

            for col in cols:
                if(self.df is None):
                    dataRow.append(col.text)
                else:
                    dataRow.append(float(col.text))
            
            if(self.df is None):
                self.df = pd.DataFrame(columns=dataRow)
            else:
                self.df.loc[len(self.df)] = dataRow
        
        print(self.df)
        self.df.to_csv(self.fileName, index=False)

    
    def regression(self):
        try:
            self.df = pd.read_csv(self.fileName)
        except:
            self.fillData()

        target = ['lifespan']
        y = self.df[target]
        X = self.df.drop(target, axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

        self.model = MLPRegressor()
        self.model.fit(X_train, y_train)
        expected_y = y_test
        predicted_y = self.model.predict(X_test)

        print(expected_y.values.tolist())
        print(predicted_y)
    
        df_temp = pd.DataFrame({'Actual': expected_y['lifespan'].values.tolist(), 'Predicted': predicted_y})
        df_temp.head()

        df_temp = df_temp.head(30)
        df_temp.plot(kind='bar',figsize=(10,6))
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        plt.show()

    def applyModel(self):
        info = self.df.columns
        data = []
        print("Fll in the values asked for.")
        for i in range(len(info) - 1):
            cont = False
            while(not cont):
                print(info[i], ":")
                inp = input()
                try:
                    data.append(float(inp))
                    cont = True
                except:
                    print("Please fill in valid info")

        predict = self.model.predict([data])
        print("you will roughly be", predict[0])

scraper = Scraper()
#scraper.fillData()
scraper.regression()
scraper.applyModel()