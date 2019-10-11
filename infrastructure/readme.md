# Infrastruktur

## Inbetriebnahme
Router, Roboter und Raspberry Pi Server sind vorkonfiguriert. Es muss also nur alles richtig eingesteckt werden und nach Power-On läuft das Netzwerk. 
Für Internetzugriff muss zusätzlich noch z.B. ein Mobile Router angehängt werden. Der WAN Port am RoboRinth Router ist auf Dynamic IP eingestellt.

## Netzwerk
<img src="RoboRinth Network.png" width="1000" >

## WLAN Zugriff
- SSID: *RoboRinth WLAN*
- Passwort: Siehe Kleber am RoboRinth Router
- 2.4GHz

## RoboRinth Router
- Modell: [Edimax br-6428ns_v4](https://www.edimax.com/edimax/merchandise/merchandise_detail/data/edimax/global/wireless_routers_n300/br-6428ns_v4/)
- Zugriff nur innerhalb LAN/WLAN
  - **[http://192.168.0.1](http://192.168.0.1)**
  - Logindaten: Siehe Kleber auf Geräterückseite
- WLAN Accesspoint
- 4x LAN Port
- 1x WAN Port

## Raspberry Pi MQTT Broker
- IP Addresse: **192.168.0.200**

## WLAN Dongle für Roboter
Die EV3 Roboter haben kein eingebautes WLAN. Es kann aber ein USB WLAN Dongle eingesteckt werden.
Folgender WLAN-Dongle wurde getestet und hat sich als zuverlässig erwiesen: [Edimax ew-7612uan_v2](https://www.edimax.com/edimax/merchandise/merchandise_detail/data/edimax/in/wireless_adapters_n300/ew-7612uan_v2/)

## Roboter 1
- Aus Lego Mindstorms EV3 Kit **Bern**
- Beschriftet mit **ROBO-01**
- **Achtung:** WLAN-Dongle mit Kleber **ANT-01** vor Power-On einstecken 
- **Achtung:** vorkonfigurierte SD-Karte nicht entfernen
- MAC Adresse: **08:be:ac:02:e4:25** (08beac02e425)
- IP Adresse: **192.168.0.201** (static DHCP lease)

## Roboter 2
- Aus Lego Mindstorms EV3 Kit **Bern**
- Beschriftet mit **ROBO-02**
- **Achtung:** WLAN-Dongle mit Kleber **ANT-02** vor Power-On einstecken
- **Achtung:** vorkonfigurierte SD-Karte nicht entfernen
- MAC Adresse: **08:be:ac:05:cd:f4** (08beac05cdf4)
- IP Adresse: **192.168.0.202** (static DHCP lease)

## Roboter 3
- Aus Lego Mindstorms EV3 Kit **Schlieren**
- Beschriftet mit **ROBO-03**
- **Achtung:** WLAN-Dongle mit Kleber **ANT-03** vor Power-On einstecken
- **Achtung:** vorkonfigurierte SD-Karte nicht entfernen
- MAC Adresse: **08:be:ac:05:cd:f3** (08beac05cdf3)
- IP Adresse: **192.168.0.203** (static DHCP lease)

# ev3dev
The Linux OS running on the EV3 robots. [https://www.ev3dev.org/](https://www.ev3dev.org/)

## Startup Configuration, Access and Deployment
See [ev3 preconfiguration](../ev3/readme.md)

## Preinstalled Tools
- Python 2.7.13
- Python 3.5.3
- gcc 6.3.0
- g++ 6.3.0
- java OpenJDK 11.0.2

# FAQ
- Ich komme mit SSH nicht auf den Roboter drauf, was tun?
  - Womöglich hat die IP-Adress-Reservierung nicht funktioniert und der Roboter hat eine andere IP Adresse bekommen als erwartet. 
    - Auf dem Display des EV3 wird die IP-Adresse angezeigt, insofern eine Verbindung besteht
    - Zudem kann man auf dem Router nachschauen welche Devices verbunden sind und welche IP Adressen sie haben: [http://192.168.0.1/admin_activeDhcpClient.asp](http://192.168.0.1/admin_activeDhcpClient.asp)
  - SSH Zugriff funktioniert NUR innerhalb des RoboRinth LAN/WLAN
- RoboRinth Router funktioniert nicht, was tun?
  - Falls eine Verbindung aufs Webinterface noch möglich ist
    - Es gibt einen System Log
    - Restore Settings mittels config file: [roborinth_router_config.bin](roborinth_router_config.bin)
    - Restore to Factory Default
  - Auf der Vorderseite hats einen kleinen Reset Knopf
