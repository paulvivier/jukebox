#!/usr/bin/bash
# Add the following to `crontab -e``:
# @reboot sleep 5 && sh /home/pi/Documents/jukebox/src/check_volume.sh
# This will periodically check the volume button
cd /home/pi/Documents/jukebox/src/
watch -n5 python jukebox.py 13

