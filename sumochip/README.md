# SumoChip software setup

1. Flash 4.4 debian headless image from http://flash.getchip.com/
2. Connect to the CHIP using serial `picocom /dev/ttyACM0` and login as `root`,
   password is `chip`
3. Connect CHIP to the internet using `nmtui`
4. Update and install software

```
apt update
apt full-upgrade
apt install git python-pip python-dev python-systemd
```

Install stable release

```
pip install sumochip
```

or install git version

```
pip install git+https://github.com/laurivosandi/sumochip
```

5. Configure sumorobot software

```
mkdir -p /etc/sumorobot
cp `python -c "import os, sumochip; print(os.path.dirname(os.path.realpath(sumochip.__file__)))"`/config/sumochip_v1.1.ini /etc/sumorobot/sumorobot.ini
```

6. Run self test

```
sumochip_test
```

7. Start the web interface

From terminal

```
sumochip_web
```

Or start and optionaly enable autostart of systemd service

```
systemctl start sumochip
systemctl enable sumochip
```
