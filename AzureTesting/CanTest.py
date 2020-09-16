import can

def id300(data):    
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    value1 = int(data1,0)
    print('Feed level: ' + str(value1))
    data4 = "0x" + data[12:14]
    value4 = int(data4, 0)
    print('Hydraulic temp: ' + str(value4))

def id301(data):
    data = str(bytearray(data).hex())
    data1 = "0x" + data[0:2]
    value1 = int(data1, 0)
    print('Motor temp: ' + str(value1))
    data2 = "0x" + data[2:4]
    value2 = int(data2, 0)
    print('Motor RPM: ' + str(value2))

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
    
try:
    can_interface = 'can0'
    bus = can.interface.Bus(can_interface, bustype='socketcan')
    while True:
        message = bus.recv(1.0)  # Timeout in seconds.
        #print(message)
        #messageData = (str(bytearray(message.data).hex()))
        #print(messageData)
    
        if message.arbitration_id==300:
            id300(message.data)
        elif message.arbitration_id==301:
            id301(message.data)
        elif message.arbitration_id==302:
            id302(message.data)
        elif message.arbitration_id==303:
            id303(message.data)
        elif message.arbitration_id==304:
            id304(message.data)
except:
    print("CAN bus error")
