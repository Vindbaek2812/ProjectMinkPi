#!/usr/bin/env python
import pika
from azure.iot.device import IoTHubDeviceClient, Message

# Selects the IoT Hub based on user selection
# Student IoT Hub
CONNECTION_STRING = "HostName=ThyrrestrupMinkIoTHub.azure-devices.net;DeviceId=ThyrrestrupMinkDevice;SharedAccessKey=2veqtyJShmtnORMdBZTGUZtvX8Zm9i06y6YRz3kK+EU="
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
    try:
        unsent = True
        while bool(unsent):
            b = client.send_message(message)
            print(b)
            if(b==True):
                print("Sending message: {}".format(message))
                unsent = False

            client = iothub_client_init()
    except:
        client = iothub_client_init()


queue_name = 'sensorData'

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

#Printing the whole statement to troubleshoot
print(' [*] PiTestConsumer is waiting for messages. To exit press CTRL + C...')
channel.start_consuming()
