#!/usr/bin/env python3
import sys

# This append is to support importing the LCD library.
sys.path.append('../grovepi/Software/Python/grove_rgb_lcd')
from grove_rgb_lcd import *

def lcdInit():
    """
    Initialize LCD
    """
    setRGB(0,128,64)
    textCommand(0x01) # clear display

def writeLetter(buffer, letter):
    """
    Prints out letter on first line of lcd
    buffer - list containing string buffer
    letter - letter to overwrite first line [0:16] of buffer
    """
    paddedLetter = f'{letter: <16}'
    buffer[0:16] = paddedLetter
    _writeBuffer(buffer)

def writeMessage(buffer, message):
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

def writeIncoming(messages):
    setText("Incoming Message")
    time.sleep(0.7)
    setText("")
    buf = []
    for message in messages:
        firstLine = f"From: {message['sender']}"
        buf[0:16] = f'{firstLine: <16}'
        for j in range(len(message['message'])):
            buf[16:] = message['message'][j:]
            setText(buf)
            if j == 0:
                time.sleep(1)
            else:
                time.sleep(0.1)
            


if __name__ == '__main__':
    """
    For testing purposes only
    """
    import time
    buf = []
    writeLetter(buf, "...")
    time.sleep(0.5)
    writeMessage(buf, "S")
    time.sleep(0.5)
    writeLetter(buf, "---")
    time.sleep(0.5)
    writeMessage(buf, "SO")
    time.sleep(0.5)
    writeLetter(buf, "...")
    time.sleep(0.5)
    writeMessage(buf, "SOS")