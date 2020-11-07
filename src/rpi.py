#!/usr/bin/env python3
import time
import sys
import threading

from lcdHandler import *
#from messageHandler import *

# GrovePi Modules
sys.path.append('../grovepi/Software/Python/')
import grovepi

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

# Define press lengths (s)
DASH = 0.3
SEND = 3

# Define pause lengths (s)
END = 1
SPACE = 3


def duringPause(duration, done):
    """
    Either end the current letter or insert a space depending on the duration of the pause and what's already been done
    """
    global message
    global letter
    global END
    global SPACE
    # Determine action
    if done == 0: # no action has been done
        if END < duration <= SPACE:
            try:
                message += morse.translate_mc_to_letter(letter)
            except TypeError:
                print("Unable to translate letter")
            print("end of letter:", letter)
            letter = ""
            return 1
        else:
            return 0
    elif done == 1: # letter has ended
        if SPACE < duration:
            message += " "
            print("space")
            return 2 # space has been added
        else:
            return 1
    else:
        return 2
            

def afterPress(duration):
    """
    Either add a dot/dash to the current letter depending on the duration of the press
    """
    global letter
    global DASH
    global SEND
    # Determine action
    if duration < DASH:
        letter += "."
        print(".")
    elif DASH <= duration < SEND:
        letter+= "-"
        print("-")

def buttonPressed():
    """
    read button value
    """
    with lock:
        return grovepi.digitalRead(BUTTON)


if __name__ == '__main__':

    # initialize state machine variables
    timerStart = 0 # time of last event
    state = 0 # 0 button is not pressed, 1 button is pressed, 2 message sent
    done = 0
    
    while True:
        elapsedTime = time.time()-timerStart # calculate time since last transition
        
        # button is not pressed
        if state == 0: 
            if buttonPressed():
                state = 1
                timerStart = time.time() # reset timer
                done = 0 # reset action counter
            elif timerStart != 0 and done != 2:
                done = duringPause(elapsedTime, done)
                
        # button is pressed        
        elif state == 1: 
            if not buttonPressed():
                state = 0
                timerStart = time.time() # reset timer
                afterPress(elapsedTime)
                done = 0 # reset action counter
            elif SEND < elapsedTime and not done:
                state = 0
                print("Message Sending:"+ message)
                time.sleep(2)
                print("Message Sent!")
                message = ""
                done = 0
                timerStart = 0
                
        # message received       
        elif state == 2:
            pass