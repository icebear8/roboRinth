# EV3 - RoboRinth App
Nach dem Bootvorgang wird automatisch eine RoboRinth Applikation gestartet. Die App verbindet sich mit einem MQTT Broker und stellt ein MQTT Interface zur Verfügung zum Lesen und Schreiben von Devices die am ev3 angeschlossen sind, z.B. ColorSensor und Motoren.
Die angeschlossenen Devices werden beim Applikationsstart automatisch detektiert und initialisiert. Es ist nur wichtig, dass Sensoren an den Input-Ports (markiert mit 1-4) und Aktoren an den Output-Ports (markiert mit A-D) angeschlossen werden. 
Auf dem Screen des ev3 wird die Roboter-ID sowie der Connection-Status angezeigt. Zudem signalisieren die LEDs den Connection-Status (grün = ok, orange = keine Verbindung).
Bei Verbindungsverlust versucht die Applikation automatisch wieder Kontakt zum Broker herzustellen.

## Konfiguration

Die Konfiguration für die Applikation liegt auf dem Filesystem der EV3 Roboter unter **/home/robot/roborinth/config/config.json**. 
Unter anderem kann dort die IP Adresse des MQTT Hosts angepasst werden. 

[Zugriff erfolgt mittels SSH.](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/)

[IP Adressen der Roboter](../infrastructure/readme.md)

## Weiterentwicklung & Deployment
Die vorkonfigurierte Python Applikation oder sonst eine Python/Java Applikation kann auf dem Host entwickelt werden und anschliessend z.B. mittels WinSCP aufs target deployed werden. Der systemd service **roborinth** startet die Applikation nach dem Bootvorgang automatisch.
Für eine C/C++ Anwendung gibt es zur Zeit keine Cross-Compilation Toolchain. Man müsste in diesem Fall auf dem Target kompilieren.

## MQTT API

Jeder Roboter sendet und empfängt Nachrichten unter einem speziellen **Root-Topic**, das der **ID des Roboters** entspricht. 
D.h. Der Roboter mit der ID `robo-01` sendet und empfängt nur Nachrichten unter dem Topic `robo-01/...`

Über MQTT können folgende Typen von Nachrichten gesendet werden:
 - Clients können **requests** publishen, welche vom Roboter verarbeitet werden, das Resultat wird als **response** gepublished
 - Clients können mit **subscribe** und **unsubscribe**  Notifikationen aktivieren/deaktivieren
 - **notification** Nachrichten werden mit einer einstellbaren Periode vom Roboter gepublished

Die Notifikationsperiode beträgt standardmässig 1 Sekunde.
 
**Achtung:** Der ev3 ist nicht besonders leistungsfähig. Bei zuvielen, gleichzeitigen Notifikations-Subscriptions und zu kurzer Notifikationsperiode kann die Applikation instabil werden. 

**Info**: Aufgrund von Stabilitätsproblemen sind Ultraschall-Distanzsensor, Drucksensor und Servomotor zur Zeit deaktiviert. Diese Devices werden für die Challenge aber vermutlich nicht benötigt.

### Requests and Responses

Note: 
- Data is always send as plain string
- Each topic has to be prefixed with robot-id. e.g. `robo-01/request/gyro/angle` 

