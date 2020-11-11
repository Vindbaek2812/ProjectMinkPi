#!/usr/bin/env python
import pika
import time
from azure.iot.device import IoTHubDeviceClient, Message

# Selects the IoT Hub based on user selection
# Student IoT Hub
CONNECTION_STRING = "HostName=ThyrrestrupMinkIoTHub1.azure-devices.net;DeviceId=ThyrrestrupDevice;SharedAccessKey=sGxsUoGiXTSkZlwKP2otiqlzgm9wzmlXPF8Qgi85kEA="
client=""

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='sensor_exchange', exchange_type='topic')


def iothub_client_init():
    # Create an IoT Hub client
    print("Connecting to " + "'"+CONNECTION_STRING+"'")
    global client
    client = IoTHubDeviceClient.create_from_connection_string(
        CONNECTION_STRING)
    return client

def callback(ch, method, properties, body):
    # print(str(body))
    global client
    # Converts the message into a object that is readable to Azure
    message = Message(body)
    unsent = True
    while(unsent):
        try:
            client.send_message(message)
            print("Sending message: {}".format(message))
            unsent = False
        except:
            print("Nothing was sent")
            time.sleep(10)
            client = iothub_client_init()


queue_name = 'sensorData'

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

#Printing the whole statement to troubleshoot
print(' [*] PiTestConsumer is waiting for messages. To exit press CTRL + C...')
channel.start_consuming()
