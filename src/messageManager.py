import atexit
import psycopg2
from datetime import datetime
from config import config


class messageManager:
    def __init__(self):
        """
        Summary: Class for managing the message history database
        """
        print('Starting Message Manager')
        # Obtain the configuration parameters
        params = config()
        # Connect to the PostgreSQL database
        self.conn = psycopg2.connect(**params)
        # Create a new cursor
        self.cur = self.conn.cursor()
        # Define cleanup function
        atexit.register(self.cleanup)

    def addMessage(self, message):
        """
        Summary: Adds provided message to the CloudSQL Postgres database

        Args: 
            message (json): json body of message from rpi containing sender, message body, and timestamp
        """

        #extract values from message
        sender = message['sender']
        body = message['message']
        timestamp = message['timestamp']
        # Execute SQL command
        self.cur.execute("INSERT INTO MESSAGES (SENDER,MESSAGE,TIMESTAMP) VALUES (%s, %s, %s)", (sender,body,timestamp))
        # Update DB
        self.conn.commit()

    def cleanup(self):
        print("Running cleanup...")
        self.conn.close()