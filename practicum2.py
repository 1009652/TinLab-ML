from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np


class Scraper():
    def __init__(self):
        self.data = np.array([])
        self.numOfRows = 0
        self.numOfCol = 0
        self.driver = webdriver.Chrome()
        self.driver.get("https://wiztech.nl/mitw/mcr/data_generator.html")

    def fillData(self):
        self.table = self.driver.find_element(By.XPATH, "//table")
        self.rows = self.table.find_elements(By.TAG_NAME, "tr")

        for row in self.rows:
            self.numOfRows += 1
            dataRow = np.array([])
            cols = row.find_elements(By.TAG_NAME, "td")

            for col in cols:
                self.numOfCol += 1
                np.append(dataRow, col.text)
                print(col.text)

            np.append(self.data, dataRow)

        self.numOfCol = self.numOfCol / self.numOfRows
    
    def transformData(self):
        self.xData = []
        self.yData = []

        for i in range(self.numOfRows):
            for j in range(self.numOfCol):
                pass

scraper = Scraper()
scraper.fillData()