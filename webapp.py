import gevent.monkey
gevent.monkey.patch_all()

from flask import Flask
from flask import render_template
from flask_socketio import SocketIO

import json

from detox_engine import ToxicityClassifier

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf1234'
socketio = SocketIO(app)

toxicityClassifier = ToxicityClassifier()

@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    print('received my event: username:' + msg['username'] + ', message:' + msg['message'] )
    print('chat toxicity analyzed...' + str(toxicityClassifier.isToxic(msg['message'])))
    if toxicityClassifier.isToxic(msg['message']) == True:
        socketio.emit('my response', { 'username': msg['username'], 'message': msg['message'], 'is_toxic': '1'}, callback=messageReceived)
    else:
        socketio.emit('my response', { 'username': msg['username'], 'message': msg['message'], 'is_toxic': '0'}, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)