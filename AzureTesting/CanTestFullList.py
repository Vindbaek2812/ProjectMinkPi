import can


bus = can.interface.Bus('can0', bustype='socketcan')
while True:
    print(bus.recv(1.0))
