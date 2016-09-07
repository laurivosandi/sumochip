## Components

The following list contains the components and their approximate cost with shipping into the European Union. VAT may be added upon entry into the EU.

| Picture                               | Description                            | Quantity | Total      |
|---------------------------------------|----------------------------------------|----------|------------|
| ![CHIP](../img/chip.png)                 | NextThingCo C.H.I.P.                   | 10pcs    |  94.32 EUR |
| ![Servo](../img/pservo.png)              | Plastik hammasratastega servo FS90R    | 20pcs    |  63.63 EUR |
| ![Spoked wheel](../img/spoked-wheel.png) | Rattad                                 | 20pcs    |  34.70 EUR |
| ![LiPo](../img/lipo.png)                 | Liitiumpolümeeraku 3.7V 1100mAh        | 10pcs    |  51.46 EUR |
| ![PCB](../img/sumochip.png)              | SumoCHIP trükkplaat MakerStudiost      | 10pcs    |  15.20 EUR |
| ![IR](../img/ir-led.png)                 | Infrared emitter and receiver          | 50 pairs |   3.91 EUR |
| ![SMD resistor](../img/smd-resistor.jpg) | 100 ohm resistors                      | 120pcs   |   1.20 EUR |
| ![SMD resistor](../img/smd-resistor.jpg) | 10k ohm resistors                      | 30pcs    |   0.60 EUR |
| ![SMD resistor](../img/smd-resistor.jpg) | 100k ohm resistors                     | 50pcs    |   0.60 EUR |
| ![Header](../img/straight-header.jpg)    | 40-pin 2.54mm male straight header     | 13pcs    |   1.02 EUR |
| ![Header](../img/angled-header.jpg)      | 40-pin 2.54mm male angled header       | 1pcs     |   0.44 EUR |
| ![SMD LED](../img/smd-led.jpg)           | LED-ide assortii                       | 50pcs    |   0.98 EUR |
| ![2N7000](../img/2n7000.jpg)             | 60V 200mA N-channel MOSFET             | 10pcs    |   0.85 EUR |
|                                       |                                        | Total:   | 270    EUR |
|                                       |                                        |Per Robot:|  27    EUR |

Robot components URLs:

- http://getchip.com/products/chip
- http://www.aliexpress.com/item/5-pcs-9g-Mini-360-Degree-Continuous-Rotation-Robot-Servo-FS90R/32621562033.html
- http://www.aliexpress.com/item/10-pcs-wheel-for-9g-360-Degree-Continuous-Rotation-Micro-Robot-Servo-FS90R/32609379555.html
- http://www.aliexpress.com/item/20pcs-lot-Free-Shipping-HRB-Lipo-Battery-3-7V-1100mah-15C-Max-30C-1S-Li-po/32430505576.html
- http://makerstudio.cc/
- http://www.aliexpress.com/item/100PCS-5mm-940nm-LEDs-infrared-emitter-and-IR-receiver-diode-50pairs-diodes-301A/2001367152.html
- http://www.aliexpress.com/item/100pcs-100-ohm-1-4W-100R-Metal-Film-Resistor-100ohm-0-25W-1-ROHS/32576340704.html
- http://www.aliexpress.com/item/100pcs-10k-ohm-1-4W-10k-Metal-Film-Resistor-10kohm-0-25W-1-ROHS/32577051768.html
- http://www.aliexpress.com/item/100pcs-100k-ohm-1-4W-100k-Metal-Film-Resistor-100kohm-0-25W-1-ROHS/32575205454.html
- http://www.aliexpress.com/item/Free-Shipping-40Pin-2-54mm-male-Single-Row-40P-single-Row-20pcs-40-pins-pin-header/1324468140.html
- http://www.aliexpress.com/item/2-Pcs-40-Position-2-54mm-Pitch-Single-Row-Right-Angle-Male-Pin-Header/32241048789.html
- http://www.aliexpress.com/item/Free-shipping-100pcs-3mm-LED-Light-White-Yellow-Red-Green-Blue-Assorted-Kit-DIY-LEDs-Set/32568914032.html
- http://www.aliexpress.com/item/12pcs-2N7000-MOSFET-N-CH-60V-200MA-TO-92-NEW-GOOD-QUALITY/32390351935.html

###Alternative components

Optional substitute components

