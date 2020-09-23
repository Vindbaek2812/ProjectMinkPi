
import os
import time

#time.sleep(15)

#starting up the CAN port so it will be able to read from it
os.system("sudo ip link set can0 up type can bitrate 250000")


#Starting the exchange to start RabbitMQ
os.system("python exchange.py sensorData")

#Starting both the CAN script and the consumer that sends the data from RabbitMQ to Azure IoTHub
os.system("python consumer-to-azure.py & python3 CANreader.py")

exit(0)