
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
MSG_TXT = '{{"motorTemp": {motorTemp},"hydraulicTemp": {hydraulicTemp},"fuelLevel":{fuelLevel},"hydraulicPressure":{hydraulicPressure}, "alarms":{alarms}, "nowTime": {nowTime}}}'
Rabbitmessage = ""
# Establish the exchange
channel.exchange_declare(exchange='sensor_exchange', exchange_type='topic')

can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan')

def id300(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[4:6]
    global fuelLevel
    fuelLevel = int(data1, 0)
    # print('Fuel level: ' + str(fuelLevel))
    data1 = "0x" + data[8:10]
    global hydraulicPressure
    hydraulicPressure = int(data1, 0)
    # print('Fuel level: ' + str(hydraulicPressure))
    data4 = "0x" + data[12:14]
    global hydraulicTemp
    hydraulicTemp = int(data4, 0)
    #print('Hydraulic temp: ' + str(hydraulicTemp))


def id301(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    global motorTemp
    motorTemp = int(data1, 0)
    #print('Motor temp: ' + str(motorTemp))
    data2 = "0x" + data[2:4]
    global motorRPM
    motorRPM = int(data2, 0)
    # print('Motor RPM: ' + str(motorRPM))


def id302(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    global TimeSinceHydServ
    TimeSinceHydServ = int(data1, 0)
    #print('Time since Hyd service: ' + str(TimeSinceHydServ))
    data2 = "0x" + data[4:6]
    global TimeSinceMotServ
    TimeSinceMotServ = int(data1, 0)
    #print('Time since Mot service: ' + str(TimeSinceMotServ))


def id303(data):
    data = str(bytearray(data).hex())

def id304(data):
    errorIndex = 0
    errorList=''
    errors = [80, 40, 20, 10, 8, 4, 2, 1]
    alarmvalue = str(bytearray(data).hex())
    print(alarmvalue)
    col1 = alarmvalue[0:2]
    col2 = alarmvalue[2:4]
    col3 = alarmvalue[4:6]
    columns = [col1, col2, col3]
    print(col1, col2, col3)
    for value in columns:
        if (re.search('[a-zA-Z]', value)):
            print("contains a letter")
        else:
            value = int(value)
            for error in errors:
                if (error <= value):
                    value = value - error
                    # print(errorIndex)
                    errorList = (errorList + str(errorIndex) + ',')
                errorIndex = errorIndex + 1
    global alarms
    alarms = errorList.rstrip(',')
    print(alarms)

def ReadCANData(col300, col301, col302, col303, col304):
    messageID0 = col300
    messageID1 = col301
    messageID2 = col302
    messageID3 = col303
    messageID4 = col304
    while messageID0 == False or messageID1 == False or messageID2 == False or messageID3 == False or messageID4 == False:
        message = bus.recv(1.0)  # timeout in seconds

        if message.arbitration_id == 300 and messageID0 == False:
            id300(message.data)
            messageID0 = True
            
        elif message.arbitration_id == 301 and messageID1 == False:
            id301(message.data)
            messageID1 = True
            
        elif message.arbitration_id == 302 and messageID2 == False:
            id302(message.data)
            messageID2 = True
            
        elif message.arbitration_id == 303 and messageID3 == False:
            id303(message.data)
            messageID3 = True
            
        elif message.arbitration_id == 304 and messageID4 == False:
            id304(message.data)
            messageID4 = True

while True:
    col300 = False
    col301 = False
    col302 = False
    col303 = False
    col304 = False
    ReadCANData(col300, col301, col302, col303, col304)


    nowdatetime = datetime.now()
    nowTime = str(nowdatetime.strftime('%d/%m/%y - %H:%M:%S'))
    nowTime = '"' + nowTime + '"'
    msg_txt_formatted = MSG_TXT.format(motorTemp=motorTemp, hydraulicTemp=hydraulicTemp, fuelLevel=fuelLevel, hydraulicPressure=hydraulicPressure, alarms=alarms, nowTime=nowTime)
    Rabbitmessage = msg_txt_formatted

    #channel.basic_publish(exchange='sensor_exchange',routing_key='sensorData',body=Rabbitmessage)
    time.sleep(delaytime)
    #print(Rabbitmessage)

connection.close()
