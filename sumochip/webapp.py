from flask import Flask, render_template
from sumorobot import Sumorobot, SensorThread, isLine, isEnemy
from flask_sockets import Sockets
from threading import Thread
from time import sleep
import imp
import json

sumorobot = Sumorobot()
codeThread = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sockets = Sockets(app)

@app.route('/')
def index():
    print "HTTP request"
    return render_template('index.html')

@sockets.route('/')
def command(ws):
    global codeThread
    while not ws.closed:
        command = ws.receive()
        if command:
            print('Command: ' + command)
        if command == '0':
            print("Stop")
            sumorobot.stop()
        elif command == '1':
            print("Forward")
            sumorobot.forward()
        elif command == '2':
            print("Back")
            sumorobot.back()
        elif command == '3':
            print("Right")
            sumorobot.right()
        elif command == '4':
            print("Left")
            sumorobot.left()
        elif command == 'sensors':
            print("keegi kysib sensoreid")
            sensors = SensorThread(ws)
        elif command == 'getSavedCode':
            with open("code.txt", "r") as fh:
                code = fh.read()
                print(code)
                ws.send(json.dumps({'savedCode':code}))
        elif command == 'executeCode':
            if codeThread:
                codeThread.running = False
            slave = imp.load_source('slave','webapp.py')
            codeThread = slave.AutonomousThread()
            codeThread.daemon = True
            codeThread.start()
        elif command == 'stopCode':
            if codeThread:
                codeThread.running = False
            print("code execution stopped")
        else:
            print("Code to be saved:")
            print(command)
            with open("code.txt", "w") as fh:
                fh.write(str(command))
            print('Saved')

if __name__ == '__main__':
    print("Started server")
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5001), app, handler_class=WebSocketHandler)
    server.serve_forever()

class AutonomousThread(Thread):
    def run(self):
        self.running = True
        while self.running:
            self.step()
            sleep(0.5)
        sumorobot.stop()
    def step(self):
         with open("code.txt", "r") as fh:
            exec(fh.read())
