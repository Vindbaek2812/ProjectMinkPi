import sys
import pika
import random
import time
from datetime import datetime

# Set up the exchange environment

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}, "nowTime": {nowTime}}}'
message = ""
# Establish the exchange
channel.exchange_declare(exchange='sensor_exchange', exchange_type='topic')

while True:
    time.sleep(1)
    temperature = TEMPERATURE + (random.random() * 15)
    humidity = HUMIDITY + (random.random() * 20)
    nowdatetime = datetime.now()
    nowTime = str(nowdatetime.strftime('%d/%m/%y - %H:%M:%S'))
    nowTime = '"' + nowTime + '"'
    msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity, nowTime=nowTime)
    message = msg_txt_formatted
    
    channel.basic_publish(exchange='sensor_exchange',
                          routing_key='sensorData',
                          body=message)

print(" [X] Sent %r:%r" % (routing_key, message))

connection.close()

