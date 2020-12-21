import random
import time
from datetime import datetime
import math

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=ThyrrestrupMinkIoTHub1.azure-devices.net;DeviceId=ThyrrestrupDevice;SharedAccessKey=sGxsUoGiXTSkZlwKP2otiqlzgm9wzmlXPF8Qgi85kEA="

MOTORTEMP = 24
HYDTEMP = 10
FUELLEVEL = 34
HYDPRESSURE = 21
ALARMS = ""
RPM = 1000
MOTORRUNTIMER = 250
MOTORRUNTIMER = 12

MSG_TXT = '{{"motorTemp": {motorTemp},"hydraulicTemp": {hydraulicTemp},"fuelLevel": {fuelLevel},"hydraulicPressure": {hydraulicPressure},"alarms": "{alarms}","RPM": {RPM},"motorRunTimerHour": {motorRunTimerHour},"mechanicalMotorTimer": {mechanicalMotorTimer},"TimeSinceHydServ": {timeSinceHydService},"TimeSinceMotServ": {timeSinceMotService},"nowTime": "{unconvTime}" }}'


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        while bool(client):
            # Build the message with simulated telemetry values.
            MOTTEMP = MOTORTEMP + (random.random() * 15)
            HYDRATEMP = HYDTEMP + (random.random() * 20)
            RPMmm = RPM + (random.random() * 100)
            HYDPRES = HYDPRESSURE + (random.random() * 12)
            MOTTEMP = math.trunc(MOTTEMP)
            HYDRATEMP = math.trunc(HYDRATEMP)
            RPMmm = math.trunc(RPMmm)
            HYDPRES = math.trunc(HYDPRES)

            NOWTIME = datetime.now()
            NOWTIME = str(NOWTIME.strftime('%d/%m/%y - %H:%M:%S'))
            RabbitMessage = MSG_TXT.format(motorTemp=MOTTEMP, hydraulicTemp=HYDRATEMP, fuelLevel=32,
                                           hydraulicPressure=HYDPRES, alarms="", RPM=RPMmm, motorRunTimerHour=12,
                                           mechanicalMotorTimer=12, timeSinceHydService=12, timeSinceMotService=12,
                                           unconvTime=NOWTIME)


            message = Message(RabbitMessage)

            # Send the message.
            print("Sending message: {}".format(message))
            client.send_message(message)
            print("Message successfully sent")
            time.sleep(5)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")


if __name__ == '__main__':
    print("IoT Hub Quickstart #1 - Simulated device")
    print("Press Ctrl-C to exit")
    iothub_client_telemetry_sample_run()
