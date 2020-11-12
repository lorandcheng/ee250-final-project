import threading
import time
from messageHandler import messageHandler

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
        self.incomingMessage = ''
        self.done=False
        self.increment = increment
        self.run()

    def run(self):
        self.next_t+=self.increment
        self.messageHandler.getMessage()
        if not self.done:
            threading.Timer( self.next_t - time.time(), self.run).start()

    def messageReceived(self):
        return self.incomingMessage


    def stop(self):
        self.done=True

if __name__ == '__main__':
    """
    Testing purposes onlu
    """
    from constants import SERVER
    messageClient = messageHandler("rpi",SERVER)
    notifier = Notifier(messageClient,1)