|Request-Topic                |Data                                     | Description |
|---|---|---|
|`request/color/present`      |-                                        |see response|
|`request/color/reflected`    |-                                        |see response|
|`request/color/ambient`      |-                                        |see response|
|`request/color/id`           |-                                        |see response|
|`request/color/name`         |-                                        |see response|
|`request/color/raw`          |-                                        |see response|
|`request/touch/present`      |-                                        |see response|
|`request/touch/pressed`      |-                                        |see response|
|`request/ultrasonic/present` |-                                        |see response|
|`request/ultrasonic/distance`|-                                        |see response|
|`request/gyro/present`       |-                                        |see response|
|`request/gyro/angle`         |-                                        |see response|
|`request/gyro/reset`         |-                                        |reset angle to 0<br>the response returns immediately<br> but it takes a few seconds until the angle is set to 0|
|`request/motor/present`      |-                                        |see response|
|`request/motor/position`     |-                                        |see response|
|`request/motor/reset`        |-                                        |see response|
|`request/motor/turn`         |`{"speed":"x","angle":"y"}`              |`-100 <= x <= 100`<br> `y has to be an int`|
|`request/motor/activate`     |`int`                                    |speed value from -100 to 100|
|`request/steering/present`   |-                                        |see response|
|`request/steering/activate`  |`{"speed":"x","steering":"y"}`           |start moving the robot with given speed and steering value<br>speed goes from -100 to 100<br>steering value impacts the radius<br>the value goes from -100 to 100<br> where as 0 means "straight line" and -100/100 "turn on point"<br>see [MoveSteering](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/motors.html#move-steering)|
|`request/steering/reset`     |-                                        |reset steering releases "brakes" which are set after requesting "turn"|
|`request/steering/turn`      |`{"speed":"x","steering":"y","angle":z"}`|turn the robot with given speed, steering, and angle.<br>the angle refers to the outer wheel in degrees<br>[MoveSteering](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/motors.html#move-steering)|
|`request/power/voltage`      |-                                        |see response|
|`request/power/current`      |-                                        |see response|
|`request/notper`             |`int`                                    |set notification period in milliseconds<br>value must be between 10 and 10000<br>default is 1000|
|`request/ctrl `              |`char`                                   |`Q` to quit<br>Command for debug purpos |
|`request/txt `               |`string`                                 |text to be displayed on ev3 Screen<br> for debug purpose|


|Response-Topic                |Data           |Description|
|---|---|---|
|`response/color/present`      |`bool`         |returns `True` if ColorSensor is present<br>in case of `False` color topics return **invalid** values|
|`response/color/reflected`    |`int`          |read reflected light intensity from [ColorSensor](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/sensors.html#color-sensor)|
|`response/color/ambient`      |`int`          |read ambient light intensity from [ColorSensor](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/sensors.html#color-sensor)|
|`response/color/id`           |`int`          |read currently detected color's id<br>[ColorSensor](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/sensors.html#color-sensor)|
|`response/color/name`         |`string`       |read currently detected color's name<br>[ColorSensor](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/sensors.html#color-sensor)|
|`response/color/raw`          |`(int,int,int)`|read [ColorSensor](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/sensors.html#color-sensor) Raw Values in RGB as tuple|
|`response/touch/present`      |`bool`         |returns `True` if TouchSensor is present<br>in case of `False` touch topics return **invalid** values|
|`response/touch/pressed`      |`bool`         |returns `True` if TouchSensor is currently pressed|
|`response/ultrasonic/present` |`bool`         |returns `True` if UltrasonicSensor is present<br>in case of `False` ultrasonic topics return **invalid** values|
|`response/ultrasonic/distance`|`decimal`      |read distance in centimeter (0.0-255.0)|
|`response/gyro/present`       |`bool`         |returns `True` if [GyroSensor](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/sensors.html#gyro-sensor) is present<br>in case of `False` gyro topics return **invalid** values|
|`response/gyro/angle`         |`int`          |read angle in degrees<br> clockwise turn --> positive angle<br>counterclockwise turn --> negative angle<br>angle has no boundaries may be <-360 or >360|
|`response/gyro/reset`         |`bool`         |`True` if request was successful|
|`response/motor/present`      |`bool`         |returns `True` if MediumMotor is present<br>in case of `False` motor topics return **invalid** values|
|`response/motor/position`     |`int`          |return position of MediumMotor in degrees (Motor may be used as sensor)|
|`response/motor/reset`        |`bool`         |`True` if request was successful|
|`response/motor/turn`         |`bool`         |`True` if request was successful|
|`response/motor/activate`     |`bool`         |`True` if request was successful|
|`response/steering/present`   |`bool`         |returns `True` if [MoveSteering](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/motors.html#move-steering) is present<br>in case of `False` steering topics return  **invalid** values|
|`response/steering/activate`  |`bool`         |`True` if request was successful|
|`response/steering/reset`     |`bool`         |`True` if request was successful|
|`response/steering/turn`      |`bool`         |`True` if request was successful|
|`response/power/voltage`      |`decimal`      |returns battery pack voltage in Volts|
|`response/power/current`      |`decimal`      |returns current draw in MilliAmps|
|`response/notper`             |`bool`         |`True` if request was successful<br>**to low value leads to system instability**
|`response/ctrl`               |`bool`         |`True` if request was successful|
|`response/txt`                |`bool`         |`True` if request was successful|

### Notifications

Note: 
- Data is always send as plain string
- Each topic has to be prefixed with robot-id. e.g. `robo-01/request/gyro/angle` 

for detailed info on notification data see request/response descriptions

|Topic                                    |Data |
|---|---|
|`notification/color/present`             |`bool`            |
|`notification/color/reflected`           |`int`             |
|`notification/color/ambient`             |`int`             |
|`notification/color/id`                  |`int`             |
|`notification/color/name`                |`string`          | 
|`notification/color/raw`                 |`(int,int,int)`   |
|`notification/touch/present`             |`bool`            |
|`notification/touch/pressed`             |`bool`            |
|`notification/ultrasonic/present`        |`bool`            |
|`notification/ultrasonic/distance`       |`decimal`         |
|`notification/gyro/present`              |`bool`            |
|`notification/gyro/angle`                |`int`             |
|`notification/motor/present`             |`bool`            |
|`notification/motor/position`            |`int`             |
|`notification/steering/present`          |`bool`            |
|`notification/power/voltage`             |`decimal`         |
|`notification/power/current`             |`decimal`         |

#### subscribe

Enable notifications by publishing one or more of the following messages.

**Attention:** To many subscriptions can lead to system instability.

|Topic                            |Request-Data |
|---|---|
|`subscribe/color/present`        |-            |
|`subscribe/color/reflected`      |-            |
|`subscribe/color/ambient`        |-            |
|`subscribe/color/id`             |-            |
|`subscribe/color/name`           |-            |
|`subscribe/color/raw`            |-            |
|`subscribe/touch/present`        |-            |
|`subscribe/touch/pressed`        |-            |
|`subscribe/ultrasonic/present`   |-            |
|`subscribe/ultrasonic/distance`  |-            |
|`subscribe/gyro/present`         |-            |
|`subscribe/gyro/angle`           |-            |
|`subscribe/motor/present`        |-            |
|`subscribe/motor/position`       |-            |
|`subscribe/steering/present`     |-            |
|`subscribe/power/voltage`        |-            |
|`subscribe/power/current`        |-            |

#### unsubsribe

Disable notifications by publishing one or more of the following messages.

|Topic                            |Request-Data |
|---|---|
|`unsubscribe/color/present`      |-            |
|`unsubscribe/color/reflected`    |-            |
|`unsubscribe/color/ambient`      |-            |
|`unsubscribe/color/id`           |-            |
|`unsubscribe/color/name`         |-            |
|`unsubscribe/color/raw`          |-            |
|`unsubscribe/touch/present`      |-            |
|`unsubscribe/touch/pressed`      |-            |
|`unsubscribe/ultrasonic/present` |-            |
|`unsubscribe/ultrasonic/distance`|-            |
|`unsubscribe/gyro/present`       |-            |
|`unsubscribe/gyro/angle`         |-            |
|`unsubscribe/motor/present`      |-            |
|`unsubscribe/motor/position`     |-            |
|`unsubscribe/steering/present`   |-            |
|`unsubscribe/power/voltage`      |-            |
|`unsubscribe/power/current`      |-            |
