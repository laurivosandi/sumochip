import os
from time import sleep
from threading import Thread

class MotorThread(Thread):
    # This class generates PWM signal necessary for servo motors using threading

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
        with open(os.path.join(self.path, "value"), "w") as fh:
          while True:
            if self.speed:
                fh.write("1")
                fh.flush()
                sleep(0.001 if self.speed > 0 else 0.002)
                fh.write("0")
                fh.flush()
                sleep(0.019 if self.speed > 0 else 0.018)
            else:
                sleep(0.020)

left = MotorThread(132)    # CSID0 on the CHIP board
right = MotorThread(133)   # CSID1
            
left.start()
right.start()

while True:
    key = raw_input('Enter your input:')
    if key == "w":
        left.speed = 1
        right.speed = 1
    elif key == "s":
        left.speed = -1
        right.speed = -1
    elif key == "a":
        left.speed = 1
        right.speed = -1
    elif key == "d":
        left.speed = -1
        right.speed = 1
    elif key == "q":
        break
    else:
        left.speed = 0
        right.speed = 0

