from __future__ import print_function

import os
import sys
from axp209 import AXP209
from time import sleep
from threading import Thread
import json

if sys.version_info[0] < 3:
    from ConfigParser import SafeConfigParser as ConfigParser
    from ConfigParser import NoOptionError, NoSectionError
else:
    from configparser import ConfigParser, NoOptionError, NoSectionError


try:
    from CHIP_IO import GPIO
    from CHIP_IO import SOFTPWM as PWM
    __use_chip_io__ = True
except ImportError:
    __use_chip_io__ = False


VALID_PINS = {"motor_left",
              "motor_right",
              "sensor_power",
              "enemy_left",
              "enemy_right",
              "line_left",
              "line_right",
              "line_front",
              "green_led",
              "yellow_led",
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
        try:
            return int(fhr.read())
        except:
            return 0

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

class IOPollThread(Thread):
    """Polls the IO pins"""

    def __init__(self, io_pins, poll_freq):
        Thread.__init__(self)
        self.io_pins = io_pins
        self._stopped_ = False
        self._values_ = {}
        self.poll_freq = poll_freq
        self.daemon = True
        self.update_io_values()
        self.start()

    def run(self):
        while not self._stopped_:
            self.update_io_values()
            sleep(self.poll_freq)

    def update_io_values(self):
        for name, pin in self.io_pins.items():
            self._values_[name] = pin.value

    def __getitem__(self, name):
        return self._values_[name]


class IOProxy(object):
    """Proxies IO access to pins through IOPollThread"""

    def __init__(self, io_pin, io_name, io_poll_thread):
        self.io_pin = io_pin
        self.io_name = io_name
        self.io_poll_thread = io_poll_thread

    @property
    def value(self):
        return self.io_poll_thread[self.io_name]

    @value.setter
    def value(self, value):
        self.io_pin.value = value

class ConfigFileNotFound(Exception):
    pass


class Sumorobot(object):

    def __init__(self, config_file=None):
        self.io = AttributeDict()
        self.io_proxies = {}
        self.config = config = ConfigParser()
        if not config_file:
            if os.path.exists("/etc/sumorobot/sumorobot.ini"):
                config_file = "/etc/sumorobot/sumorobot.ini"
            if os.path.exists("sumorobot.ini"):
                config_file = "sumorobot.ini"

        if not config_file:
            raise ConfigFileNotFound("No config files found")
        print("Using config file '{}'".format(config_file))

        if sys.version_info[0] < 3:
            import codecs
            with codecs.open(config_file, 'r', encoding='utf-8') as fh:
                config.readfp(fh)
        else:
            config.read(config_file, encoding='utf-8')

        force_use_chip_io = False
        self.axp209 = None
        if "sumorobot" in config.sections():
            sumo_conf = config.options("sumorobot")
            if "use_chip_io" in sumo_conf and config.get("sumorobot", "use_chip_io"):
                force_use_chip_io = config.getboolean("sumorobot", "use_chip_io")
                print("override use_chip_io", __use_chip_io__)

            if "axp209" in sumo_conf:
                i2c_bus = config.getint("sumorobot", "axp209")
                print("Using axp209 library")
                self.axp209 = AXP209(i2c_bus)
            else:
                self.axp209 = None


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

                self.motor_left = ChipIOMotor(config.get("ChipIO", "motor_left"),
                                             int(freq), float(duty_min), float(duty_max),
                                             stop_on_zero)
                chip_io_pins.remove("motor_left")
            if "motor_right" in chip_io_pins:
                unexport(config.get("PythonIO", "motor_right"))
                try:
                    freq, duty_min, duty_max = config.get("ChipIO", "motor_right_cal").split(",")
                except NoOptionError:
                    freq, duty_min, duty_max = 500, 49, 90
                self.motor_right = ChipIOMotor(config.get("ChipIO", "motor_right"),
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
                self.motor_left = PythonIOMotor(config.get("PythonIO", "motor_left"))
                python_io_pins.remove("motor_left")

            if "motor_right" in python_io_pins:
                self.motor_right = PythonIOMotor(config.get("PythonIO", "motor_right"))
                python_io_pins.remove("motor_right")

            for pin_name in python_io_pins:
                self.io[pin_name] = PythonIOPin(config.get("PythonIO", pin_name))
        else:
            non_python_io_pins = non_chip_io_pins - used_pins


        unconfigured_pins = non_python_io_pins
        if unconfigured_pins:
            for pin_name in unconfigured_pins:
                self.io[pin_name] = NoIOPin()

        io_poll_freq = 0.01
        try:
            io_poll_freq = self.config.getint("sumorobot", "io_poll_freq")
        except (NoSectionError, NoOptionError):
            pass
        self.io_poll_thread = IOPollThread(self.io, io_poll_freq)

        for name, pin in self.io.items():
            if isinstance(pin, NoIOPin):
                continue
            self.io_proxies[pin_name] = IOProxy(pin, name, self.io_poll_thread)


        print("NoIO pins: ", ", ".join(str(pin) for pin in unconfigured_pins))

        from pprint import pprint
        print("{:<15}: {}".format("motor_left", type(self.motor_left).__name__))
        print("{:<15}: {}".format("motor_right", type(self.motor_right).__name__))
        for name, pin in self.io.items():
            print("{:<15}: {}".format(name, type(pin).__name__))

    def __getattr__(self, name):
        if name in self.io_proxies:
            return self.io_proxies[name]
        elif name in self.io:
            return self.io[name]
        else:
            raise AttributeError("'{}' object has no I/O pin named '{}'".format(type(self).__name__, name))


    def forward(self):
        self.motor_left.speed = 1
        self.motor_right.speed = -1
    def back(self):
        self.motor_left.speed = -1
        self.motor_right.speed = 1
    def stop(self):
        self.motor_left.speed = 0
        self.motor_right.speed = 0
    def right(self):
        self.motor_left.speed = 1
        self.motor_right.speed = 1
    def left(self):
        self.motor_left.speed = -1
        self.motor_right.speed = -1

    @property
    def sensor_power(self):
        return bool(self.io["sensor_power"].value)

    @sensor_power.setter
    def sensor_power(self, val):
        if val:
            self.io["sensor_power"].value = 1
        else:
            self.io["sensor_power"].value = 0

    @property
    def battery_gauge(self):
        if self.axp209:
            return self.axp209.battery_gauge
        else:
            return 0

    def isEnemy(self, value):
        if value == 'LEFT':
            return not self.enemy_left.value
        elif value == 'RIGHT':
            return not self.enemy_right.value
        elif value == 'FRONT':
            left = self.enemy_left.value
            right = self.enemy_right.value
            if right == 0 and left == 0:
                return True
            else:
                return False

    def isLine(self, value):
        if value == 'LEFT':
            return not self.line_left.value
        elif value == 'RIGHT':
            return not self.line_right.value
        elif value == 'FRONT':
            return not self.line_front.value



class SensorThread(Thread):
    def __init__(self, ws, sumorobot):
        Thread.__init__(self)
        self.daemon = True
        self.ws = ws
        self.sumorobot = sumorobot
        self.start()
    def run(self):
        while True:
            if self.ws and not self.ws.closed:
                self.ws.send(json.dumps(self.getData()))
                sleep(0.2)

    def getData(self):
        stats = {}
        s = self.sumorobot
        #for filename in os.listdir("/sys/power/axp_pmu/battery/"):
        #    with open ("/sys/power/axp_pmu/battery/" + filename) as fh:
        #        stats[filename] = int(fh.read())
        stats["capacity"] = s.battery_gauge

        right = not s.enemy_right.value
        left = not s.enemy_left.value
        line_right = not s.line_right.value
        line_front = not s.line_front.value
        line_left = not s.line_left.value

        s.blue_led.value = not left
        s.green_led.value = not right

        if line_front:
            s.red_led.value = s.yellow_led.value = not line_front
        else:
            s.red_led.value = not line_left
            s.yellow_led.value = not line_right

        stats["enemy_right"] = 1 if right else 0
        stats["enemy_left"] = 1 if left else 0
        stats["line_left"] = 1 if line_left else 0
        stats["line_right"] = 1 if line_right else 0
        stats["line_front"] = 1 if line_front else 0
        return stats


def self_test(s):
    from time import sleep

    print("powering on the sensors")
    s.sensor_power = True

    t=0.1
    print("LED test", end="")
    for x in range(5):
        s.blue_led.value = False
        s.red_led.value = True
        s.yellow_led.value = True
        s.green_led.value = True
        sleep(t)
        s.blue_led.value = True
        s.red_led.value = False
        s.yellow_led.value = True
        s.green_led.value = True
        sleep(t)
        s.blue_led.value = True
        s.red_led.value = True
        s.yellow_led.value = False
        s.green_led.value = True
        sleep(t)
        s.blue_led.value = True
        s.red_led.value = True
        s.yellow_led.value = True
        s.green_led.value = False
        sleep(t)
        s.blue_led.value = True
        s.red_led.value = True
        s.yellow_led.value = False
        s.green_led.value = True
        sleep(t)
        s.blue_led.value = True
        s.red_led.value = False
        s.yellow_led.value = True
        s.green_led.value = True
        sleep(t)
        print(".", end="")
        sys.stdout.flush()
    print()


    print("motor_left test")
    for x in range(-100, 100, 2):
        s.motor_left.speed = x/100.0
        print(x, end="   \r")
        sys.stdout.flush()
        sleep(0.01)
    print()
    s.motor_left.speed = 0

    print("motor_right test")
    for x in range(-100, 100, 2):
        s.motor_right.speed = x/100.0
        print(x, end="   \r")
        sys.stdout.flush()
        sleep(0.01)
    print()
    s.motor_left.speed = 0


    print("sumorobot.forward()")
    s.forward()
    sleep(1)
    s.stop()

    print("sumorobot.back()")
    s.back()
    sleep(1)
    s.stop()

    print("Entering play mode")
    while True:
        right = not s.enemy_right.value
        left = not s.enemy_left.value
        line_right = not s.line_right.value
        line_front = not s.line_front.value
        line_left = not s.line_left.value

        s.blue_led.value = not left
        s.green_led.value = not right

        if line_front:
            s.red_led.value = s.yellow_led.value = not line_front
        else:
            s.red_led.value = not line_left
            s.yellow_led.value = not line_right



        if right and left:
            s.forward()
        elif left:
            s.left()
        elif right:
            s.right()
        else:
            s.stop()

        print(1 if right else 0,
              1 if left else 0,
              "  ",
              1 if line_right else 0,
              1 if line_front else 0,
              1 if line_left else 0,
              end="\r")
        sys.stdout.flush()

        sleep(0.01)

def main():
    try:
        s = Sumorobot()
        self_test(s)
    except KeyboardInterrupt:
        print("\nGraceful shutdown (Leds and sensors off)")
        s.sensor_power = False
        s.blue_led.value = 1
        s.red_led.value = 1
        s.yellow_led.value = 1
        s.green_led.value = 1

if __name__ == "__main__":
    main()
