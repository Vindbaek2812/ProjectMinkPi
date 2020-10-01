import re
import pika
import time
from datetime import datetime
import can

#Different atributes from the CAN bus
motorTemp = None
hydraulicTemp = None
fuelLevel=None
hydraulicPressure=None
motorRPM=None
TimeSinceHydServ = None
TimeSinceMotServ = None
MechanicalMotTime = None
MotRunTimeHour = None
MotRunTimeMin = None
alarms=""
RabbitMessage = ""

# Set the delay time
delaytime = 1

# Set up the exchange environment
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# Establish the exchange
channel.exchange_declare(exchange='sensor_exchange', exchange_type='topic')

# Define CAN bus socket
can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan')

#assembles the message with sensorDATA from each column
def makeString(stringPart):
    global RabbitMessage
    if(RabbitMessage==""):
        RabbitMessage = RabbitMessage + stringPart
    else:
        RabbitMessage = RabbitMessage + ',' + stringPart

def SendString():
    global RabbitMessage
    if(len(RabbitMessage) > 0):
        nowdatetime = datetime.now()
        nowTime = str(nowdatetime.strftime('%d/%m/%y - %H:%M:%S'))
        RabbitMessage=('{' + RabbitMessage + ',' + '"' + nowTime + '"' + '}')

        #This line is sending the message to RabbitMQ
        #channel.basic_publish(exchange='sensor_exchange',routing_key='sensorData',body=RabbitMessage)
        #print(RabbitMessage)
        RabbitMessage=""
    #else:
        #print("Nothing has changed")
    
#Method for converting node 300 on the CAN bus to readable data and sending it to the makeString method for assembling it into a combined string
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
        hydraulicPressure = int(data2, 0)
        makeString("hydraulicPressure:" + str(hydraulicPressure))
    data3 = "0x" + data[12:14]
    global hydraulicTemp
    if(hydraulicTemp!=int(data3,0)):
        hydraulicTemp = int(data3, 0)
        makeString("hydraulicTemp:" + str(hydraulicTemp))

#Method for converting node 301 on the CAN bus to readable data and sending it to the makeString method for assembling it into a combined string
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

#Method for converting node 302 on the CAN bus to readable data and sending it to the makeString method for assembling it into a combined string
def id302(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    global TimeSinceHydServ
    if(TimeSinceHydServ!=int(data1,0)):
        TimeSinceHydServ = int(data1, 0)
        makeString("TimeSinceHydServ:" + TimeSinceHydServ)
    data2 = "0x" + data[4:6]
    global TimeSinceMotServ
    if (TimeSinceMotServ != int(data2, 0)):
        TimeSinceMotServ = int(data1, 0)
        makeString("TimeSinceMotServ:" + TimeSinceMotServ)
    data3 = "0x" + data[8:14]
    global MechanicalMotTime
    if (MechanicalMotTime != int(data3, 0)):
        MechanicalMotTime = int(data3, 0)
        print("MechanicalMotTime:" + MechanicalMotTime * 10)


#Method for converting node 303 on the CAN bus to readable data and sending it to the makeString method for assembling it into a combined string
def id303(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:6]
    print(data1)
    global MotRunTimeHour
    if (MotRunTimeHour != int(data1, 0)):
        MotRunTimeHour = int(data1, 0)
        print("MotRunTimeHour:" + MotRunTimeHour * 10)
        print("MotRunTimeHour:" + MotRunTimeHour)
#Method for converting node 304 on the CAN bus to readable data and sending it to the makeString method for assembling it into a combined string
def id304(data):
    errorIndex = 0
    errorList = ''
    index = 0
    errors = [80, 40, 20, 10, 8, 4, 2, 1]
    alarmvalue = str(bytearray(data).hex())
    col1 = alarmvalue[0:2]
    col2 = alarmvalue[2:4]
    col3 = alarmvalue[4:6]
    columns = [col1, col2, col3]
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
                    errorList = (errorList + str(errorIndex) + '-')
                errorIndex = errorIndex + 1
    global alarms
    alarmsList = errorList.rstrip('-')
    if (alarmsList!=alarms):
        alarms=alarmsList
        makeString('alarms:' + str('"' + alarmsList + '"'))


#This method is sorting the CAN messages into each arbitration Id
def ReadCANData(col300, col301, col302, col303, col304):
    while col300 == False or col301 == False or col302 == False or col303 == False or col304 == False:
        message = bus.recv(10.0)  # timeout in seconds

        if message.arbitration_id == 300 and col300 == False:
            id300(message.data)
            col300 = True
            
        elif message.arbitration_id == 301 and col301 == False and col300==True:
            id301(message.data)
            col301 = True

        elif message.arbitration_id == 302 and col302 == False and col301==True:
            id302(message.data)
            col302 = True

        elif message.arbitration_id == 303 and col303 == False and col302==True:
            id303(message.data)
            col303 = True

        elif message.arbitration_id == 304 and col304 == False and col303==True:
            id304(message.data)
            col304 = True

        if (col304==True):
            SendString()

#This keeps the script running infinitely
while True:
    ReadCANData(False, False, False, False, False)

connection.close()
