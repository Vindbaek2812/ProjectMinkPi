#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# This is for starting the Script in the correct directory
cd /
cd /home/pi/Documents/ProjectMinkPi #where the script is
sudo echo PiStartupScript.py is being started...
sudo -u pi python PiStartupScript.py #a commnad to run the script
cd /