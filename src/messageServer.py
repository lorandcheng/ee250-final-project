#!/usr/bin/env python3
from flask import Flask
from flask import jsonify
from flask import request
from config import config
import psycopg2
import json
import messageManager


app = Flask('Cloud Messaging Server')

HOST = '0.0.0.0'
PORT = '4200'

def writeToDB(message):
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


@app.route('/send-message', methods=['POST'])
def postMessageCallback():
    """
    Summary: A callback for when POST is called on [host]:[port]/send-message

    Returns:
        string: A JSON-formatted string containing the response message
    """

    # Get the payload containing the sender, message, and timestamp
    payload = request.get_json()
    print(payload)
    #TODO add message to db
    response = {'Response': 'Message sent'}

    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

if __name__ == '__main__':
    
    test = {
        'sender': 'Lorand',
        'message': 'testing message',
        'timestamp': 'today'
    }
    writeToDB(test)

    # Start the flask app
    app.run(debug=False, host=HOST, port=PORT)