from flask import Flask
from flask import jsonify
from flask import request

import json
import messageManager

app = Flask('Cloud Messaging Server')

HOST = '127.0.0.1'
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

    #TODO add message to db
    response = {'Response': 'Message sent'}

    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=False, host=HOST, port=PORT)