import os
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubDeviceClient


async def main():
    conn_str = "HostName=ThyrrestrupMinkIoTHub1.azure-devices.net;DeviceId=Service;SharedAccessKey=T4X/stmoiOd4uGO8co6CI7c9l5P5xxS/I1HOm87zPto="
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str,)


    # connect the client.
    await device_client.connect()
    print("Connected to Azure IoT hub")

    # define behavior for receiving a message
    # NOTE: this could be a function or a coroutine
    def message_received_handler(message):
        print("the data in the message received was ")
        print(message.data)
        command=str(message.data)
        if("update" in command):
            print("update the damn thing")

    # set the message received handler on the client
    device_client.on_message_received = message_received_handler

    # define behavior for halting the application
    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                print("Quitting...")
                break

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for messages
    await user_finished

    # Finally, disconnect
    await device_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
