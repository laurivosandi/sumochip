from __future__ import print_function

import os
import sys
from time import sleep
from threading import Thread
import json

if sys.version_info[0] < 3:
    from ConfigParser import SafeConfigParser as ConfigParser
    from ConfigParser import NoOptionError
else:
    from configparser import ConfigParser, NoOptionError


try:
    from CHIP_IO import GPIO
    from CHIP_IO import SOFTPWM as PWM
    __use_chip_io__ = True
except ImportError:
    __use_chip_io__ = False


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


VALID_PINS = {"motor_left",
              "motor_right",
              "sensor_power",
              "enemy_left",
              "enemy_right",
              "line_left",
              "line_right",
              "line_front",
              "green_led",
              "yelow_led",
              "red_led",
              "blue_led"}

def unexport(pin):
    if os.path.exists("/sys/class/gpio/gpio{}".format(pin)):
        with open("/sys/class/gpio/unexport", "w") as fh:
            fh.write(str(pin))

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

class ChipIOMotor(object):
    _speed = 0

    def __init__(self, pin, freq=500, duty_min=49.0, duty_max=90.0, stop_on_zero=False):
        self.pin = pin
        self.freq = freq
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.stop_on_zero = stop_on_zero
        sleep(0.1)
        PWM.start(pin, 0, 500)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, val):
        self._speed = val
        if val == 0 and not self.stop_on_zero:
            duty = 0
        else:
            duty = int(map(val, -1.0, 1.0, self.duty_min, self.duty_max))
        PWM.set_duty_cycle(self.pin, duty)


class ChipIOPin(object):

    def __init__(self, pin):
        self.pin = pin
        self.direction = None

    @property
    def value(self):
        if self.direction != "in":
            self.direction = "in"
            GPIO.setup(self.pin, GPIO.IN)
        return GPIO.input(self.pin)

    @value.setter
    def value(self, val):
        if self.direction != "out":
            self.direction = "out"
            GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH if val else GPIO.LOW)


class PythonIOGPIOExportException(Exception):
    pass


class PythonIOPin(object):

    def __init__(self, pin):
        self.pin = pin
        self.path = path = "/sys/class/gpio/gpio{}".format(pin)
        self.direction = "in"
        if not os.path.exists(path):
            with open("/sys/class/gpio/export", "w") as fh:
                try:
                    fh.write(str(pin))
                except IOError as err:
                    raise PythonIOGPIOExportException("GPIO {} export failed".format(pin))
        if not os.path.exists(path):
            raise PythonIOGPIOExportException("GPIO {} export failed".format(pin))
        self.fhr = open(os.path.join(path, "value"), "r")
        self.fhw = open(os.path.join(path, "value"), "w")

    @property
    def value(self):
        fhr = self.fhr
        fhr.seek(0)
        return int(fhr.read())

    @value.setter
    def value(self, val):
        if self.direction != "out":
            self.direction = "out"
            with open(os.path.join(self.path, "direction"), "w") as fh:
                fh.write("out")

        self.fhw.write(str(int(val)))
        self.fhw.flush()


class NoIOPin(object):
    """Stub class for I/O pins that don't have a real gpio pin"""
    pin = None
    value = 0



class PythonIOMotor(Thread): # This class generated PWM signal necessary for servo motors
    def __init__(self, pin=192):
        Thread.__init__(self)
        self.path = "/sys/class/gpio/gpio{}".format(pin)
        if not os.path.exists(self.path):
            with open("/sys/class/gpio/export", "w") as fh:
                fh.write(str(pin))
        with open(os.path.join(self.path, "direction"), "w") as fh:
            fh.write("out")
        self.speed = 0
        self.daemon = True
        self.start()
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


