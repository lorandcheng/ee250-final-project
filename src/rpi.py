#!/usr/bin/env python3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# Author: Lorand Cheng https://github.com/lorandcheng
# Date: Nov 15, 2020
# Project: USC EE250 Final Project, Morse Code Translator and Messenger
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import time
import sys
import threading

from constants import *
from lcdHandler import *
from messageHandler import messageHandler
from messageNotifier import Notifier
from morseCode import Morse_Code_Bin_Tree

# GrovePi Modules
sys.path.append('../grovepi/Software/Python/')
import grovepi
grovepi.pinMode(BUTTON,"INPUT")
grovepi.pinMode(LED,"OUTPUT")
grovepi.pinMode(BUZZER,"OUTPUT")
# LCD connected to I2C port
lcdInit()
lock = threading.Lock() #define I2C lock

#Declare message tools
morse = Morse_Code_Bin_Tree() # morse code translator
letter = "" # string containing morse code for one letter
message = "" # string containing letters in message
received = [] # list of received messages
buf = [] # buffer for storing letter and message

def duringPause(duration, done):
    """
    Summary: Either end the current letter or insert a space depending on the duration of the pause and what's already been done
    Args:
        duration (time in seconds): duration of pause
        done (int): number of actions that have already been done
    """

    global message
    global letter
    global buf
    global lock
    global END
    global SPACE
    # Determine action
    if done == 0: # no action has been done
        if END < duration <= SPACE:
            try:
                message += morse.translate_mc_to_letter(letter)
            except TypeError:
                print("Unable to translate letter")
            print("end of letter:", morse.translate_mc_to_letter(letter))
            with lock:
                writeLetter(buf, " ")
                writeMessage(buf, message)
            letter = ""
            return 1
        else:
            return 0
    elif done == 1: # letter has ended
        if SPACE < duration:
            message += " "
            with lock:
                writeLetter(buf, "Space")
                writeMessage(buf, message)
            print("space")
            return 2 # space has been added
        else:
            return 1
    else:
        return 2

def afterPress(duration):
    """
    Summary: Either add a dot/dash to the current letter depending on the duration of the press
    Args:
        duration (time in seconds): duration of press
    """

    global letter
    global lock
    global DASH
    global SEND
    # Determine action
    if duration < DASH:
        letter += "."
        print(".")
    elif DASH <= duration < SEND:
        letter+= "-"
        print("-")
    with lock:
        writeLetter(buf, letter)

def buttonPressed():
    """
    Summary: read button value
    """

    with lock:
        return grovepi.digitalRead(BUTTON)

def alert(replay):
    """
    Summary: flash LED and play buzzer to alert for incoming message
    Args:
        replay (boolean): indicates whether this is a replayed message
    """

    with lock:
        grovepi.digitalWrite(LED,1)
        if not replay:
            for i in range(3):
                grovepi.digitalWrite(BUZZER,1)
                time.sleep(0.1)
                grovepi.digitalWrite(BUZZER,0)
                time.sleep(0.1)
        writeIncoming(received)
        grovepi.digitalWrite(LED,0)

if __name__ == '__main__':

    # initialize state machine variables
    timerStart = 0 # time of last event
    state = 0 # 0 button is not pressed, 1 button is pressed, 2 message sent
    done = 0 # action counter
    messageClient = messageHandler("rpi",SERVER) # for handling message sending
    notifier = Notifier(messageClient,1) # for message notifications
    replay = False # flag for determining whether message is replay
    while True:
        try:
            elapsedTime = time.time()-timerStart # calculate time since last transition

            # if there is an incoming message
            if len(notifier.getMessages()) != 0:
                received = notifier.getMessages()
                print("Incoming message",received)
                notifier.markMessagesRead()
                state = 2
                index = 0

            # button is not pressed
            if state == 0:
                if buttonPressed():
                    state = 1
                    timerStart = time.time() # reset timer
                    done = 0 # reset action counter
                elif timerStart != 0 and done != 2: # if this is not the first time and there are still actions to be done
                    done = duringPause(elapsedTime, done)

            # button is pressed
            elif state == 1:
                # on release
                if not buttonPressed():
                    state = 0
                    timerStart = time.time() # reset timer
                    afterPress(elapsedTime)
                    done = 0 # reset action counter
                # on send
                elif SEND < elapsedTime and not done:
                    state = 0
                    writeLetter(buf, "Message Sending")
                    print("Message Sending:" + message)
                    success = messageClient.sendMessage(message)
                    time.sleep(2)
                    if success:
                        writeLetter(buf, "Message Sent!")
                    else:
                        writeLetter(buf, "Message Failed!")
                        print("Message Failed!")
                    time.sleep(1)
                    lcdInit()
                    message = ""
                    buf = []
                    done = 0
                    timerStart = 0

            # message received
            elif state == 2:
                alert(replay)
                with lock:
                    writeLetter(buf, "Hold button")
                    writeMessage(buf, "to replay")
                time.sleep(1)
                if(buttonPressed()):
                    replay = True
                else:
                    replay = False
                    writeLetter(buf, " ")
                    writeMessage(buf, message)
                    state = 0
                    letter = ""
                    buf = []
                    done = 0
                    timerStart = 0


        #Graceful shutdown
        except KeyboardInterrupt:
            try:
                with lock:
                    setRGB(0, 0, 0)
                    textCommand(0x01)
                    #TODO turn off led and buzzer
                    break
            except:
                pass
            

        # retry after LCD error
        except IOError as err:
            if str(err) == '121':
                time.sleep(0.25)
            else:
                raise
