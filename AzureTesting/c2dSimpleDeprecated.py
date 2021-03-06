import threading
import time
from azure.iot.device import IoTHubDeviceClient

CONNECTION_STRING = "HostName=ThyrrestrupMinkIoTHub1.azure-devices.net;DeviceId=Service;SharedAccessKey=T4X/stmoiOd4uGO8co6CI7c9l5P5xxS/I1HOm87zPto="

RECEIVED_MESSAGES = 0

def message_listener(client):
    global RECEIVED_MESSAGES
    while True:
        message = client.receive_message()
        RECEIVED_MESSAGES += 1
        print("\nMessage received:")

        #print data and both system and application (custom) properties
        for property in vars(message).items():
            print ("    {0}".format(property))

        print( "Total calls received: {}".format(RECEIVED_MESSAGES))
        print()

def iothub_client_sample_run():
    try:
        print("Connecting")
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        print("Connected")
        message_listener_thread = threading.Thread(target=message_listener, args=(client,))
        message_listener_thread.daemon = True
        message_listener_thread.start()

        while True:
            time.sleep(1000)

    except KeyboardInterrupt:
        print ( "IoT Hub C2D Messaging device sample stopped" )

print ( "Starting the Python IoT Hub C2D Messaging device sample..." )
print ( "Waiting for C2D messages, press Ctrl-C to exit" )

iothub_client_sample_run()