class Sumorobot(object):

    def __init__(self, config_file):
        self.io = AttributeDict()
        self.config = config = ConfigParser()

        if sys.version_info[0] < 3:
            import codecs
            with codecs.open(config_file, 'r', encoding='utf-8') as fh:
                config.readfp(fh)
        else:
            config.read(config_file, encoding='utf-8')

        force_use_chip_io = False
        if "sumorobot" in config.sections():
            sumo_conf = config.options("sumorobot")
            if "use_chip_io" in sumo_conf and config.get("sumorobot", "use_chip_io"):
                force_use_chip_io = config.getboolean("sumorobot", "use_chip_io")
                print("override use_chip_io", __use_chip_io__)


        if "ChipIO" in config.sections() and (__use_chip_io__ or force_use_chip_io):
            print("Using ChipIO")
            io_conf = config.options("ChipIO")
            chip_io_pins = {key for key, val in config.items("ChipIO") if val} & VALID_PINS
            used_pins = set(chip_io_pins)
            print("ChipIO pins: ", ", ".join(str(pin) for pin in chip_io_pins))
            non_chip_io_pins = VALID_PINS - chip_io_pins

            try:
                stop_on_zero = config.getboolean("ChipIO", "motor_stop_on_zero_speed")
            except NoOptionError:
                stop_on_zero = False

            if "motor_left" in chip_io_pins:
                unexport(config.get("PythonIO", "motor_left"))
                try:
                    freq, duty_min, duty_max = config.get("ChipIO", "motor_left_cal").split(",")
                except NoOptionError:
                    freq, duty_min, duty_max = 500, 49, 90

                self.leftMotor = ChipIOMotor(config.get("ChipIO", "motor_left"),
                                             int(freq), float(duty_min), float(duty_max),
                                             stop_on_zero)
                chip_io_pins.remove("motor_left")
            if "motor_right" in chip_io_pins:
                unexport(config.get("PythonIO", "motor_right"))
                try:
                    freq, duty_min, duty_max = config.get("ChipIO", "motor_right_cal").split(",")
                except NoOptionError:
                    freq, duty_min, duty_max = 500, 49, 90
                self.rightMotor = ChipIOMotor(config.get("ChipIO", "motor_right"),
                                            int(freq), float(duty_min), float(duty_max),
                                            stop_on_zero)
                chip_io_pins.remove("motor_right")

            for pin_name in chip_io_pins:
                unexport(config.get("PythonIO", pin_name))
                self.io[pin_name] = ChipIOPin(config.get("ChipIO", pin_name))

        else:
            used_pins = set()
            non_chip_io_pins = VALID_PINS

        if "PythonIO" in config.sections():
            print("Using PythonIO")
            io_conf = config.options("PythonIO")
            python_io_pins = {key for key, val in config.items("PythonIO") if val} & VALID_PINS
            python_io_pins -= used_pins
            print("PythonIO pins: ", ", ".join(str(pin) for pin in python_io_pins))
            non_python_io_pins = non_chip_io_pins - python_io_pins

            if "motor_left" in python_io_pins:
                self.leftMotor = PythonIOMotor(config.get("PythonIO", "motor_left"))
                python_io_pins.remove("motor_left")

            if "motor_right" in python_io_pins:
                self.rightMotor = PythonIOMotor(config.get("PythonIO", "motor_left"))
                python_io_pins.remove("motor_right")

            for pin_name in python_io_pins:
                self.io[pin_name] = PythonIOPin(config.get("PythonIO", pin_name))
        else:
            non_python_io_pins = set()


        unconfigured_pins = non_python_io_pins
        if unconfigured_pins:
            for pin_name in unconfigured_pins:
                self.io[pin_name] = NoIOPin()
        print("NoIO pins: ", ", ".join(str(pin) for pin in unconfigured_pins))

        from pprint import pprint
        print("{:<15}: {}".format("leftMotor", type(self.leftMotor).__name__))
        print("{:<15}: {}".format("rightMotor", type(self.rightMotor).__name__))
        for name, pin in self.io.items():
            print("{:<15}: {}".format(name, type(pin).__name__))

        self.isAutonomous = False
    def forward(self):
        self.leftMotor.speed = 1
        self.rightMotor.speed = -1
    def back(self):
        self.leftMotor.speed = -1
        self.rightMotor.speed = 1
    def stop(self):
        self.leftMotor.speed = 0
        self.rightMotor.speed = 0
    def right(self):
        self.leftMotor.speed = 1
        self.rightMotor.speed = 1
    def left(self):
        self.leftMotor.speed = -1
        self.rightMotor.speed = -1

    def leds_on(self):
        for led in (pin for pin in self.io if pin.endswith("led")):
            self.io[led].value = 0

    @property
    def sensor_power(self):
        return bool(s.io["sensor_power"].value)

    @sensor_power.setter
    def sensor_power(self, val):
        if val:
            s.io["sensor_power"].value = 1
        else:
            s.io["sensor_power"].value = 0


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

if __name__ == "__main__":
    s = Sumorobot("config/sumochip.ini")
    from time import sleep
    s.sensor_power = True
    s.leds_on()
    s.io.red_led.value = True
    s.io.yelow_led.value = True
    while False:
        for x in range(-100, 100, 1):
            s.leftMotor.speed = x/100.0
            print(x)
            sleep(0.01)
        for x in range(100, -100, -1):
            s.leftMotor.speed = x/100.0
            print(x)
            sleep(0.01)

    while True:
        right = not bool(s.io["enemy_right"].value)
        left = not bool(s.io["enemy_left"].value)

        s.io.blue_led.value = not left
        s.io.green_led.value = not right


        if right and left:
            s.forward()
        elif left:
            s.right()
        elif right:
            s.left()
        else:
            s.stop()

        print(1 if right else 0, 1 if left else 0, end="\r")
        sys.stdout.flush()

        sleep(0.01)
