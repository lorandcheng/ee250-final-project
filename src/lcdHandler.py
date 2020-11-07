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

def addLetter(buffer, letter, lock):
    """
    Prints out letter on first line of lcd
    """
    paddedLetter = f'{letter: <16}'
    buffer[0:16] = paddedLetter
    _writeBuffer(buffer, lock)

def addMessage(buffer, message, lock):
    """
    Prints out message on second line of lcd
    """
    buffer[16:] = message
    _writeBuffer(buffer, lock)


def _writeBuffer(buffer, lock):
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
    lock = threading.Lock() #define I2C lock
    buf = []
    addLetter(buf, "...", lock)
    time.sleep(0.5)
    addMessage(buf, "S", lock)
    time.sleep(0.5)
    addLetter(buf, "---", lock)
    time.sleep(0.5)
    addMessage(buf, "SO", lock)
    time.sleep(0.5)
    addLetter(buf, "...", lock)
    time.sleep(0.5)
    addMessage(buf, "SOS", lock)