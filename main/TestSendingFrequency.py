import re
import pika
import time
from datetime import datetime
import can

#Different atributes from the CAN bus
motorTemp = 20
hydraulicTemp = 20
fuelLevel=100
hydraulicPressure=10
motorRPM=10
TimeSinceHydServ = 10
TimeSinceMotServ = 10
MechanicalMotTime = 10
MotRunTimeHour = 10
MotRunTimeMin = 10
alarms=""

# Set the delay time
delaytime = 1

# Set up the exchange environment
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Define the JSON message to send to IoT Hub.
#MSG_TXT = '{{"motorTemp": {motorTemp},"hydraulicTemp": {hydraulicTemp},"fuelLevel":{fuelLevel},"hydraulicPressure":{hydraulicPressure}, "alarms":{alarms}, "nowTime": {nowTime}}}'
Rabbitmessage = ""
# Establish the exchange
channel.exchange_declare(exchange='sensor_exchange', exchange_type='topic')

# Define CAN bus socket
can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan')

#assembles the message with sensorDATA
def makeString(stringPart):
    global Rabbitmessage
    if(Rabbitmessage==""):
        Rabbitmessage = Rabbitmessage + stringPart
    else:
        Rabbitmessage = Rabbitmessage + ',' + stringPart


def SendString():
    nowdatetime = datetime.now()
    nowTime = str(nowdatetime.strftime('%d/%m/%y - %H:%M:%S'))
    nowTime = '"' + nowTime + '"'
    global Rabbitmessage
    Rabbitmessage=('{' + Rabbitmessage + ',' + nowTime + '}')

    #This line is sending the message to RabbitMQ
    #channel.basic_publish(exchange='sensor_exchange',routing_key='sensorData',body=Rabbitmessage)
    print(Rabbitmessage)

def id300(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[4:6]
    global fuelLevel
    if (fuelLevel != int(data1, 0)):
        fuelLevel = int(data1, 0)
        makeString("fuelLevel:" + str(fuelLevel))

    data2 = "0x" + data[8:10]
    global hydraulicPressure
    if(hydraulicPressure!=int(data2, 0)):
        hydraulicPressure = int(data1, 0)
        makeString("hydraulicPressure:" + str(hydraulicPressure))

    data3 = "0x" + data[12:14]
    global hydraulicTemp
    if(hydraulicTemp!=int(data3,0)):
        hydraulicTemp = int(data3, 0)
        makeString("hydraulicTemp:" + str(hydraulicTemp))



def id301(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    global motorTemp
    if(motorTemp!=int(data1,0)):
        motorTemp = int(data1, 0)
        makeString("motorTemp:" + str(motorTemp))
    data2 = "0x" + data[2:4]
    global motorRPM
    motorRPM = int(data2, 0)
    # print('Motor RPM: ' + str(motorRPM))


def id302(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    global TimeSinceHydServ
    TimeSinceHydServ = int(data1, 0)
    # print('Time since Hyd service: ' + str(TimeSinceHydServ))
    data2 = "0x" + data[4:6]
    global TimeSinceMotServ
    TimeSinceMotServ = int(data1, 0)
    # print('Time since Mot service: ' + str(TimeSinceMotServ))


def id303(data):
    data = str(bytearray(data).hex())


def id304(data):
    errorIndex = 0
    errorList = ''
    index = 0
    errors = [80, 40, 20, 10, 8, 4, 2, 1]
    alarmvalue = str(bytearray(data).hex())
    # print(alarmvalue)
    col1 = alarmvalue[0:2]
    col2 = alarmvalue[2:4]
    col3 = alarmvalue[4:6]
    columns = [col1, col2, col3]
    # print(col1, col2, col3)
    for value in columns:
        index = index + 1
        if (re.search('[a-zA-Z]', value)):
            if (value == "c0" and index == 3):
                errorList = errorList + '16-17-'
        else:
            value = int(value)
            for error in errors:
                if (error <= value):
                    value = value - error
                    # print(errorIndex)
                    errorList = (errorList + str(errorIndex) + '-')
                errorIndex = errorIndex + 1
    global alarms
    alarmsList = errorList.rstrip('-')
    if (alarmsList!=alarms):
        alarms = '"' + alarmsList + '"'
        makeString('alarms:' + str(alarms))



def ReadCANData(col300, col301, col302, col303, col304):
    messageID0 = col300
    messageID1 = col301
    messageID2 = col302
    messageID3 = col303
    messageID4 = col304
    while messageID0 == False or messageID1 == False or messageID2 == False or messageID3 == False or messageID4 == False:
        message = bus.recv(10.0)  # timeout in seconds

        if message.arbitration_id == 300 and messageID0 == False:
            id300(message.data)
            messageID0 = True

        elif message.arbitration_id == 301 and messageID1 == False and messageID0==True:
            id301(message.data)
            messageID1 = True

        elif message.arbitration_id == 302 and messageID2 == False and messageID1==True:
            id302(message.data)
            messageID2 = True

        elif message.arbitration_id == 303 and messageID3 == False and messageID2==True:
            id303(message.data)
            messageID3 = True

        elif message.arbitration_id == 304 and messageID4 == False and messageID3==True:
            id304(message.data)
            messageID4 = True

        if (messageID4==True):
            SendString()

while True:
    col300 = False
    col301 = False
    col302 = False
    col303 = False
    col304 = False
    ReadCANData(col300, col301, col302, col303, col304)

connection.close()
