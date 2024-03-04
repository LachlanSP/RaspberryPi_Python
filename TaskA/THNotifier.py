import os
import sys
import json
import time
import sqlite3 as lite
import datetime
from sense_hat import SenseHat

class jsonReader:
    def __init__(self, fileName):
        self._file = fileName

    def readJSON(self):
        requiredFields = ["cold_temperature_upper_limit", "comfortable_temperature_range", "hot_temperature_lower_limit",
                          "dry_humidity_upper_limit", "comfortable_humidity_range", "wet_humidity_lower_limit"]
        file = open(file=self._file, mode="r", encoding='utf-8').read()
        jsonData = json.loads(file)
        for field in requiredFields: # Validate all fields are valid
            if field not in jsonData:
                raise ValueError("Required JSON field missing: " + field)
        return jsonData

class environmentReader:
    def __init__(self):
        self._sense = SenseHat()

    def getTemperature(self):
        cpuTemp = os.popen("vcgencmd measure_temp").readline() # Capture current CPU temperature
        cpuTemp = float(cpuTemp.replace("temp=","").replace("'C\n","")) # Reformat temperature as float

        humidTemp = self._sense.get_temperature_from_humidity()
        pressureTemp = self._sense.get_temperature_from_pressure()

        avgTemp = (humidTemp + pressureTemp)/2 # Determine average temperature from humidity and pressure sensors
        correctedTemp = avgTemp - ((cpuTemp - avgTemp) / 1.5) # Calculate calibrated temperature

        return round(correctedTemp)


    def getHumidity(self):
        currentHumidity = round(self._sense.get_humidity())
        return currentHumidity

class databaseInterface:
    def __init__(self, fileName):
        self._file = fileName
        self._tableName = "ENVIRONMENT_DATA"

    def createTable(self):
        connection = lite.connect(self._file)
        cursor = connection.cursor()
        query= "CREATE TABLE IF NOT EXISTS "+self._tableName+"(timestamp DATETIME, temperature NUMERIC, humidity NUMERIC)"
        cursor.execute(query)
        connection.commit()
        connection.close()

    def insertData(self, environmentData):
        connection = lite.connect(self._file)
        cursor = connection.cursor()

        timestamp = environmentData['dateTime']
        temperature = environmentData['temp']
        humidity = environmentData['humidity']

        query="INSERT INTO "+self._tableName+" (timestamp, temperature, humidity) values(?, ?, ?)"
        cursor.execute(query, (timestamp, temperature, humidity))
        connection.commit()
        connection.close()

class senseHatInterface:
    def __init__(self, colourDict):
        self._sense = SenseHat()
        self._colourDict = colourDict

    def clearHat(self):
        self._sense.clear()

    def determineHumidityColour(self, value):
        colour = None
        if value > int(self._colourDict['wet_humidity_lower_limit']): # if humidity is 'wet'
            colour = [0, 0, 255] # set humidity colour to blue
        elif value < int(self._colourDict['dry_humidity_upper_limit']): # if humidity is 'dry'
            colour = [128, 0, 128] # set humidity colour to purple
        else: # if humidity is 'comfortable'
            colour = [0, 255, 0] # set humidity colour to green
        return colour

    def determineTempColour(self, temp):
        colour = None
        if temp > int(self._colourDict['hot_temperature_lower_limit']): # if temperature is 'hot'
            colour = [255, 0, 0] # set temp colour to red
        elif temp < int(self._colourDict['cold_temperature_upper_limit']): # if temperature is 'cold'
            colour = [128, 128, 128] # set temp colour to grey
        else: # if temperature is 'comfortable'
            colour = [0, 255, 0] # set temp colour to green
        return colour

    def displayTemperature(self, temperature):
        colour = self.determineTempColour(temperature)
        message = "T" + str(temperature)
        self._sense.show_message(text_string=message, scroll_speed=0.15, text_colour=colour)
    
    def displayHumidity(self, humidity):
        colour = self.determineHumidityColour(humidity)
        message = "H" + str(humidity)
        self._sense.show_message(text_string=message, scroll_speed=0.15, text_colour=colour)


def main():
    configLocation = "config.json"
    try:
        fileReader = jsonReader(configLocation)
        jsonData = fileReader.readJSON() # Retrieve config file data
    except FileNotFoundError as error: # Handle missing file error
        print("ERROR: Could not find file at filepath", configLocation)
        print(error)
        sys.exit(1) # Exit if fields missing from config file
    except json.JSONDecodeError as error: # Handle JSON error
        print("An error occured when attempting to read the JSON file")
        print(error)
        sys.exit(1) # Exit if fields missing from config file
    except ValueError as error:
        print(error)
        sys.exit(1) # Exit if fields missing from config file
    except Exception as error: # Final catch-all for unexpected errors
        print("An expected error occured")
        print(error)
        sys.exit(1) # Exit if fields missing from config file

    dbInterface = databaseInterface("environment.db")
    dbInterface.createTable()
    hatController = senseHatInterface(jsonData)
    conditionReader = environmentReader()
    
    while True:
        try:
            currentTime = datetime.datetime.now().strftime("%d/%m/%y-%H:%M:%S")
            currentTemperature = conditionReader.getTemperature()
            currentHumidity = conditionReader.getHumidity()

            hatController.displayTemperature(currentTemperature)
            hatController.displayHumidity(currentHumidity)
            dataDict = {"dateTime": currentTime, "temp": currentTemperature, "humidity": currentHumidity}

            dbInterface.insertData(dataDict) # Pass environmental data for insertion to database
            time.sleep(5)
        except KeyboardInterrupt: # Handle clean exit via ctrl+c
            hatController.clearHat()
            print("\nExitng...")
            break
        
if __name__ == '__main__':
    main()
