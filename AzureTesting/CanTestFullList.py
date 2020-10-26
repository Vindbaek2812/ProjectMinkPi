import can

can_interface = 'can1'
bus = can.interface.Bus(can_interface, bustype='socketcan')
while True:
    message = bus.recv(1.0)  # Timeout in seconds.
    print(message)
    #if message.arbitration_id==301:
        #data = str(bytearray(message.data).hex())
        #data1 = data[4:6]
        #data2 = data[6:8]
        #value2 = int("0x" + data1, 0) + 256 * int("0x" + data2, 0)
        #print('RPMreader: ' + str(value2))
        #print("=====================")
    #if message.arbitration_id==303:
        #data = str(bytearray(message.data).hex())
        #print(message)
        
        
        
        #50 timer 32 00 00 00
        #150 timer 96 00 00 00
        #2000 timer d0 07 00 00
        #4000 timer a0 0f 00 00
        #25005 timer ad 61 00 00
        #100025 timer 