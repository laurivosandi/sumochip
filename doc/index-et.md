#SumoCHIP

##Sissejuhatus

Sumoroboti komplekti kuuluvad: SumoCHIP tütarplaat, CHIP emaplaat, liitiumpolümeeraku, 20mm ning 30mm distantskruvid, plaadid kere jaoks, kaks servomootorit, joonejälgimisandurid, mutrid, poldid, alumiiniumleht šablooniga saha jaoks ning termorüüž vastase andurite varjestamiseks.

![Stuff](img/kit/00-components.jpg)

Lisaks on vaja akutrelli, 3mm metallpuuri, plekikääre, kruvikeerajat, näpitsaid. Trükkplaadi jootmiseks on vaja ka jootekolbi, tina ning kampoli.

[TOC]

## Komponendid

Järgnevalt on välja toodud 10 roboti ehitamise jaoks vajalikud komponendid ning umbkaudne kulu koos saatmisega Euroopa Liitu. Kauba sisenedes EU-sse võivad lisanduda veel importmaksud:

| Pilt                                  | Kirjeldus                              | Hulk     | Rida kokku |
|---------------------------------------|----------------------------------------|----------|------------|
| ![CHIP](img/chip.png)                 | NextThingCo C.H.I.P.                   | 10tk     |  94.32 EUR |
| ![Servo](img/pservo.png)              | Plastik hammasratastega servo FS90R    | 20tk     |  63.63 EUR |
| ![Spoked wheel](img/spoked-wheel.png) | Rattad                                 | 20tk     |  34.70 EUR |
| ![LiPo](img/lipo.png)                 | Liitiumpolümeeraku 3.7V 1100mAh        | 10tk+    |  51.46 EUR |
| ![PCB](img/sumochip.png)              | SumoCHIP trükkplaat MakerStudiost      | 10tk     |  15.20 EUR |
| ![IR](img/ir-led.png)                 | Infrared emitter and receiver          | 50 paari |   3.91 EUR |
| ![SMD resistor](img/smd-resistor.jpg) | 100 ohm resistors                      | 120tk    |   1.20 EUR |
| ![SMD resistor](img/smd-resistor.jpg) | 10k ohm resistors                      | 30tk     |   0.60 EUR |
| ![SMD resistor](img/smd-resistor.jpg) | 100k ohm resistors                     | 50tk     |   0.60 EUR |
| ![Päis](img/straight-header.jpg)      | 40-pin 2.54mm male straight header     | 13tk     |   1.02 EUR |
| ![Päis](img/angled-header.jpg)        | 40-pin 2.54mm male angled header       | 1tk      |   0.44 EUR |
| ![SMD LED](img/smd-led.jpg)           | LED-ide assortii                       | 50pcs    |   0.98 EUR |
| ![2N7000](img/2n7000.jpg)             | 60V 200mA N-channel MOSFET             | 10pcs    |   0.85 EUR |
|                                       |                                        | Kokku:   | 270    EUR |
|                                       |                                        | Robot:   |  27    EUR |

Lingid hankimiseks:

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

###Alternatiivsed komponendid

Valikulised asenduskomponendid

| Pilt                      | Kirjeldus                    | Hulk | Hind       | Vahesumma | Hinnavahe |
|---------------------------|------------------------------|------|------------|-----------|-----------|
| ![Servo](img/mservo.png)  | Metallhammasratastega servo  | 2tk  |   4.86 EUR |  9.72 EUR | +3.40 EUR |
| ![Wheel](img/wheel.png)   | Servo ratas                  | 2tk  |   2.19 EUR |  4.38 EUR | +0.94 EUR |
| ![OPB745](img/opb745.jpg) | Optek OPB745 jooneanduriks   | 3tk  |   3.00 EUR |  9.00 EUR | +9.00 EUR |

Lingid hankimiseks:

- http://www.aliexpress.com/item/Smart-car-tires-steering-wheel-tire-tire-rubber-tire-tracking-DIY-model-toy-car-accessories-aperture/2055170090.html
- http://ee.farnell.com/optek-technology/opb745/photo-interrupter-reflective-3/dp/1497910


##Emaplaat

Sumorobotil kasutame ajuna CHIP nimelist arvutit mille hinnaks on umbkaudu 8€. CHIP emaplaadil on realiseeritud SoC (System on Chip) koos WiFi toega.

