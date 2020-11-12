import threading
import time
import messageHandler

class Notifier():
    """
    Summary: Class for checking incoming messages
    """
    def __init__(self, increment):
        self.next_t = time.time()
        self.incomingMessage = ''
        self.done=False
        self.increment = increment
        self.run()

    def run(self):
        self.next_t+=self.increment
        if not self.done:
            threading.Timer( self.next_t - time.time(), self.run).start()

    def messageReceived(self):
        return self.incomingMessage


    def stop(self):
        self.done=True
