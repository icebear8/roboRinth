# Mosquitto
[Mosquitto](https://mosquitto.org/) is an open source implementation of a server for version 5.0, 3.1.1, and 3.1 of the MQTT protocol. It also includes a C and C++ client library, and the mosquitto_pub and mosquitto_sub utilities for publishing and subscribing.

For the RoboRinth project we use Mosquitto as the MQTT broker.
The broker can run on a PC or on a Raspberry Pi.
A Docker image with mosquitto pre installed is prepared.

## Docker Image
The Mosquitto Docker image is maintained on [Github](https://github.com/icebear8/arctic/tree/master/mosquitto).

## Setup PC
* Precondition: Docker must be installed on the PC
* Download the Docker image: `docker pull icebear8/mosquitto:latest`
* Run the image: `docker run -p 1883:1883 icebear8/mosquitto`
  * Configuration: `docker run -p 1883:1883 -e SERVICE_ARGS="<additional config>" icebear8/mosquitto`

## Setup Raspberry Pi
Docker images for the Raspberry Pi are tagged with `-arm`.
* Precondition: Raspberry Pi with Docker installed
* Download the Docker image: `docker pull icebear8/mosquitto:latest-arm`
* Run the image: `docker run -p 1883:1883 icebear8/mosquitto:latest-arm`

### RancherOS
[RancherOS](https://rancher.com/rancher-os) is a lightweight, secure Linux distribution, built from containers to run containers well.

* Installation on Raspberry Pi: https://rancher.com/docs/os/v1.x/en/installation/running-rancheros/server/raspberry-pi/
