import os

print("Updating the Raspberry Pi")
print("TODO")
print("Send a picture to CAN screen that says updating the Raspberry Pi")

#Updating the Raspberry Pi
os.system("sudo apt update")

#Getting the newest code from GIThub
os.system("cd ProjectMinkPi git pull")

#Rebooting the Pi
os.system("sudo reboot")

exit(0)