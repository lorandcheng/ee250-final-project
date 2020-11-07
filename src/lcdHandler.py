#!/usr/bin/env python3
import sys
import threading
import time
# This append is to support importing the LCD library.
sys.path.append('../grovepi/Software/Python/grove_rgb_lcd')
from grove_rgb_lcd import *

def lcdInit():
    """
    Initialize LCD
    """
    textCommand(0x01) # clear display

def addLetter(buffer, letter):
    """
    Prints out letter on first line of lcd
    buffer - list containing string buffer
    letter - letter to overwrite first line [0:16] of buffer
    """
    paddedLetter = f'{letter: <16}'
    buffer[0:16] = paddedLetter
    _writeBuffer(buffer)

def addMessage(buffer, message):
    """
    Prints out message on second line of lcd
    buffer - list containing string buffer
    message - message to overwrite second line [16:] of buffer
    """
    buffer[16:] = message
    _writeBuffer(buffer)


def _writeBuffer(buffer):
    """
    Writes the contents of the buffer to the LCD
    """
    if len(buffer) < 32:
        lcdOutput = buffer
    else:
        lcdOutput = buffer[:16]+buffer[-16:]
    setText(lcdOutput)



if __name__ == '__main__':
    """
    For testing purposes only
    """
    buf = []
    addLetter(buf, "...")
    time.sleep(0.5)
    addMessage(buf, "S")
    time.sleep(0.5)
    addLetter(buf, "---")
    time.sleep(0.5)
    addMessage(buf, "SO")
    time.sleep(0.5)
    addLetter(buf, "...")
    time.sleep(0.5)
    addMessage(buf, "SOS")