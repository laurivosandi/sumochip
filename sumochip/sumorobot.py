import os
from time import sleep
from threading import Thread
import json

motorLeftPin = 202
motorRightPin = 196
enemyLeftPin = 192
enemyRightPin = 195
lineLeftPin = 193
lineRightPin = 194
lineFrontPin = 195
enemyLeftPath = "/sys/class/gpio/gpio%d" % enemyLeftPin
enemyRightPath = "/sys/class/gpio/gpio%d" % enemyRightPin
lineLeftPath = "/sys/class/gpio/gpio%d" % lineLeftPin
lineRightPath = "/sys/class/gpio/gpio%d" % lineRightPin
lineFrontPath = "/sys/class/gpio/gpio%d" % lineFrontPin

class Sumorobot:
    def __init__(self):
        self.leftMotor = MotorThread(motorLeftPin)
        self.leftMotor.start()
        self.rightMotor = MotorThread(motorRightPin)
        self.rightMotor.start()
        self.isAutonomous = False
    def forward(self):
        self.leftMotor.speed = 1
        self.rightMotor.speed = 1
    def back(self):
        self.leftMotor.speed = -1
        self.rightMotor.speed = -1
    def stop(self):
        self.leftMotor.speed = 0
        self.rightMotor.speed = 0
    def right(self):
        self.leftMotor.speed = -1
        self.rightMotor.speed = 1
    def left(self):
        self.leftMotor.speed = 1
        self.rightMotor.speed = -1

class MotorThread(Thread): # This class generated PWM signal necessary for servo motors
    def __init__(self, pin=192):
        Thread.__init__(self)
        self.path = "/sys/class/gpio/gpio%d" % pin
        if not os.path.exists(self.path):
            with open("/sys/class/gpio/export", "w") as fh:
                fh.write(str(pin))
        with open(os.path.join(self.path, "direction"), "w") as fh:
            fh.write("out")
        self.speed = 0
        self.daemon = True
    def run(self):
        print("run")
        with open(os.path.join(self.path, "value"), "w") as fh:
          while True:
            if self.speed:
                fh.write("1")
                fh.flush()
                sleep(0.002 if self.speed > 0 else 0.001)
                fh.write("0")
                fh.flush()
                sleep(0.018 if self.speed > 0 else 0.019)
            else:
                sleep(0.020)

class SensorThread(Thread):
    def __init__(self, ws):
        Thread.__init__(self)
        self.daemon = True
        self.ws = ws
        self.start()
    def run(self):
        while True:
            if self.ws and not self.ws.closed:
                self.ws.send(json.dumps(getData()))
                sleep(0.2)


def getData():
    createFiles()
    stats = {}
    for filename in os.listdir("/sys/power/axp_pmu/battery/"):
        with open ("/sys/power/axp_pmu/battery/" + filename) as fh:
            stats[filename] = int(fh.read())
    with open(os.path.join(enemyRightPath, "value")) as fh:
        stats["enemy_right"] = int(fh.read())
    with open(os.path.join(enemyLeftPath, "value")) as fh:
        stats["enemy_left"] = int(fh.read())
    with open(os.path.join(lineLeftPath, "value")) as fh:
        stats["line_left"] = int(fh.read())
    with open(os.path.join(lineRightPath, "value")) as fh:
        stats["line_right"] = int(fh.read())
    with open(os.path.join(lineFrontPath, "value")) as fh:
        stats["line_front"] = int(fh.read())
    return stats

def createFiles():
    #enemysensor files check
    if not os.path.exists(enemyLeftPath):
        with open("/sys/class/gpio/export", "w") as fh:
            fh.write(str(enemyLeftPin))
    if not os.path.exists(enemyRightPath):
        with open("/sys/class/gpio/export", "w") as fh:
            fh.write(str(enemyRightPin))
    #linesensor files check
    if not os.path.exists(lineLeftPath):
        with open("/sys/class/gpio/export", "w") as fh:
            fh.write(str(lineLeftPin))
    if not os.path.exists(lineRightPath):
        with open("/sys/class/gpio/export", "w") as fh:
            fh.write(str(lineRightPin))
    if not os.path.exists(lineFrontPath):
        with open("/sys/class/gpio/export", "w") as fh:
            fh.write(str(lineFrontPin))
    
def isLine(value):
    if value == 'LEFT':
        with open(os.path.join(lineLeftPath, "value")) as fh:
            return int(fh.read()) == 1
    elif value == 'RIGHT':
        with open(os.path.join(lineRightPath, "value")) as fh:
            return int(fh.read()) == 1
    elif value == 'FRONT':
        with open(os.path.join(lineFrontPath, "value")) as fh:
            return int(fh.read()) == 1

def isEnemy(value):
    if value == 'LEFT':
        with open(os.path.join(enemyLeftPath, "value")) as fh:
            return int(fh.read()) == 1
    elif value == 'RIGHT':
        with open(os.path.join(enemyRightPath, "value")) as fh:
            return int(fh.read()) == 1
    elif value == 'FRONT':
        left = 0
        right = 0
        with open(os.path.join(enemyLeftPath, "value")) as fh:
            left = fh.read()
        with open(os.path.join(enemyRightPath, "value")) as fh:
            right = fh.read()
        if right == 1 and left == 1:
            return True
        else:
            return False
