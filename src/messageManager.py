#!/usr/bin/env python3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# Author: Lorand Cheng https://github.com/lorandcheng
# Date: Nov 15, 2020
# Project: USC EE250 Final Project, Morse Code Translator and Messenger
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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

        # extract values from message
        sender = message['sender']
        body = message['message']
        timestamp = message['timestamp']
        # Execute SQL command to add message
        self.cur.execute("INSERT INTO MESSAGES (SENDER,MESSAGE,TIMESTAMP) VALUES (%s, %s, %s)", (sender,body,timestamp))
        # Update DB
        self.conn.commit()

    def getMessage(self, sender, lastRead):
        """
        Summary: Retreives messages since last message sent by sender

        Args: 
            sender (string): sender identity
        """

        # execute SQL command and retreive results
        self.cur.execute("SELECT * FROM messages WHERE sender != (%s) AND timestamp > (%s) ORDER BY timestamp", (sender, lastRead))
        rawResult = self.cur.fetchall()
        # parse results into a list of message objects
        result = []
        for tpl in rawResult:
            result.append({
                'id': tpl[0],
                'sender': tpl[1],
                'message': tpl[2],
                'timestamp': tpl[3]
            })
        return result

    def history(self):
        """
        Summary: Pulls message history from db
        """

        # execute SQL command and retreive results 
        self.cur.execute("SELECT * FROM messages ORDER BY timestamp")
        rawResult = self.cur.fetchall()
        # parse results into a list of message objects
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
        """
        Summary: close the connection to the database on termination
        """
        print("Running cleanup...")
        self.conn.close()

if __name__ == '__main__':
    """
    For testing purposes only!
    """
    from pprint import pprint
    messageManager = messageManager()
    pprint(messageManager.getMessage("rpi","2020-11-15 03:11:00"))