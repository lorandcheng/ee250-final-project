import time
import sys
import threading
#import messageHandler

sys.path.append('../grovepi/Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../grovepi/Software/Python/grove_rgb_lcd')

# GrovePi Modules
import grovepi
import grove_rgb_lcd

#Declare message tools
from morseCode import Morse_Code_Bin_Tree, Node
letter = ""
message = ""
morse = Morse_Code_Bin_Tree()


"""
Declare port numbers, initialize pins, create lock
"""
LED = 1 #D1
grovepi.pinMode(LED,"OUTPUT")
BUTTON = 3 #D3
grovepi.pinMode(BUTTON,"INPUT")
# LCD connected to I2C port
grove_rgb_lcd.textCommand(0x01) # Clear display
lock = threading.Lock() #define I2C lock




def actAfterPause(duration):
    """
    Either end the current letter or insert a space depending on the duration of the pause
    """
    global message
    global letter
    # Define pause lengths (s)
    END = 1
    SPACE = 3
    # Determine action
    if END < duration <= SPACE:
        message += morse.translate_mc_to_letter(letter)
        letter = ""
        print("end of letter")
    elif SPACE < duration:
        message += " "
        print("space")

def actAfterPress(duration):
    """
    Either add a dot/dash to the current letter, or send the message depending on the duration of the press
    """
    global letter
    # Define press lengths (s)
    DASH = 0.4
    SEND = 3
    # Determine actino
    if duration < DASH:
        letter += "."
        print(".")
    elif DASH <= duration < SEND:
        letter+= "-"
        print("-")
    elif SEND < duration:
        print(message)
        message = ""

def buttonPressed():
    """
    read button value
    """
    with lock:
        return grovepi.digitalRead(BUTTON)


if __name__ == '__main__':
    # initialize timer variables
    pressStart = 0
    pressDuration = 0
    pauseStart = 0
    pauseDuration  = 0
    # loop forever
    while True:
        # if the button was pressed
        if buttonPressed():
            pressStart = time.time() # start button timer
            if pauseStart:
                pauseDuration = time.time()-pauseStart # calculate length of pause
                actAfterPause(pauseDuration)
            while buttonPressed():
                pass
            pressDuration = time.time()-pressStart # calculate length of press
            actAfterPress(pressDuration)
            pauseStart = time.time() # start pause timer