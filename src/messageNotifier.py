#!/usr/bin/env python3
import threading
import time
from messageHandler import messageHandler
from datetime import datetime

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
        self.lastRead = datetime.now()
        self.done=False
        self.increment = increment
        self.run()

    def run(self):
        self.next_t+=self.increment
        self.incomingMessages = self.messageHandler.getMessages(self.lastRead)
        if not self.done:
            threading.Timer( self.next_t - time.time(), self.run).start()

    def stop(self):
        self.done=True

if __name__ == '__main__':
    """
    Testing purposes only
    """
    from constants import SERVER
    messageClient = messageHandler("rpi",SERVER)
    notifier = Notifier(messageClient,1)