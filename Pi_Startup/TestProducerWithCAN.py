
import sys
import pika
import time
from datetime import datetime
import can

#Different atributes from the CAN bus
motorTemp=20
hydraulicTemp=20
fuelLevel=100

# Set the delay time
delaytime=1

# Checking for changes in different nodes
col300=False
col301=False
col302=False
col303=False
col304=False

# Set up the exchange environment

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Define the JSON message to send to IoT Hub.
MSG_TXT = '{{"motorTemp": {motorTemp},"hydraulicTemp": {hydraulicTemp}, "nowTime": {nowTime}}}'
Rabbitmessage = ""
# Establish the exchange
channel.exchange_declare(exchange='sensor_exchange', exchange_type='topic')

# Define the CAN bus and setting up the interface to start reading from it


def id300(data):    
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    value1 = int(data1,0)
    #print('Feed level: ' + str(value1))
    data4 = "0x" + data[12:14]
    global hydraulicTemp
    hydraulicTemp = int(data4, 0)
    #print('Hydraulic temp: ' + str(value4))

def id301(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    global motorTemp
    motorTemp = int(data1, 0)
    #print('Motor temp: ' + str(value1))
    data2 = "0x" + data[2:4]
    value2 = int(data2, 0)
    #print('Motor RPM: ' + str(value2))

def id302(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    value1 = int(data1, 0)
    #print('Time since Hyd service: ' + str(value1))
    data2 = "0x" + data[2:4]
    value1 = int(data1, 0)
    #print('Time since Hyd service: ' + str(value1))

def id303(data):
    data = str(bytearray(data).hex())
    

def id304(data):
    data = str(bytearray(data).hex())
    
#defining CAN bus
can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan')
while True:
    message = bus.recv(1.0)  # Timeout in seconds.
    
    #uncomment this to see the whole can message
    #print(message)
    #messageData = (str(bytearray(message.data).hex()))
    #print(messageData)

    if message.arbitration_id==300: 
        id300(message.data)
        print("change to col300")
    elif message.arbitration_id==301:
        id301(message.data)
        print("change to col301")
    elif message.arbitration_id==302:
        id302(message.data)
        print("change to col302")
    elif message.arbitration_id==303:
        id303(message.data)
        print("change to col303")
    elif message.arbitration_id==304:
        id304(message.data)
        print("change to col304")

    if col300==False & col301==False:
        nowdatetime = datetime.now()
        nowTime = str(nowdatetime.strftime('%d/%m/%y - %H:%M:%S'))
        nowTime = '"' + nowTime + '"'
        msg_txt_formatted = MSG_TXT.format(motorTemp=motorTemp, hydraulicTemp=hydraulicTemp, nowTime=nowTime)
        Rabbitmessage = msg_txt_formatted

    #Variable delay here
    #time.sleep(delaytime)
    
        channel.basic_publish(exchange='sensor_exchange',
                              routing_key='sensorData',
                              body=Rabbitmessage)

print(" [X] Sent %r:%r" % (routing_key, Rabbitmessage))

connection.close()


