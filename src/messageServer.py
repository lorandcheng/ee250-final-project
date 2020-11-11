#!/usr/bin/env python3
from flask import Flask
from flask import jsonify
from flask import request
import json

from messageManager import messageManager


app = Flask('Cloud Messaging Server')

HOST = '0.0.0.0'
PORT = '4200'




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
    messageManager.addMessage(payload)
    response = {'Response': 'Message sent'}

    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

if __name__ == '__main__':
    
    # test = {
    #     'sender': 'Lorand',
    #     'message': 'testing message',
    #     'timestamp': 'today'
    # }
    # writeToDB(test)

    messageManager = messageManager();
    # Start the flask app
    app.run(debug=False, host=HOST, port=PORT)