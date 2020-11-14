#!/usr/bin/env python3
import json
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO

from messageManager import messageManager

app = Flask('Cloud Messaging Server')
socketio = SocketIO(app)

HOST = '0.0.0.0'
PORT = '4200'

@app.route('/')
def home():
   return render_template('index.html')

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

@app.route('/get-messages', methods=['GET'])
def gettMessageCallback():
    """
    Summary: A callback for when GET is called on [host]:[port]/get-message

    Returns:
        string: A JSON-formatted string containing the messages received from rpi since the last sent message
    """

    # Get the payload containing the sender, message, and timestamp
    sender = request.args.get('sender')
    lastRead = request.args.get('lastRead')
    response = messageManager.getMessage(sender, lastRead)

    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

@socketio.on('initial-connect')
def handle_connection(message):
    print(message)

if __name__ == '__main__':
    
    # test = {
    #     'sender': 'Lorand',
    #     'message': 'testing message',
    #     'timestamp': 'today'
    # }
    # writeToDB(test)

    messageManager = messageManager()
    # Start the flask app with socketio
    socketio.run(app, host=HOST, port=PORT)