
##Software

The underlying software for the sumo robot is written in Python using web framework Flask.
 The underlying source code can be attained from GitHub at https://github.com/laurivosandi/sumochip and corrections and additions are welcome.


###Software installation

Sumo robot is programmable through the web, but in order to do that we will need to install a web application on the robot. The following steps will guide you through this. This is only necessary on the first time.

Kuna CHIP-il pole videoväljundeid on kuvari ühendamine problemaatiline. Eelistatud on hoopiski üle USB kaabli jadaliidese kasutamine selleks, et robotile teha esmane seadistus. Windows puhul on vaja paigaldada ohjurtarkvara,
 et üldse USB kaablit kasutada saaks. Mac OS X ning Linux puhul seda teha vaja pole.
Since CHIP has no video output connecting a screen is problematic.
Preferred usage would be serial connection via USB cable, to set up the device. For windows additional driver installation is needed to be able to use the USB cable.
Mac OS X or Linux do not have these problems.

![Serial](../img/kit/62-connecting-via-usb.jpg)
Ohjurtarkvara minema siit.
###Installing drivers

For Ubuntu and Mac OS X driver installation is not needed, for Windows driver installation is necessary. Open Device Manager:

![Device manager](../img/usbser/01.png)

Find CDC Composite Gadget marked with a yellow triangle and right click on it and select *Update Driver Software...*:

![Device manager](../img/usbser/02.png)

Click on *Browse my computer for driver software*:

![Device manager](../img/usbser/03.png)

Select *Let me pick from a list of device drivers on my computer*:

![Device manager](../img/usbser/04.png)

Select *Show All Devices* and click on *Next*:

![Device manager](../img/usbser/05.png)

Scroll down on the list on the left and choose *Microsoft*. After scroll down in the righthand list and select *USB Serial Device*:

![Device manager](../img/usbser/06.png)

On the pop-up warning window click *Yes*:

![Device manager](../img/usbser/07.png)

Drivers should now be installed:

![Device manager](../img/usbser/08.png)

A new *USB Serial Device* should appear to device list. Remember the serial number as it will be needed later. On this particular screenshot it is COM6:

![Device manager](../img/usbser/09.png)


###Opening serial connection

For connecting to your robot via serial connection Windows users can use [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).
Ubuntu and other UNIX operating systems can use programs like `screen`, `picocom` or your own preference.
Serial connection allows access to command line inside CHIP and many other smart devices. CHIP uses Debian as its operating system and many commands are the same as Ubuntu.


###Logging into the robot

```bash
sudo picocom -b 115200 /dev/ttyACM0
```
Ctrl-A, Ctrl-X

Username is *root* and password *chip*.

###Setting up the network

First we need to connect CHIP to Internet using WiFi. For that we use NetworkManager pseudografical interface:

```bash
nmtui
```
To verify Internet connection use the `ping` command. Press Ctrl-C to abort:

```bash
ping neti.ee
```


Due do CHIP not having a battery or clock that keeps track of time, then CHIP will try to request the time from the Internet, but sometimes this may fail.
To verify the clock is correct you can use the following command, safe connections to Internet(e.g. GitHub) will fail if the clock is wrong.

```bash
date
```


###Updating the operating system

If the connection is present we can do a software update to CHIP's OS:

```bash
apt update       # Refresh the packet list
apt full-upgrade   # Update the packages
```


### Installing dependencies

Install Git version control software:

```bash
apt install python-pip python-dev git
```

###Installing the sumo robot software

After those steps we are ready to install the sumo robot software:

```bash
pip install sumochip
```

If all has gone according to plan so far then we can find out what is the CHIP's IP address. For this we can use the command :

```bash
ifconfig
```

Try connecting to the robot using SSH, in Windows use PuTTY and under UNIX the command:

```bash
ssh <username>@<ip-aadress>
```

###Setting up the software for sumo robot

Get the configuration file, that has the information about which legs the servomotors and sensors are connected to:

```bash
mkdir -p /etc/sumorobot/
curl https://raw.githubusercontent.com/artizirk/sumochip/master/sumochip/config/sumochip_v1.1.ini > /etc/sumorobot/sumorobot.ini
```


Run test program, to abort press Ctrl-C:

```bash
sumochip_test
```

Check that the line sensors LEDs work. For this look into the line sensors with your mobile phone camera. Infrared will appear as violet in the camera:
![Checking line sensors](../img/kit/63-checking-line-sensors.jpg)

Perform the same check on the sensors for detecting enemies:

![Checking enemy sensors](../img/kit/64-checking-enemy-sensors.jpg)



Try to run the web application:

```bash
sumochip_web
```

If you need to shut down the robot then use the command:

```bash
shutdown -h now
```


##Using the terminal

###Most frequently used commands

Commands used on CHIP also work the same on RaspberryPi and Ubuntu:

* Current directory: `pwd`
* Displaying files and directories in the current directory: `ls -lah`
* Enter directory: `cd directoryname`
* Move up a directory: `cd ..`
* Delete a file: `rm filename`

###Editing files in the terminal

As many other Linux systems CHIP has a text editor called `nano`, to open a file with this program:

```bash
nano path/filename.py
```
Use the keyboard shortcut Ctrl-K to cut the text and Ctrl-U to paste the text. Ctrl-X allows you to save and exit the program.

For a more convenient text editing experience you can use Midnight Commander. To install try:
```Bash
apt install mc
```

:
Opening files is the same:

```bash
mcedit path/filename.py
```

Navigating the menus is similar to graphical applications, Alt-F opens the main menu. Most important shortcuts are F5 to copy, F6 to cut and F10 to exit the program.

[Back to main page](index-en.md "Main page")
