#!/usr/bin/env python3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# Author: Lorand Cheng https://github.com/lorandcheng
# Date: Nov 15, 2020
# Project: USC EE250 Final Project, Morse Code Translator and Messenger
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import sys

# This append is to support importing the LCD library.
sys.path.append('../grovepi/Software/Python/grove_rgb_lcd')
from grove_rgb_lcd import *

def lcdInit():
    """
    Summary: Initialize LCD
    """
    
    setRGB(0,128,64)
    textCommand(0x01) # clear display

def writeLetter(buffer, letter):
    """
    Summary: Prints out letter on first line of lcd
    Args:
        buffer (list): list containing string buffer
        letter (string): letter to overwrite first line [0:16] of buffer
    """

    paddedLetter = f'{letter: <16}'
    buffer[0:16] = paddedLetter
    _writeBuffer(buffer)

def writeMessage(buffer, message):
    """
    Summary: Prints out message on second line of lcd
    Args:
        buffer (list): list containing string buffer
        message (string): message to overwrite second line [16:] of buffer
    """

    buffer[16:] = message
    _writeBuffer(buffer)


def _writeBuffer(buffer):
    """
    Summary: Writes the contents of the buffer to the LCD
    Args:
        buffer(list: list containing string buffer
    """

    if len(buffer) < 32:
        lcdOutput = buffer
    else:
        lcdOutput = buffer[:16]+buffer[-16:]
    setText(lcdOutput)

def writeIncoming(messages):
    """
    Summary: displays incoming message on the LCD, scrolling the second line to show the full message
    Args:
        messages (list): list of message objects with fields 'sender' and 'message' required
    """

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
                time.sleep(2)
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