<img src="https://cdn.shopify.com/s/files/1/1065/9514/t/15/assets/chip1.png?5824758464935567530">

CHIP-il on päised LCD paneeliga ning CSI kaamera liidestamiseks. Kuna Allwinneri kiibistik võimaldab neid jalgu programmeerida üldotstarbeliste sisend/väljundviikudena ja roboti puhul LCD paneelile rakendust pole, saab samu väljaviike kasutada servomootorite juhtumiseks või sensoritest sisendi lugemiseks.



##Tütarplaat

###Tütarplaadi skeem

Sumoroboti jaoks on vaja teha liidestused mootorite ning sensoritega. SumoCHIP skeemis on loodud liidestused CHIP-i päiste ning infrapuna kaugussensorite, joonejälgimissensorite, servomootorite ja diagnostiliste tuledega:

![Circuit](https://rawgithub.com/laurivosandi/sumochip/master/pcb/sumochip.sch.svg)

Skeemis on P abil märgistatud piikribad, D abil valgusdioodid, Q abil (foto)transistorid.

Roboti tööpõhimõte on üsna lihtne, robotil on kaheksa infrapunadioodi, mis lülitatakse võistlemise ajaks sisse, ning neist dioodidest tagasi peegelduvat valgust tuvastatakse kaheksa infrapuna fototransistoriga. Skeemis märgitud väljatransistor Q6 on kasutusel tütarplaadile joodetud D1, D6-D9 ning P13-P15 kaudu ühendatud infrapunadioodide sisse-välja lülitamiseks. Jõudeolekus on otstarbekas dioodid välja lülitada, muidu tarbivad nad asjata märgatava hulga voolu. Päise P7-8 jalgu tüüritakse vaikimisi läbi takistite 3.3V suunas, kuid tütarplaadile joodetud Q1-Q5 ning P10-P12 kaudu ühendatud fototransistorite avanedes peegeldunud või keskkkonna valguse tõttu tõmmatakse pinge 0V ligi. Tarkvaraliselt loogikaväärtusi kontrollides nendel jalgadel saab tuvastada, kas sensori ees on midagi (0V ehk *false*) või ei ole midagi (3.3V ehk *true*). Tütarplaadile joodetud sensorid on kasutusel vastase tuvastamiseks ning läbi P10-12 ja P13-15 kaudu on ühendatud joonejälgimissensorid.

###Trükkplaadi hankimine

Juhtmetega liidestuse tegemine on kohmakas ning on oht teha vigu, mistõttu võib kogu plaat maha põleda. Seetõttu on soovitatud hankida trükkplaat, mis ülalnimetatud skeemi realiseerib.

SumoCHIP trükkplaadi hankimiseks on laias laastus neli varianti:

* Osta IT Kolledži robootikaklubist
* Freesida CNC abil
* Söövitada koduste vahenditega
* Tellida DirtyPCB-st

Kicadi projekti leiab Git lähtekoodivaramust, sellest saab eksportida LinuxCNC jaoks sobivas formaadis failid. Freesimine käib kolmes etapis: esmalt freesitakse V-tüüpi otsikuga alumine pool (back.ngc); seejärel puuritakse augud (drill.ngc); jargnevalt pööratakse trükkplaat ümber, kinnitatakse külgmistesse aukudesse ning lõpuks freesitakse trükkplaadi ülemine pool (front.ngc). Näide CNC masinaga trükkplaadi freesimisest:

![Pilt freesimisest](img/cnc-milling-pcb.jpg)



###Komponentide jootmine

Komponentide jootmisel on abiks järgnev joonis:

![PCB layout](https://rawgit.com/laurivosandi/sumochip/8c88d02933c06c37d371292771ff80047eec376a/pcb/sumochip-brd.svg)

Jootmise järjekord:

0. Jooda takistid R1-R20
0. Jooda päised P1-P16
0. Jooda väljatransistor Q6
0. Jooda infrapuna valgusdioodid D1, D6-D8
0. Jooda infrapuna fototransistorid Q1-Q4
0. Jooda valgusdioodid D2-D5

###Plaadi testimine

Kontrolli testeriga, et omavahel lühises ei oleks:

* Maa ja 3.3V rajad
* Maa ja 5V rajad
* 3.3V ja 5V rajad


##Roboti kokku panemine

###Mootorite monteerimine

Kinnita distantskruvid ühele kere jaoks ette nähtud plaatidest:

![Base assembled](img/kit/10-base-assembled.jpg)

Kleebi ühele servomootorile kahepoolne teip nagu näidatud pildil:

![Servo taping](img/kit/11-servo-taping.jpg)

Eemalda kahepoolse teibi eraldamiskile:

![Servo taping](img/kit/13-servo-tape-peeling.jpg)

Aseta servod tasapinnale ning suru üksteise vastu:

![Servo taping](img/kit/14-servos-aligned.jpg)

Niiviisi saad servod üksteise külge ühendatud üsna täpselt:

![Servo taping](img/kit/15-servos-taped.jpg)

Lisa mõlemale servole veel kahepoolset teipi:

![Servo taping](img/kit/16-servos-tape-peeling.jpg)

Suru servod eelnevalt kokku monteeritud raamile:

![Servos attached](img/kit/17-servos-attached.jpg)

Lisa teine kere plaat ning kinnita see poltidega:

![Bottom attached](img/kit/18-bottom-attached.jpg)


###Saha monteerimine

Prindi saha šabloon kleebitavale paberile. Kleebi prinditud šabloon alumiiniumlehe kaitsekilele. Lõika plekikääridega välja sahk. Aseta sahk katkendjoone järgi kruustangide vahele nagu näidatud pildil:

![Bottom attached](img/kit/20-plow.jpg)

Vääna väljaulatuv osa 90 kraadi:

![Bottom attached](img/kit/21-plow.jpg)

Eemalda sahk kruustangide vahelt ning voldi sahk käsitsi kokku:

![Bottom attached](img/kit/22-plow.jpg)

Kruustangide abil suru voltimisjoon veelgi rohkem kokku:

![Bottom attached](img/kit/23-plow.jpg)

Vääna väljaulatuv osa 45 kraadi:

![Bottom attached](img/kit/24-plow.jpg)

Vaheta pooled ning suru ka teine pool kokku:

![Bottom attached](img/kit/25-plow.jpg)

Puuri augud 3mm puuri abil punasega näidatud punktidesse:

![Bottom attached](img/kit/26-plow.jpg)

Eemalda kile koos šablooniga:

![Bottom attached](img/kit/27-plow.jpg)

Sahk ongi nüüd välja lõigatud:

![Bottom attached](img/kit/28-plow.jpg)

Monteeri sahk roboti kerele poltide abil:

![Bottom attached](img/kit/29-plow.jpg)






###Aju ühendamine

Kuna tütarplaadi jootmisel võib nii mõndagi nihu minna peaks tütarplaati enne emaplaadi külge ühendamist hoolikalt kontrollima. CHIP-i toiteploki võib üsna kergesti maha põletada kui näiteks CHIP käivitada nii et 5V rada või 3.3V rada on lühises maaga.

Lõika termorüüžist ~1cm pikkused jupid ning kata nendega fototransistorid:

![Enemy sensors](img/kit/42-enemy-sensors-covered.jpg)

Kasuta välgumihklit, et termorüüzi kuumutada. Selle tulemusena peaks termorüüž olema fikseeritud fototransistori suhtes:

![Enemy sensors](img/kit/43-enemy-sensors-shrunk.jpg)

Ühenda CHIP tütarplaadi külge nii et päised oleks kohakuti ning lüliti oleks USB pesa poolel.

![Enemy sensors](img/kit/44-attaching-daughterboard.jpg)

Ühenda aku tütarplaadi aku päise külge nii, et aku positiivne juhe (tüüpiliselt punane) jääb lüliti poole:

![Battery connected](img/kit/45-battery-connected.jpg)

Aku ühendamisel peab olema erakordselt tähelepanelik kuna aku tagurpidi ühendamisel kahjustub CHIP-i toiteplokk!

Aku fikseerimiseks kasuta kahepoolset teipi, vajadusel püga CHIP-ilt väljaulatuvaid jalgu mis võivad akusse augu lüüa:

![Taping battery](img/kit/47-taping-battery.jpg)

Roboti aju kokku monteerituna:

![Brain assembled](img/kit/48-brain-assembled.jpg)

Servomootorite juhtmete pakkimiseks kasuta pildil näidatud varianti:

![Wrapping servo wires](img/kit/50-wrapping-servo-wires.jpg)

Veendudes, et akut liiga tugevalt kokku ei surutaks fikseeri aju kere suhtes mutrite abil:

![Brain fixed](img/kit/52-brain-fixed.jpg)


###Joonejälgimisandurite ühendamine

Poltide ning mutrite abil monteeri joonejälgimisandurid saha külge:

![Line sensors](img/kit/31-line-sensors-attached.jpg)

Eemalda parempoolne ratas ning ühenda jooneandurite LED-id servo päiste kõrvale ning fototransistorid ratta taha peitu jäävate päiste külge. Midagi halba ei juhtu kui sensorid tagurpidi ühendada:

![Line sensors wired](img/kit/53-line-sensors-wired.jpg)


###Robot valmis

Viimane samm on veel kinnitada rattad kruvidega:

![Robot assembled](img/kit/60-robot-assembled.jpg)

Roboti käivitamiseks lülita sisse tütarplaadil olev lüliti, see on aku mehhaaniliselt eraldamiseks robotist selleks et roboti saaks pikemaks ajaks hoiustada kahjustamata akut. Vajadusel vajuta ettevaatlikult korraks ka CHIP-il olevat power on nuppu:

![Powering on](img/kit/61-powering-on.jpg)

Selle tulemusena peaks CHIP-i micro-USB pesa kõrval olevad valgusdioodid sisse lülituma.

##Tarkvara

Sumoroboti baastarkvara on kirjutatud Python programmeerimiskeeles kasutades Flask veebirakenduste raamistikku. Baastarkvara lähtekood on kättesaadav GitHubist aadressil https://github.com/laurivosandi/sumochip ning parandused ning täiendused on teretulnud.


###Tarkvara paigaldus

Sumorobotit saab veebi kaudu programmeerida aga selleks et seda üldse teha on vaja robotisse esmalt paigaldada veebirakendus. Piisab sellest, et järgnevad sammud üks kord läbi teha roboti peal.

Kuna CHIP-il pole videoväljundeid on kuvari ühendamine problemaatiline. Eelistatud on hoopiski üle USB kaabli jadaliidese kasutamine selleks, et robotile teha esmane seadistus. Windows puhul on vaja paigaldada ohjurtarkvara, et üldse USB kaablit kasutada saaks. Mac OS X ning Linux puhul seda teha vaja pole.

![Serial](img/kit/62-connecting-via-usb.jpg)

###Ohjurtarkvara paigaldus

Ubuntu ning Mac OS X all ohjurtarkvara paigaldada pole vaja, Windowsi puhul on asi mõnevõrra keerukam. Ava *Device Manager*:

![Device manager](img/usbser/01.png)

Leia nimistust kollase kolmnurgaga *CDC Composite Gadget* ning tee parem klõps sellel ning vali menüüst *Update Driver Software...*:

![Device manager](img/usbser/02.png)

Järgnevalt vali *Browse my computer for driver software*:

![Device manager](img/usbser/03.png)

Seejärel vali *Let me pick from a list of device drivers on my computer*:

![Device manager](img/usbser/04.png)

Jäta valituks *Show All Devices* ning klõpsa *Next* nupul:

![Device manager](img/usbser/05.png)

Keri vasakpoolses nimekirjas allapoole ning vali *Microsoft* seejärel keri parempoolses nimekirjas alla ning vali *USB Serial Device*:

![Device manager](img/usbser/06.png)

Hoiatusaknas klõpsa *Yes* nupul:

![Device manager](img/usbser/07.png)

Ohjurtarkvara peaks olema seejärel edukalt paigaldatud:

![Device manager](img/usbser/08.png)

Seadmete nimekirja peaks tekkima uus *USB Serial Device* seade. Jäta selle jadaliidese number meelde, järgneval kuvatõmmisel on ta nimeks COM6:

![Device manager](img/usbser/09.png)


###Jadaliidese avamine

Jadaliidese kasutamiseks võivad Windowsi kasutajad pruukida [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) nimelist programmi. Ubuntu ning teiste UNIX-ilaadsete operatsioonisüsteemide all võib kasutada `screen`, `picocom` vms programme. Jadaliides võimaldab ligipääsu CHIP-i sees käiva tarkvara käsureale nii nagu paljude teiste nutiseadmete puhul. CHIP kasutab operatsioonisüsteemina Debiani ning paljud Ubuntust tuttavad käsud toimivad seal täpselt samamoodi.


###Robotisse sisse logimine

Kasutajanimi on *root* ning parool on *chip*.


###Võrgu seadistamine

Esmalt ühenda CHIP WiFi kaudu Internetti, selleks saad kasutada NetworkManageri pseudograafilist kasutajaliidest:

```bash
nmtui
```

Interneti ühenduse olemasolus saad veenduda näiteks `ping` abil, vajuta Ctrl-C et katkestada:

```bash
ping neti.ee
```

Kuna CHIP-il pole akut ega kella mis aja üle arvestust peaks püüab CHIP peale võrguühenduse loomist kellaaega küsida Internetist aga mõnikord võib see ebaõnnestuda. Kellaaja kontrollimiseks saab kasutada järgnevat käsku, turvalised ühendused Internetti (nt GitHub) kipuvad ebaõnnestuma kui kell on vale:

```bash
date
```


###Operatsioonisüsteemi uuendamine

Kui võrguühendus on olemas võime teha CHIP-i operatsioonisüsteemile tarkvarauuenduse:

```bash
apt update       # Uuenda pakettide nimekirju
apt full-upgrade   # Uuenda pakette
```


### Sõltuvuste paigaldamine

Paigalda sõltuvused ning Git versioonihaldustarkvara:

```bash
apt install python-pip python-dev git
```

###Sumoroboti tarkvara paigaldus

Seejärel võime paigaldada sumoroboti tarkvara:

```bash
pip install sumochip
```

Kui kõik on seni sujuvalt kulgenud võib välja uurida mis IP aadressil CHIP asub. Selleks saab kasutada käsku:

```bash
ifconfig
```

Proovi algatada SSH ühendus robotisse, Windowsis saab selleks kasutada PuTTY-t ning UNIX-iliste all:

```bash
ssh <ip-aadress>
```

###Sumoroboti tarkvara seadistamine

Paigalda konfiguratsioonifail mis ütleb mis jalgade külge servomootorid ja sensorid ühendatud on:

```bash
mkdir -p /etc/sumorobot/
curl https://raw.githubusercontent.com/artizirk/sumochip/master/sumochip/config/sumochip_v1.1.ini > /etc/sumorobot/sumorobot.ini
```


Käivita testprogramm, katkestamiseks vajuta jällegi Ctrl-C:

```bash
sumochip_test
```

Kontrolli, et jooneandurite LED-id toimivad. Selleks vaata jooneanduritesse mobiiltelefoni kaamera kaudu. Kaameras paistab infrapuna violetsena:

![Checking line sensors](img/kit/63-checking-line-sensors.jpg)

Soorita sama kontroll ka vastase tuvastamise sensoritel:

![Checking enemy sensors](img/kit/64-checking-enemy-sensors.jpg)



Proovi käivitada ka veebiliides:

```bash
sumochip_web
```


Kui on vaja robotit viisakalt kinni panna siis selle jaoks saab kasutada käsku:

```bash
shutdown -h now
```


##Terminaliga ringi käimine

###Enimkasutatavad käsud

CHIP-i peal kasutatavad käsud töötavad täpselt samamoodi Raspberry Pi ning Ubuntu peal:

* Praeguse kataloogi tuvastamine: `pwd`
* Failide ning kataloogide nimekirja kuvamine praeguses kataloogis: `ls -lah`
* Sisene kataloogi: `cd katalooginimi`
* Mine ülemisse kataloogi: `cd ..`
* Faili kustutamine: `rm failinimi`

###Failide redigeerimine terminalis

CHIP-il nagu paljudel teistel Linuxilistel on kohe kaasas tekstiredaktor `nano`, selleks et faili avada selle programmiga:

```bash
nano tee/failini.py
```
Kasuta klahvikombinatsiooni Ctrl-K et teksti paigutada lõikepuhvrisse ning Ctrl-U et neid uude valitud kohta kleepida. Ctrl-X abil saab salvestada faili ning programmist väljuda.

Pisut mugavam tekstiredaktor on Midnight Commander koosseisus, selle paigaldamiseks:

```Bash
apt install mc
```

Failide avamine käib samamoodi:

```bash
mcedit tee/failini.py
```
Menüüdes navigeerimine käib analoogselt graafiliste rakendustega, Alt-F avab peamenüü. Kiirklahvidest kõige olulisemad on F5 kopeerimiseks, F6 lõikamiseks ning F10 programmist väljumiseks.
