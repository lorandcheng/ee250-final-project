#!/usr/bin/env python3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# Author: Lorand Cheng https://github.com/lorandcheng
# Date: Nov 15, 2020
# Project: USC EE250 Final Project, Morse Code Translator and Messenger
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import json
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from datetime import datetime
from messageManager import messageManager

app = Flask(__name__)
socketio = SocketIO(app)

HOST = '0.0.0.0'
PORT = '4200'

@app.route('/')
def home():
    """
    Summary: serves index.html file to clients connecting on the home page
    """
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def postMessageCallback():
    """
    Summary: A callback for when POST is called on [host]:[port]/send-message

    Returns:
        string: A JSON-formatted string containing the response message
    """

    # Get the payload containing the sender, message, and timestamp
    # if type(request.get_data())==bytes:
    payload = request.get_data().decode('utf-8')
    payload = json.loads(payload)
    payload['timestamp'] = str(datetime.now())
    # else:
    #     payload = request.get_json()
    #     print('rpi-message')
    print(payload)
    # add message to database
    messageManager.addMessage(payload)
    # notify clients of new message
    socketio.emit('message',payload)
    # send response
    response = {'Response': 'Message sent'}
    return json.dumps(response)

@app.route('/get-messages', methods=['GET'])
def getMessageCallback():
    """
    Summary: A callback for when GET is called on [host]:[port]/get-message

    Returns:
        string: A JSON-formatted string containing the messages received since the last message sent by caller
    """

    # Get the payload containing the sender, message, and timestamp
    sender = request.args.get('sender')
    lastRead = request.args.get('lastRead')
    response = messageManager.getMessage(sender, lastRead)
    return json.dumps(response)

@app.route('/history', methods=['GET'])
def historyCallback():
    """
    Summary: A callback for when GET is called on [host]:[port]/history

    Returns:
        string: A JSON-formatted string containing the entire message history in the db
    """

    response = messageManager.history()
    return json.dumps(response)

@socketio.on('initial-connect')
def handleConnection(message):
    """
    Summary: handles intial connection
    """
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