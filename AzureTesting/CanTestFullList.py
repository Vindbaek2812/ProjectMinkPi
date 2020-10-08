import can

can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan')
while True:
    message = bus.recv(1.0)  # Timeout in seconds.

    if message.arbitration_id==301:
        print(message)
        data = str(bytearray(message.data).hex())
        data1 = "0x" + data[4:6]
        value1 = int(data1, 0)
        print('RPMreader1: ' + str(value1))

        data = str(bytearray(message.data).hex())
        data2 = "0x" + data[4:6] + 256 * data[6:8]
        value2 = int(data2, 0)
        print('RPMreader2: ' + str(value2))
        print("=====================")
