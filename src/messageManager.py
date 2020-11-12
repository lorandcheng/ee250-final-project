#!/usr/bin/env python3
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
            message (json): json body of message containing sender, message body, and timestamp
        """

        #extract values from message
        sender = message['sender']
        body = message['message']
        timestamp = message['timestamp']
        # Execute SQL command
        self.cur.execute("INSERT INTO MESSAGES (SENDER,MESSAGE,TIMESTAMP) VALUES (%s, %s, %s)", (sender,body,timestamp))
        # Update DB
        self.conn.commit()

    def getMessage(self, sender, lastRead):
        """
        Summary: Retreives messages since last message sent by sender

        Args: 
            sender (string): sender identity
        """
        self.cur.execute("SELECT * FROM messages WHERE sender != (%s) AND timestamp > (%s)", (sender, lastRead))
        rawResult = self.cur.fetchall()
        result = []
        for tpl in rawResult:
            result.append({
                'id': tpl[0],
                'sender': tpl[1],
                'message': tpl[2],
                'timestamp': tpl[3]
            })
        return result

    def cleanup(self):
        print("Running cleanup...")
        self.conn.close()

if __name__ == '__main__':
    """
    For testing purposes only!
    """
    messageManager = messageManager()
    print(messageManager.getMessage("Lorand","2020-11-10 12:34:56.789012"))