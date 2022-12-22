#!/usr/bin/bash
# Add the following to `crontab -e``:
# @reboot /home/pi/Documents/jukebox/src/boot.sh
# This will turn the dash lights on as soon as it can light up.
raspi-gpio set 23 op dh
