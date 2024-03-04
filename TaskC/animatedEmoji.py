from time import sleep
from sense_hat import SenseHat

class emojiFormatter:

    def createEmojis(self):
        # matrix is 8x8
        b = (0,0,0) #black
        w = (255,255,255) #white
        y = (255,255,0) #yellow
        p = (255,102,255) #pink
        r = (255,0,0) #red
        br = (102,51,0) #brown
        lbr = (153,76,0) #light brown
        pb = (150, 215, 255) #pale blue

        emoji1 = [ # Happy Emoji
            y,y,y,y,y,y,y,y,
            y,y,y,y,y,y,y,y,
            y,b,b,y,y,b,b,y,
            y,b,b,y,y,b,b,y,
            y,y,y,y,y,y,y,y,
            y,p,y,y,y,y,p,y,
            y,y,p,p,p,p,y,y,
            y,y,y,y,y,y,y,y
        ]

        emoji2 = [ # Crying Emoji
            y,y,y,y,y,y,y,y,
            y,b,b,y,y,b,b,y,
            y,b,b,y,y,b,b,y,
            y,pb,y,y,y,pb,y,y,
            y,y,pb,y,y,y,pb,y,
            y,y,p,p,p,p,y,y,
            y,p,y,y,y,y,p,y,
            y,y,y,y,y,y,y,y
        ]

        emoji3 = [ # Clown Emoji
            w,w,w,w,w,w,w,w,
            w,w,pb,w,w,pb,w,w,
            w,w,b,w,w,b,w,w,
            w,w,w,r,r,w,w,w,
            w,w,w,r,r,w,w,w,
            w,r,w,w,w,w,r,w,
            w,w,r,r,r,r,w,w,
            w,w,w,w,w,w,w,w
        ]

        emoji4 = [ # Poop Emoji
            w,w,w,w,w,w,w,w,
            w,w,w,br,br,w,w,w,
            w,w,br,br,br,br,w,w,
            w,br,w,br,br,w,br,w,
            br,br,b,br,br,b,br,br,
            br,lbr,br,br,br,br,lbr,br,
            br,br,lbr,lbr,lbr,lbr,br,br,
            br,br,br,br,br,br,br,br
        ]

        emoji5 = [ # Cool Emoji
            y,y,y,y,y,y,y,y,
            b,b,b,y,y,b,b,b,
            y,b,b,b,b,b,b,y,
            y,b,b,b,b,b,b,y,
            y,y,y,y,y,y,y,y,
            y,p,y,y,y,y,p,y,
            y,y,p,p,p,p,y,y,
            y,y,y,y,y,y,y,y
        ]

        emojiList = [emoji1, emoji2, emoji3, emoji4, emoji5]
        return emojiList

class senseHatInterface:
    def __init__(self):
        self._sense = SenseHat()

    def displayEmoji(self, emoji):
        SenseHat.set_pixels(self._sense, emoji)

    def clearHat(self):
        self._sense.clear()
        return

def main():
    try:
        emojiController = emojiFormatter()
        emojiList = emojiController.createEmojis() # Get list of emoji matricies
        senseHatController = senseHatInterface()
        while True:
            for emoji in emojiList: # Loop through list of emojis
                senseHatController.displayEmoji(emoji) # Print emoji onto hat
                sleep(2) #sleep for 2 seconds
            #Print next emoji
    except KeyboardInterrupt:
        senseHatController.clearHat()
        print("\nExiting...")

if __name__ == '__main__':
    main()