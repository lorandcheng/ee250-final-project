from datetime import datetime
from config import config
import psycopg2

class messageManager:
    def __init__(self):
        """
        Summary: Class for managing the message history database
        """
        print('Starting Message Manager')

    def addMessage(message):
        """
        Summary: Adds provided message to the CloudSQL Postgres database

        Args: 
            message (json): json body of message from rpi containing sender, message body, and timestamp
        """

        # Obtain the configuration parameters
        params = config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()
        #extract values from message
        sender = message['sender']
        body = message['message']
        timestamp = message['timestamp']

        cur.execute("INSERT INTO MESSAGES (SENDER,MESSAGE,TIMESTAMP) VALUES (%s, %s, %s)", (sender,body,timestamp))

        # For example:cursor.execute("insert into people values (%s, %s)", (who, age))
        # Update DB and close connection
        conn.commit()
        conn.close()