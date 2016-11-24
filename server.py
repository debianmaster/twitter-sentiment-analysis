import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
import os

sio = socketio.Server()
app = Flask(__name__)



#API
@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat', namespace='/chat')
def message(sid, data):
    sio.emit('reply', data,namespace='/chat')

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0',int(os.environ.get('socket_port')))), app)




  





