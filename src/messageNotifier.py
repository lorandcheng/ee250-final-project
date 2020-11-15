#!/usr/bin/env python3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# Author: Lorand Cheng https://github.com/lorandcheng
# Date: Nov 15, 2020
# Project: USC EE250 Final Project, Morse Code Translator and Messenger
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import threading
import time
import pytz
from messageHandler import messageHandler
from datetime import datetime

def convertDatetimeTz(dt, tz1, tz2):
    """
    Summary: converts datetime from one timezone to another
    Args:
        dt (str): datetime to be converted
        tz1 (pytz timezone): initial timezone
        tz2 (pytz timezone): destination timezone
    """
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    dt = datetime.strptime(dt,"%Y-%m-%d %H:%M:%S.%f")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    return dt

class Notifier():
    def __init__(self, messageHandler, increment):
        """
        Summary: Class for checking incoming messages

        Args:
            messageHandler (messageHandler object): messageHandler to send the get requests
            increment (int): time delay in seconds between get requests
        """
        self.messageHandler = messageHandler
        self.next_t = time.time()
        self.incomingMessages = []
        self.lastRead = str(convertDatetimeTz(str(datetime.now()),'America/Los_Angeles','Europe/London'))
        self.done=False
        self.increment = increment
        self.run()

    def run(self):
        """
        Summary: check for new messages ever increment, spawn new thread at next increment and call run() recursively
        """

        self.next_t+=self.increment
        self.incomingMessages = self.messageHandler.getMessages(self.lastRead).json()
        if not self.done:
            threading.Timer( self.next_t - time.time(), self.run).start()

    def getMessages(self):
        """
        Summary: returns list of new messages
        """

        return self.incomingMessages

    def markMessagesRead(self):
        """
        Summary: updates lastRead field to current time
        """
        
        self.lastRead = str(convertDatetimeTz(str(datetime.now()),'America/Los_Angeles','Europe/London'))
        self.incomingMessages = []

    def stop(self):
        """
        Summary: function for stopping notifications (unused)
        """

        self.done=True

if __name__ == '__main__':
    """
    Testing purposes only
    """
    from constants import SERVER
    messageClient = messageHandler("Lorand",SERVER)
    notifier = Notifier(messageClient,1)
    while True:
        for message in notifier.getMessages():
            print(message['sender'])
        time.sleep(1)