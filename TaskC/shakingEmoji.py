from sense_hat import SenseHat
from time import sleep

class imuInterface:
    def __init__(self):
        self.__sense = SenseHat()

    def getAccelerometerData(self):
        accelerometer = self.__sense.get_accelerometer_raw()
        return accelerometer

    def determineShaken(self):
        accelerometerData = self.getAccelerometerData()
        yAxis = abs(accelerometerData['y'])
        xAxis = abs(accelerometerData['x'])
        zAxis = abs(accelerometerData['z'])

        if yAxis > 2 or xAxis > 2 or zAxis > 2:
            return True
        else:
            return False

class senseHatInterface:
    def __init__(self):
        self._sense = SenseHat()

    def displayEmoji(self, emoji):
        SenseHat.set_pixels(self._sense, emoji)

    def clearHat(self):
        self._sense.clear()
        return

class emojiFormatter:
    #def __init__(self):

    def createEmojis(self):
        # matrix is 8x8
        b = (0,0,0) #black
        y = (255,255,0) #yellow
        p = (255,102,255) #pink
        pb = (150, 215, 255) #pale blue

        emoji1 = [
            y,y,y,y,y,y,y,y,
            y,y,y,y,y,y,y,y,
            y,b,b,y,y,b,b,y,
            y,b,b,y,y,b,b,y,
            y,y,y,y,y,y,y,y,
            y,p,y,y,y,y,p,y,
            y,y,p,p,p,p,y,y,
            y,y,y,y,y,y,y,y
        ]

        emoji2 = [
            y,y,y,y,y,y,y,y,
            y,b,b,y,y,b,b,y,
            y,b,b,y,y,b,b,y,
            y,pb,y,y,y,pb,y,y,
            y,y,pb,y,y,y,pb,y,
            y,y,p,p,p,p,y,y,
            y,p,y,y,y,y,p,y,
            y,y,y,y,y,y,y,y
        ]

        emojiList = [emoji1, emoji2]
        return emojiList

def main():
    try:  
        emojiController = emojiFormatter()
        emojiList = emojiController.createEmojis()
        happyEmoji = emojiList[0]
        sadEmoji = emojiList[1]

        accelerometerController = imuInterface()
        senseHatController = senseHatInterface()

        while True:
            #display happy emoji
            senseHatController.displayEmoji(happyEmoji)
            #when shaken
            if accelerometerController.determineShaken():
                #Display sad emoji
                senseHatController.displayEmoji(sadEmoji)
                sleep(2) # Show sad emoji for 2 seconds
            #Refresh back to sad emoji
    except KeyboardInterrupt:
        senseHatController.clearHat()
        print("\nExiting...")

if __name__ == "__main__":
    main()