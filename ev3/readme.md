# EV3 - RoboRinth App

Die EV3 Roboter so konfiguriert das eine RoboRinth App nach dem Bootvorgang gestartet wird. Die App verbindet sich mit einem MQTT Broker und stellt ein MQTT Interface zur Verfügung zum Lesen und Schreiben von Sensoren/Aktoren

## Konfiguration

MQTT Host usw. können auf dem Filesystem der EV3 roboter unter **/home/robot/roborinth/config/config.json** angepasst werden. Ein Neustart der Applikation ist erforderlich damit die Änderungen wirksam werden.

## MQTT API

Note: Data is always send as string type

|Topic|Data|Response|
|---|---|---|
|'robo-0x/ctrl'|'Q'|void, Application is going to be terminated|
|'robo-0x/txt'| string |void, Show string on EV3 Display|
|'robo-0x/color/present'|don't care|"True"/"False" under topic './response'|
|'robo-0x/color/reflected'|don't care|"0.0" under topic './response'|
|'robo-0x/color/ambient'|don't care|xxx under topic './response'|
|'robo-0x/color/color'|don't care|xxx under topic './response'|
|'robo-0x/color/colorname'|don't care|xxx under topic './response'|
|'robo-0x/color/colorraw'|don't care|xxx under topic './response'|
|'robo-0x/touch/present'|don't care|xxx under topic './response'|
|'robo-0x/touch/pressed'|don't care|xxx under topic './response'|
|'robo-0x/ultrasonic/present'|don't care|xxx under topic './response'|
|'robo-0x/ultrasonic/distance'|don't care|xxx under topic './response'|
|'robo-0x/gyro/present'|don't care|xxx under topic './response'|
|'robo-0x/gyro/angle'|don't care|xxx under topic './response'|
|'robo-0x/gyro/reset'|don't care|xxx under topic './response'|
|'robo-0x/motor/present'|don't care|xxx under topic './response'|
|'robo-0x/motor/position'|don't care|xxx under topic './response'|
|'robo-0x/motor/reset'|don't care|void, motor is stopped and position set to 0|
|'robo-0x/motor/turn'|float| servo motor turns for given angle|
|'robo-0x/motor/activate'|float|servo motor starts running with given duty cycle|
|'robo-0x/steering/present'|don't care|xxx under topic './response'|
|'robo-0x/steering/activate'|{"steering":"x","speed":"y"|void, movement as per given steering parameters|
|'robo-0x/steering/reset'|don't care|xxx under topic './response'|
|'robo-0x/steering/turn'|float|void, turn by given angle|
