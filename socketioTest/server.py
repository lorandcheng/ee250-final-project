from flask import Flask, render_template
from flask_socketio import SocketIO

HOST = '0.0.0.0'
PORT = '4200'

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
   return render_template('templates/index.html')

@socketio.on('initial-connect')
def handle_connection(message):
    print(message)

if __name__ == '__main__':
    socketio.run(app, host=HOST, port=PORT)