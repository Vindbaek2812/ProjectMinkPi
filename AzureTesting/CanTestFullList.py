import can

can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan')
while True:
    message = bus.recv(1.0)  # Timeout in seconds.

    if message.arbitration_id==301:
        data = str(bytearray(message.data).hex())
        data1 = data[4:6]
        data2 = data[6:8]
        value2 = int("0x" + data1, 0) + 256 * int("0x" + data2, 0)
        print('RPMreader: ' + str(value2))
        print("=====================")
