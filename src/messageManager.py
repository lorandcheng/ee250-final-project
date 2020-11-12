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

    def getMessage(self, sender):
        """
        Summary: Retreives messages since last message sent by sender

        Args: 
            sender (string): sender identity
        """
        self.cur.execute("SELECT * FROM messages WHERE id > (SELECT id FROM messages WHERE sender IN(%s) ORDER BY id DESC LIMIT 1)", sender)
        rawResult = self.cur.fetchall()
        result = []
        for tpl in rawResult:
            result.append({
                'id': tpl[0],
                'sender': tpl[1],
                'message': tpl[2],
                'timestamp': tpl[3]
            })
        print(result[0]['id'])
        return result

    def cleanup(self):
        print("Running cleanup...")
        self.conn.close()