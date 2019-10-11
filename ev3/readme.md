# EV3 - RoboRinth App

Die EV3 Roboter so konfiguriert das eine RoboRinth App nach dem Bootvorgang gestartet wird. Die App verbindet sich mit einem MQTT Broker und stellt ein MQTT Interface zur Verfügung zum Lesen und Schreiben von Sensoren/Aktoren

## Konfiguration

Die Konfiguration für die Applikation liegt auf dem Filesystem der EV3 roboter unter **/home/robot/roborinth/config/config.json**. 
Unter anderem kann die IP Adresse des MQTT Hosts angepasst werden.

## MQTT API

Jeder Roboter kann Nachrichten publishen und empfangen. **Das Root-Topic ist jeweils die ID des Roboters**. Z.B. robo-01

Über MQTT können folgende Typen von Nachrichten gesendet werden:
 - **requests** werden vom Roboter ausgeführt, das Resultat wird als **response** gepublished
 - Mit **subscribe** und **unsubscribe** können Notifikationen aktiviert werden
 - **notification** Nachrichten werden mit einer einstellbaren Periode vom Roboter gepublished

Die Notifikationsperiode beträgt standarmässig 1 Sekunde.
 
**Achtung:** Der ev3 ist nicht besonders leistungsfähig. Bei zuvielen Notifikations-subscriptions gleichzeitig und zu kurzer Notifikationsperiode kann die Applikation instabil werden.


### Requests and Responses

Note: 
- Data is always send as plain string
- Each topic has to be prefixed with robot-id. e.g. `robo-01/request/gyro/angle` 

|Request-Topic                |Data                                     | Description |
|---|---|---|
|`request/ctrl `              |`char`                                   |`Q` to quit<br>Command for debug purpos |
|`request/txt `               |`string`                                 |text to be displayed on ev3 Screen<br> for debug purpose|
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
|`request/gyro/reset`         |-                                        |see response|
|`request/motor/present`      |-                                        |see response|
|`request/motor/position`     |-                                        |see response|
|`request/motor/reset`        |-                                        |see response|
|`request/motor/turn`         |`{"speed":"x","angle":"y"}`              |`-100 <= x <= 100`<br> `y has to be an int`|
|`request/motor/activate`     |`int`                                    |speed value from -100 to 100|
|`request/steering/present`   |-                                        |see response|
|`request/steering/activate`  |`{"speed":"x","steering":"y"}`           |see [MoveSteering](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/motors.html#move-steering)|
|`request/steering/reset`     |-                                        |see response
|`request/steering/turn`      |`{"speed":"x","steering":"y","angle":z"}`|[MoveSteering](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/motors.html#move-steering)|
|`request/power/voltage`      |-                                        |see response|
|`request/power/current`      |-                                        |see response|
|`request/notper`             |`int`                                    |set notification period in milliseconds<br>value must be between 10 and 10000<br>default is 1000|


|Response-Topic                |Data           |Description|
|---|---|---|
|`response/ctrl`               |`bool`         |Command for debug purpose |
|`response/txt`                |`bool`         |Displays Text on ev3 Screen (debug)|
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
|`response/gyro/reset`         |`bool`         |reset angle to 0|
|`response/motor/present`      |`bool`         |returns `True` if MediumMotor is present<br>in case of `False` motor topics return **invalid** values|
|`response/motor/position`     |`int`          |read position of MediumMotor in degrees (Motor may be used as sensor)|
|`response/motor/reset`        |`bool`         |reset position to 0|
|`response/motor/turn`         |`bool`         |turn MediumMotor with given speed to given angle in degrees<br>angle is relative<br>speed goes from -100 to 100|
|`response/motor/activate`     |`bool`         |set speed value to MediumMotor<br>speed goes from -100 to 100|
|`response/steering/present`   |`bool`         |returns `True` if [MoveSteering](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/motors.html#move-steering) is present<br>in case of `False` steering topics return  **invalid** values|
|`response/steering/activate`  |`bool`         |start moving the robot with given speed and steering value<br>speed goes from -100 to 100<br>steering value impacts the radius<br>the value goes from -100 to 100<br> where as 0 means "straight line" and -100/100 "turn on point"|
|`response/steering/reset`     |`bool`         |reset steering releases "brakes" which are set after requesting "turn"|
|`response/steering/turn`      |`bool`         |turn the robot with given speed, steering, and angle.<br>the angle refers to the outer wheel in degrees|
|`response/power/voltage`      |`decimal`      |returns battery pack voltage in Volts|
|`response/power/current`      |`decimal`      |returns current draw in MilliAmps|
|`response/notper`             |`bool`         |`True` if request was successful<br>**to low value leads to system instability**

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
