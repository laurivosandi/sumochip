from __future__ import print_function
from flask import Flask, render_template
from sumorobot import Sumorobot, SensorThread
from flask_sockets import Sockets
from threading import Thread
from time import sleep
import imp
import json
import os

codeTemplate = """
from threading import Thread
from time import sleep
class AutonomousThread(Thread):
    def __init__(self, sumorobot):
        Thread.__init__(self)
        self.sumorobot = sumorobot

    def run(self):
        self.running = True
        print("Starting AutonomousThread")
        while self.running:
            self.step()
            sleep(0.01)
        print("AutonomousThread was stopped")
        self.sumorobot.stop()
    def step(self):
        sumorobot = self.sumorobot
        isEnemy = sumorobot.isEnemy
        isLine = sumorobot.isLine
"""


sumorobot = Sumorobot()
codeThread = None
codeText = ""
codeBytecode = None

app = Flask(__name__)
try:
    with open("/etc/machine-id", "r") as fh:
        app.config['SECRET_KEY'] = fh.read()
except:
    app.config['SECRET_KEY'] = 'secret!'
sockets = Sockets(app)

@app.route('/')
def index():
    print("HTTP request")
    return render_template('index.html')

@sockets.route('/')
def command(ws):
    global codeThread
    global codeText
    global codeBytecode
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
            sensors = SensorThread(ws, sumorobot)
        elif command == 'getSavedCode':
            with open("code.txt", "r") as fh:
                code = fh.read()
                print(code)
                ws.send(json.dumps({'savedCode':code}))
                codeText = code
                fullCodeText = codeTemplate + "".join((" "*8 + line + "\n" for line in codeText.split("\n")))
                print(fullCodeText)
                codeBytecode = compile(codeText, "<SumorobotCode>", "exec")
        elif command == 'executeCode':
            if codeThread:
                codeThread.running = False
            slave = {}
            exec(codeBytecode, slave)
            codeThread = slave["AutonomousThread"](sumorobot)
            codeThread.daemon = True
            codeThread.start()
            sumorobot.sensor_power = True
        elif command == 'stopCode':
            if codeThread:
                codeThread.running = False
            print("code execution stopped")
            sumorobot.sensor_power = False
        else:
            print("Code to be saved:")
            print(command)
            with open("code.txt", "w") as fh:
                fh.write(str(command))
            codeText = str(command)
            fullCodeText = codeTemplate + "".join((" "*8 + line + "\n" for line in codeText.split("\n")))
            print(fullCodeText)
            codeBytecode = compile(fullCodeText, "<SumorobotCode>", "exec")
            print('Saved')


def main():
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    ip, port = ('0.0.0.0', 5001)
    if os.getuid() == 0:
        port = 80
    server = pywsgi.WSGIServer((ip, port), app, handler_class=WebSocketHandler)
    print("Starting server at http://{}:{}".format(ip, port))
    server.serve_forever()

if __name__ == '__main__':
    main()
