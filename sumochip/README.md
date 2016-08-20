# SumoChip software setup

1. Flash 4.4 debian headless image from http://flash.getchip.com/
2. Connect to the CHIP using serial `picocom /dev/ttyACM0` and login as `root`,
   password is `chip`
3. Connect CHIP to the internet using `nmtui`
4. Update and install software

```
apt update
apt full-upgrade
apt install git python-pip python-dev
pip install Flask Flask-Sockets CHIP-IO axp209
git clone https://github.com/artizirk/sumochip
```

5. Configure sumorobot software

```
cd ~/sumochip/sumochip
rm sumorobot.ini
ln -s config/sumochip_v1.1.ini sumorobot.ini
```

6. Run self test

```
cd ~/sumochip/sumochip
python sumorobot.py
```
