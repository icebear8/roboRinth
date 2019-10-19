# roboRinth – Collaborative Robot Challenge

## Project Description

The goal is to examine a labyrinth of lines with multiple (2-3) robots, find an optimal path from start to finish and possibly collect tokens within the labyrinth

## :fire:Starting Point:fire:
- Plug & Play Network infrastructure: [Details details](infrastructure/readme.md)
- preconfigured MQTT Broker running on Raspberry Pi: [Details here](mqtt/mosquitto/readme.md)
- MQTT Client Application: [Details here](mqtt/mqttClient/readme.md)
- MQTT Spy:  [Details here](mqtt/mqttSpy)
- 3 preconfigured Lego Mindstorm Robots: [Details here](ev3/readme.md)

## Challenge Environment and Conditions

- 2-3 Lego Mindstorm robots
    - Actors (motors)
    - Sensors (brightness sensor, gyroscope, …)
    - ev3dev OS to run any code on the robot
    - MQTT client
    - WiFi dongle to communicate with server
- Raspberry Pi / PC as server
- Raspberry Pi's / PC's as MQTT clients

<img src="roboRinth_Project_Setup.png" alt="Setup" width="400"/>

### Idea of the challenge
- <https://www.youtube.com/watch?v=6K-78wloOzY>

### Proposition for team splitting
- 1 team logic on robots (sensors, actors, communication)
- 2 teams logic on server (data analysis, map composition, tasks & instructions)

### Time for project
- Start: Monday, 21st of October, after arrival
- End: Wednesday, 23rd of October, before lunch

### Programming language
- possibly Python

### Requirements to PC
- possibly Docker
- possibly VirtualBox

