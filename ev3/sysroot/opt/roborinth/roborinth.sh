#!/bin/sh

echo "start roboClient"
cd /home/robot/roborinth/app
sudo chvt 6 #show an empty terminal on screen to avoid flickering
sudo -u robot python3 -u main.py
sudo chvt 1 #bring back brickman
