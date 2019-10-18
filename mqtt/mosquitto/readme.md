# Mosquitto
[Mosquitto](https://mosquitto.org/) is an open source implementation of a server for version 5.0, 3.1.1, and 3.1 of the MQTT protocol. It also includes a C and C++ client library, and the mosquitto_pub and mosquitto_sub utilities for publishing and subscribing.

For the RoboRinth project we use Mosquitto as the MQTT broker.
The broker can run on a PC or on a Raspberry Pi.
A Docker image with mosquitto pre installed is prepared.

## Docker Image
The Mosquitto Docker image is maintained on [Github](https://github.com/icebear8/arctic/tree/master/mosquitto).

## Setup PC
* Precondition: Docker must be installed on the PC
  * https://docs.docker.com/docker-for-windows/install/
  * Hint: VirtualBox must be deactivated to use Docker for Windows (Docker uses HyperV)
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
  * Initial user is `rancher` and  password is `rancher`

### BalenaOS
As an alternative to RancherOS, [BalenaOS](https://www.balena.io/os/) can be used instead.
BalenaOS comes with an additional framework to manage and deploy Docker containers.
Use the BalenaOS development version with the user `root` and SSH on port 22222 which is open and unsecured.

### Raspbian and Docker
To use Docker on Raspbian an install script is available under `https://get.docker.com`.
**Before executing the script it must be carefully reviewed, since it is executed with root access.**

Instructions
* https://blog.docker.com/2019/03/happy-pi-day-docker-raspberry-pi/
* or https://howchoo.com/g/nmrlzmq1ymn/how-to-install-docker-on-your-raspberry-pi

# Docker Image
[Mosquitto](https://mosquitto.org/) is an open source implementation of a server for version 5.0, 3.1.1, and 3.1 of the MQTT protocol. It also includes a C and C++ client library, and the mosquitto_pub and mosquitto_sub utilities for publishing and subscribing.

##  Changelog
* mosquitto:1.6.3-r3, Alpine v3.10.1 with mosquitto v1.6.3

# Usage
`docker run -p 1883:1883 icebear8/mosquitto`

##  Environment Variables

| Variable        | Description |
|-                |-            |
| SERVICE_ARGS    | Arguments for the mosquitto service at startup |
