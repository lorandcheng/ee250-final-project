import json
from datetime import datetime
from flask import Flask, request, render_template
from flask_socketio import SocketIO

HOST = 'localhost'
PORT = '4200'

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/test', methods=['POST'])
def postMessage():
    print(type(request.get_data())==bytes)
    payload = request.get_data().decode('utf-8')
    payload = json.loads(payload)
    payload['timestamp'] = str(datetime.now())
    print(payload)
    response = {'Response': 'Message sent'}

    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

@socketio.on('initial-connect')
def handleConnection(message):
    print(message)

if __name__ == '__main__':
    socketio.run(app, host=HOST, port=PORT)