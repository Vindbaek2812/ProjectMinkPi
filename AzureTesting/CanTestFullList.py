import can

can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan')
while True:
    message = bus.recv(1.0)  # Timeout in seconds.
    #print(message)
    if message.arbitration_id==300:
        #print(message)
        data = str(bytearray(message.data).hex())
        data1 = "0x" + data[4:6]
        value1 = int(data1, 0)
        #print('Fuel level: ' + str(value1))
        data2 = "0x" + data[8:10]
        value1 = int(data2, 0)
        #print('Hydraulic Pressure: ' + str(value1))
        
    if message.arbitration_id==301:
        #print(message)
        data = str(bytearray(message.data).hex())
        data1 = "0x" + data[4:6]
        value1 = int(data1, 0)
        #print('RPM: ' + str(value1))
    
    if message.arbitration_id==304:
        #print(message.data)
        messageData = (str(bytearray(message.data).hex()))
        print(messageData)