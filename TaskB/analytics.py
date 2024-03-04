import os
import sqlite3 as sqlite
import pandas
from matplotlib import pyplot
from matplotlib.dates import DateFormatter
import seaborn

class databaseInterface:
    def __init__(self, filename):
        self._file = filename
        self._tableName = "ENVIRONMENT_DATA"

    def retrieveAllData(self):
        connection = sqlite.connect(self._file)
        timestampColumn = ['timestamp']
        query = "SELECT * FROM "+self._tableName
        dataframe = pandas.read_sql(query, connection, parse_dates=timestampColumn)
        return dataframe

class graphingInterface():

    def createCountPlot(self, data):
        pyplot.figure(figsize=(10,6))
        seaborn.countplot(data=data, y='humidity')
        pyplot.title("Humidity Frequency Distribution")
        pyplot.ylabel("Humidity (%)")
        pyplot.show()

    def createHistogram(self, data):
        pyplot.figure(figsize=(10,6))
        seaborn.histplot(x='temperature', data=data, hue='temperature', discrete=True, stat="count", label="Temperature")
        pyplot.xlabel("Temperature (C)")
        pyplot.title("Temperature Frequency Distribution")
        pyplot.show()

    def createScatterplot(self, data):
        #create chart and two y-axes
        figure, leftAxis = pyplot.subplots(figsize=(10, 6))
        rightAxis = leftAxis.twinx()
        #Temperature on the left axis
        seaborn.scatterplot(x='timestamp', y='temperature', data=data, ax=leftAxis, color='tab:red', legend=False)
        leftAxis.set_ylabel('Temperature (C)', color='tab:red')
        #humidity on the right axis
        seaborn.scatterplot(x='timestamp', y='humidity', data=data, ax=rightAxis, color='tab:blue', legend=False)
        rightAxis.set_ylabel('Humidity (%)', color='tab:blue')
        #format date in HH:MM
        dateFormatter = DateFormatter('%H:%M')
        leftAxis.xaxis.set_major_formatter(dateFormatter) 
        pyplot.title('Temperature and Humidity Scatterplot\n(19/08/2023)')
        pyplot.xlabel("Time")
        pyplot.show()

    def createLineChart(self, data):
        #create chart and two y-axes
        figure, leftAxis = pyplot.subplots(figsize=(10, 6))
        rightAxis = leftAxis.twinx()
        #Temperature on left axis
        seaborn.lineplot(x='timestamp', y='temperature', data=data, ax=leftAxis, color='tab:red', legend=False)
        leftAxis.set_ylabel('Temperature (C)', color='tab:red')
        leftAxis.legend(loc='upper left')
        #humidity on right axis
        seaborn.lineplot(x='timestamp', y='humidity', data=data, ax=rightAxis, color='tab:blue', legend=False)
        rightAxis.set_ylabel('Humidity (%)', color='tab:blue')
        rightAxis.legend(loc='upper right')
        #format date in HH:MM (no date)
        dateFormatter = DateFormatter('%H:%M')
        leftAxis.xaxis.set_major_formatter(dateFormatter) 
        pyplot.xlabel("Time")
        pyplot.title('Temperature and Humidity Line Chart\n(19/08/2023)') 
        pyplot.show()


class dataManipulator():
    def __init__(self, allData):
        self._allData = allData

    def filterDataframe(self, date): # filter data down to a given date
        filteredDate = pandas.to_datetime(date).date()
        filteredData = self._allData[self._allData['timestamp'].dt.date == filteredDate]
        print(filteredData)
        return filteredData

def main():
    currentPath = os.path.realpath(__file__)
    directory = os.path.dirname(currentPath)
    directory = directory.replace('TaskB', 'TaskA')
    os.chdir(directory)
    dbPath = 'environment.db'
    databaseController = databaseInterface(dbPath)
    allData = databaseController.retrieveAllData() # Dataframe of all data
    dataTransformer = dataManipulator(allData)
    filteredData = dataTransformer.filterDataframe('19/08/23') #Data filtered down to provided date
    grapher = graphingInterface()
    grapher.createLineChart(filteredData)
    grapher.createScatterplot(filteredData)
    grapher.createHistogram(allData)
    grapher.createCountPlot(allData)

if __name__ == "__main__":
    main()