| Picture                   | Description                  | Quantity | Price  | Total     | Difference|
|---------------------------|------------------------------|------|------------|-----------|-----------|
| ![Servo](../img/mservo.png)  | Servo with metal gears       | 2tk  |   4.86 EUR |  9.72 EUR | +3.40 EUR |
| ![Wheel](../img/wheel.png)   | Servo wheel                  | 2tk  |   2.19 EUR |  4.38 EUR | +0.94 EUR |
| ![OPB745](../img/opb745.jpg) | Optek OPB745 line sensor     | 3tk  |   3.00 EUR |  9.00 EUR | +9.00 EUR |

Alternative component URLs:

- http://www.aliexpress.com/item/Smart-car-tires-steering-wheel-tire-tire-rubber-tire-tracking-DIY-model-toy-car-accessories-aperture/2055170090.html
- http://ee.farnell.com/optek-technology/opb745/photo-interrupter-reflective-3/dp/1497910


##Motherboard

The CPU used on the sumo robot is a 8€ computer called CHIP. CHIP is a system on a chip with WiFi support.
<img src="https://cdn.shopify.com/s/files/1/1065/9514/t/15/assets/chip1.png?5824758464935567530">

C.H.I.P. is designed to work with any screen. You can use it with LCD panels or CSI cameras.
Allwinner's chipset allows us to program the pins as general input/output pins and
since using CHIP as a robot does not require using a LCD panel we can use the same output pins controlling the servo motors or reading input from the sensors.



##Daughterboard

###Daughterboard schematics


The sumo robot needs interfaces to communicate with the servo and sensors. SumoCHIP schema has interfaces between CHIP's headers and infra red distance sensors, line following sensors, servo engines and diagnostic LEDs:

![Circuit](https://rawgithub.com/laurivosandi/sumochip/master/pcb/sumochip.sch.svg)
Schema
Noted on the schema are pin headers noted as P, LEDs noted as D, (photo)transistors noted as Q.

The operation of the robot is simple, with it having 8 infrared emitters, that are switched on during competition and the light reflected from those emitters will be detected with 8 infrared phototransistors.
The field transistor Q6 is used to turn infrared emitters in and out via the D1, D6-D9 and P13-P15 connections. In standby mode it is optimal to switch the diodes off, as they consume a bit of current.
In dark conditions the pull up resistor will ensure digital 1. If light is sensed by phototransistor(Q1-Q5 and P10-P12 on the schema) it will open and pull down the digital input towards 0. This helps the software detect
the presence of objects infront of the robot. The sensors soldered onto the daughterboard are used to identify opposing robots. The sensors for detecting the line are connected via P10-12 and P13-15.


###Acquiring the PCB


Connecting your robot via wires is clunky and fire hazard is increased. Due to aforementioned reasons it would be advised to get the PCB that implements the schema.

There are 4 options to obtain SumoCHIP :

* Buy from IT College's Robotics Club
* Rout by a CNC machine
* Etch at home
* Order from DirtyPCB

Kicadi projekti leiab Git lähtekoodivaramust, sellest saab eksportida LinuxCNC jaoks sobivas formaadis failid.
 Freesimine käib kolmes etapis: esmalt freesitakse V-tüüpi otsikuga alumine pool (back.ngc); seejärel puuritakse augud (drill.ngc);
  jargnevalt pööratakse trükkplaat ümber, kinnitatakse külgmistesse aukudesse ning lõpuks freesitakse trükkplaadi ülemine pool (front.ngc).
   Näide CNC masinaga trükkplaadi freesimisest:
Suitable files for LinuxCNC can be found on Kicad's project on Git source code repository.
Routing will be done in 3 stages: Routing the back side (back.ngc); Afterwards holes are drilled(drill.ngc);
Following flip the PCB, fasten it and rout the top side(front.ngc).

Example of the PCB:

![Picture of routing](../img/cnc-milling-pcb.jpg)



###Soldering the components

The following schematic is helpful when soldering:

![PCB layout](https://rawgit.com/laurivosandi/sumochip/8c88d02933c06c37d371292771ff80047eec376a/pcb/sumochip-brd.svg)

Soldering order:

0. Solder resistors R1-R20
0. Solder headers P1-P16
0. Solder field transistor Q6
0. Solder infrared light diodes D1, D6-D8
0. Solder infrared phototransistors Q1-Q4
0. Solder light diodes D2-D5

###Testing the PCB

Use a tester to verify that the following points do not create a short circuit:

* Ground and 3.3V traces
* Ground and 5V traces
* 3.3V ja 5V traces

[Return to main page](index-en.md "Main page")
[Assembly](assembly-en.md "Assembly")
